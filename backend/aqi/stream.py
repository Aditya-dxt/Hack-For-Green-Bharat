"""
Hybrid AQI Engine (Official CPCB + Fallbacks)

Priority Order:
1) Official CPCB API (data.gov.in)
2) OpenAQ Live Data
3) Simulation

India-focused.
"""

from datetime import datetime, timedelta
import random
import math
import time
import os
from typing import Dict, List, Tuple
import requests

CACHE_TTL = 300
CPCB_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
CPCB_BASE_URL = "https://api.data.gov.in/resource"

# 🔐 Hardcoded API Key
CPCB_API_KEY = "62a0a8bb9c9e1790d5eb1da4248e76e6dafbb8ad"


class AQIStream:

    def __init__(self):
        self.cache: Dict[str, Tuple[float, Dict]] = {}

        self.cities = {
            "Delhi": {"lat": 28.6139, "lng": 77.2090, "baseline": 300},
            "Mumbai": {"lat": 19.0760, "lng": 72.8777, "baseline": 160},
            "Bangalore": {"lat": 12.9716, "lng": 77.5946, "baseline": 110},
            "Chennai": {"lat": 13.0827, "lng": 80.2707, "baseline": 130},
            "Kolkata": {"lat": 22.5726, "lng": 88.3639, "baseline": 200},
            "Hyderabad": {"lat": 17.3850, "lng": 78.4867, "baseline": 140},
            "Pune": {"lat": 18.5204, "lng": 73.8567, "baseline": 150},
            "Ahmedabad": {"lat": 23.0225, "lng": 72.5714, "baseline": 180},
            "Lucknow": {"lat": 26.8467, "lng": 80.9462, "baseline": 220},
            "Jaipur": {"lat": 26.9124, "lng": 75.7873, "baseline": 190},
        }

    # ---------------------------------------------------
    # PUBLIC
    # ---------------------------------------------------

    def get_current(self, city: str) -> Dict:
        if city not in self.cities:
            raise ValueError("Unsupported city")

        # Cache
        if city in self.cache and time.time() - self.cache[city][0] < CACHE_TTL:
            return self.cache[city][1]

        # 1️⃣ Try CPCB
        cpcb = self._fetch_cpcb(city)
        if cpcb:
            self.cache[city] = (time.time(), cpcb)
            return cpcb

        # 2️⃣ Try OpenAQ
        live = self._fetch_openaq(city)
        if live:
            self.cache[city] = (time.time(), live)
            return live

        # 3️⃣ Simulation fallback
        sim = self._simulate(city)
        return sim

    def get_history(self, city: str, range: str):
        now = datetime.now()
        data = []

        if range == "24h":
            for h in range(24, -1, -1):
                ts = now - timedelta(hours=h)
                data.append({
                    "time": ts.strftime("%H:%M"),
                    "aqi": self._simulate(city, ts)["aqi"]
                })
        elif range == "7d":
            for d in range(7, -1, -1):
                ts = now - timedelta(days=d)
                data.append({
                    "time": ts.strftime("%b %d"),
                    "aqi": self._simulate(city, ts)["aqi"]
                })
        return data

    def get_all_cities(self):
        result = []
        for city in self.cities:
            cur = self.get_current(city)
            result.append({
                "name": city,
                "lat": self.cities[city]["lat"],
                "lng": self.cities[city]["lng"],
                "aqi": cur["aqi"],
                "severity": cur["severity"],
                "source": cur["source"]
            })
        return sorted(result, key=lambda x: x["aqi"], reverse=True)

    def get_insights(self, city):
        cur = self.get_current(city)
        hist = self.get_history(city, "24h")
        trend = "increasing" if hist[-1]["aqi"] > hist[0]["aqi"] else "decreasing"
        avg = sum(x["aqi"] for x in hist) / len(hist)
        return {
            "city": city,
            "trend": trend,
            "avg_24h": round(avg, 1),
            "current": cur["aqi"],
            "severity": cur["severity"],
            "source": cur["source"]
        }

    # ---------------------------------------------------
    # CPCB FETCH
    # ---------------------------------------------------

    def _fetch_cpcb(self, city):
        if not CPCB_API_KEY:
            return None

        try:
            response = requests.get(
                f"{CPCB_BASE_URL}/{CPCB_RESOURCE_ID}",
                params={
                    "api-key": CPCB_API_KEY,
                    "format": "json",
                    "filters[city]": city,
                    "limit": 50,
                    "sort": "-last_update"
                },
                timeout=8
            )

            data = response.json()
            records = data.get("records", [])

            if not records:
                return None

            # Worst station logic
            worst = max(records, key=lambda r: int(r.get("aqi", 0)))

            aqi = int(worst.get("aqi", 0))

            return {
                "city": city,
                "aqi": aqi,
                "pm25": float(worst.get("pm2_5", 0) or 0),
                "pm10": float(worst.get("pm10", 0) or 0),
                "timestamp": worst.get("last_update"),
                "severity": self._severity(aqi),
                "description": self._desc(aqi),
                "source": "CPCB"
            }

        except:
            return None

    # ---------------------------------------------------
    # OPENAQ FETCH
    # ---------------------------------------------------

    def _fetch_openaq(self, city):
        try:
            r = requests.get(
                "https://api.openaq.org/v2/latest",
                params={"city": city},
                timeout=6
            )

            data = r.json()

            pm25, pm10 = None, None

            for res in data.get("results", []):
                for m in res.get("measurements", []):
                    if m["parameter"] == "pm25":
                        pm25 = float(m["value"])
                    if m["parameter"] == "pm10":
                        pm10 = float(m["value"])

            if pm25 or pm10:
                aqi = self._calculate_cpcb(pm25, pm10)
                return self._format(city, aqi, pm25, pm10, "OpenAQ")

        except:
            return None

    # ---------------------------------------------------
    # CPCB CALCULATION (for fallback)
    # ---------------------------------------------------

    def _subindex(self, conc, bps):
        for lo, hi, a_lo, a_hi in bps:
            if lo <= conc <= hi:
                return ((a_hi - a_lo)/(hi - lo))*(conc - lo) + a_lo
        return 500

    def _calculate_cpcb(self, pm25, pm10):
        pm25_bp = [(0,30,0,50),(31,60,51,100),(61,90,101,200),
                   (91,120,201,300),(121,250,301,400),(251,500,401,500)]

        pm10_bp = [(0,50,0,50),(51,100,51,100),(101,250,101,200),
                   (251,350,201,300),(351,430,301,400),(431,600,401,500)]

        subs = []
        if pm25:
            subs.append(self._subindex(pm25, pm25_bp))
        if pm10:
            subs.append(self._subindex(pm10, pm10_bp))

        return int(round(max(subs))) if subs else 0

    # ---------------------------------------------------
    # SIMULATION
    # ---------------------------------------------------

    def _simulate(self, city, ts=None):
        cfg = self.cities[city]
        now = ts or datetime.now()

        base = cfg["baseline"]
        diurnal = math.sin(now.hour / 24 * math.pi) * 40
        noise = random.gauss(0, 25)

        pm25 = max(10, base * 0.35 + diurnal + noise)
        pm10 = max(20, base * 0.6 + diurnal + noise)

        aqi = self._calculate_cpcb(pm25, pm10)
        return self._format(city, aqi, pm25, pm10, "simulation")

    # ---------------------------------------------------
    # HELPERS
    # ---------------------------------------------------

    def _format(self, city, aqi, pm25, pm10, source):
        return {
            "city": city,
            "aqi": aqi,
            "pm25": round(pm25,1) if pm25 else None,
            "pm10": round(pm10,1) if pm10 else None,
            "timestamp": datetime.utcnow().isoformat(),
            "severity": self._severity(aqi),
            "description": self._desc(aqi),
            "source": source
        }

    def _severity(self, aqi):
        if aqi <= 50: return "good"
        if aqi <= 100: return "satisfactory"
        if aqi <= 200: return "moderate"
        if aqi <= 300: return "poor"
        if aqi <= 400: return "very-poor"
        return "severe"

    def _desc(self, aqi):
        if aqi <= 50: return "Minimal impact."
        if aqi <= 100: return "Minor breathing discomfort."
        if aqi <= 200: return "Breathing discomfort to sensitive groups."
        if aqi <= 300: return "Breathing discomfort to most people."
        if aqi <= 400: return "Respiratory illness on prolonged exposure."
        return "Serious health impact."
