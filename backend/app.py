"""
Environmental Intelligence API
CPCB-based AQI + Live + Simulation + Insights
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import uvicorn

from yolo.detector import YOLODetector
from aqi.stream import AQIStream
from reports.processor import ReportProcessor

# -------------------------------------------------------------------
# FastAPI Initialization
# -------------------------------------------------------------------

app = FastAPI(
    title="Environmental Intelligence API (India CPCB)",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# Services
# -------------------------------------------------------------------

yolo_detector = YOLODetector()
aqi_engine = AQIStream()
report_processor = ReportProcessor()

# -------------------------------------------------------------------
# MODELS
# -------------------------------------------------------------------

class ImageAnalysisResponse(BaseModel):
    detected_category: str
    confidence: float
    scores: Dict[str, float]
    detected_objects: List[str]
    explanation: str


class AQICurrentResponse(BaseModel):
    city: str
    aqi: int
    pm25: Optional[float]
    pm10: Optional[float]
    timestamp: str
    severity: str
    description: str
    source: str


class AQIHistoryPoint(BaseModel):
    time: str
    aqi: int


class CityAQIResponse(BaseModel):
    name: str
    lat: float
    lng: float
    aqi: int
    severity: str
    source: str


class ReportSubmission(BaseModel):
    image_data: Optional[str]
    category: str
    latitude: float
    longitude: float
    location_name: str
    yolo_result: Optional[Dict]
    timestamp: str


class ReportSubmissionResponse(BaseModel):
    report_id: str
    status: str
    validation_status: str
    estimated_verification_time: int
    message: str


# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "3.0.0",
        "standard": "Indian CPCB AQI",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/report/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        result = yolo_detector.analyze(image_data)
        return ImageAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/aqi/current", response_model=AQICurrentResponse)
async def get_current(city: str = Query(...)):
    try:
        return AQICurrentResponse(**aqi_engine.get_current(city))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/aqi/history", response_model=List[AQIHistoryPoint])
async def get_history(city: str, range: str = "24h"):
    try:
        data = aqi_engine.get_history(city, range)
        return [AQIHistoryPoint(**p) for p in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cities", response_model=List[CityAQIResponse])
async def get_cities():
    try:
        data = aqi_engine.get_all_cities()
        return [CityAQIResponse(**c) for c in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/insights/aqi")
async def insights(city: str):
    return aqi_engine.get_insights(city)


@app.post("/api/report/submit", response_model=ReportSubmissionResponse)
async def submit(report: ReportSubmission):
    return ReportSubmissionResponse(**report_processor.process_submission(report.dict()))


@app.get("/api/report/status/{report_id}")
async def status(report_id: str):
    return report_processor.get_status(report_id)

@app.get("/api/current/{city}", response_model=AQICurrentResponse)
async def get_current_path(city: str):
    try:
        return AQICurrentResponse(**aqi_engine.get_current(city))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
