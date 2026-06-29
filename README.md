<div align="center">

# 🌿 Hack For Green Bharat
### Streaming RAG-Based Environmental Intelligence System

**A real-time AI-powered environmental monitoring platform**  
built for the Hack For Green Bharat hackathon 🇮🇳

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-hack--for--green--bharat.vercel.app-brightgreen?style=for-the-badge)](https://hack-for-green-bharat-black.vercel.app)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Forks](https://img.shields.io/github/forks/Aditya-dxt/Hack-For-Green-Bharat?style=for-the-badge)](https://github.com/Aditya-dxt/Hack-For-Green-Bharat/network/members)
[![Stars](https://img.shields.io/github/stars/Aditya-dxt/Hack-For-Green-Bharat?style=for-the-badge)](https://github.com/Aditya-dxt/Hack-For-Green-Bharat/stargazers)

</div>

---

## 🖼️ Preview

> *(Drop a screenshot here — drag a PNG into the file on GitHub)*

![Hack For Green Bharat Preview](src/assets/preview.png)

---

## 🌐 Live Demo

👉 [hack-for-green-bharat-black.vercel.app](https://hack-for-green-bharat-black.vercel.app)

---

## 🧩 What Is This?

**Hack For Green Bharat** is a real-time environmental intelligence system that combines:

- **IoT-style sensor simulation** generating live environmental data
- **Citizen reporting** for on-ground issue submission
- **AI anomaly detection** that flags dangerous environmental events
- **RAG (Retrieval-Augmented Generation)** pipeline that explains alerts in plain language
- **Streaming data pipeline** processing events in real time
- A **React + TypeScript frontend** dashboard for live monitoring

```
Sensor Simulation + Citizen Reports

                │

                ▼

       Streaming Data Layer

                │

                ▼

     Anomaly Detection Engine

                │

                ▼

       RAG + LLM AI Engine

  (Context-aware Explanations)

                │

                ▼

    Alert Dispatcher + Logger

                │

                ▼

   Frontend Dashboard (React/TS)
```

---

## ✨ Features

### 📡 Real-Time Streaming Pipeline
- Simulates live environmental sensor data (air quality, water levels, temperature, etc.)
- Event-driven architecture with continuous data ingestion
- WebSocket / streaming layer for low-latency data flow

### 🚨 Anomaly Detection
- Automated flagging of dangerous environmental threshold breaches
- Configurable alert sensitivity per metric
- Audit trail and logging of all detected events

### 🤖 RAG-Based AI Explanations
- LLM-powered natural language explanations for every alert
- Retrieval-Augmented Generation pulls relevant environmental context
- Makes alerts actionable and understandable — not just raw numbers

### 👥 Citizen Reporting
- Citizens can submit environmental issues from the frontend
- Reports feed into the same anomaly detection pipeline
- Ground-truth signals complementing sensor data

### 📊 Intelligence Dashboard
- Live monitoring of environmental metrics
- Alert feed with AI-generated explanations
- Historical data and trend visualization

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React · TypeScript · Vite · Tailwind CSS |
| **Backend** | Python · FastAPI |
| **AI / RAG** | LangChain · ChromaDB · LLM (OpenAI / local) |
| **Streaming** | Real-time event pipeline (streaming module) |
| **ML Models** | Anomaly detection models (models/) |
| **Data** | Environmental datasets (data/) |
| **Deployment** | Vercel (frontend) |

---

## 📂 Project Structure
Hack-For-Green-Bharat/

├── src/                  # React + TypeScript frontend

├── backend/              # FastAPI backend server

├── citizen/              # Citizen reporting module

├── rag/                  # RAG pipeline (LangChain + ChromaDB)

├── models/               # Anomaly detection ML models

├── streaming/            # Real-time data streaming layer

├── services/             # Shared service utilities

├── reporting/            # Alert & report generation

├── integration/          # External API integrations

├── utils/                # Helper functions

├── data/                 # Environmental datasets

├── guidelines/           # Hackathon brief & constraints

├── main.py               # Python backend entry point

└── index.html            # Frontend entry point

---

## 🚀 Getting Started

### Frontend

```bash
# Install dependencies
npm install

# Start dev server
npm run dev        # → http://localhost:5173
```

### Backend (AI + Streaming Engine)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the backend
python main.py
```

---

## 🏆 Hackathon Context

This project was built for **Hack For Green Bharat** — a sustainability-focused hackathon challenging developers to build AI-powered environmental solutions for India.

The system addresses a real problem: environmental alerts in India are often delayed, unclear, and inaccessible to citizens. This platform bridges the gap by combining sensor data, citizen signals, and AI explanations into one real-time dashboard.

---

## 🔮 Roadmap

- [ ] Real IoT sensor integration (replace simulation)
- [ ] Mobile app for citizen reporting
- [ ] Multi-region environmental heatmap
- [ ] Government authority notification system
- [ ] Offline-capable edge deployment

---

## 📄 License

MIT — open source and free to use.

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for third-party credits.

---

<div align="center">
  Built for a greener India 🌱🇮🇳<br/>
  by <a href="https://github.com/Aditya-dxt">Aditya Dixit</a>
</div>
