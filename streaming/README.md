# 📡 Real-Time Streaming Module  
**Hack-For-Green-Bharat**

This module implements **real-time environmental data streaming and processing** for the *Streaming RAG-Based Environmental Intelligence System*.

It is responsible for **live data simulation, ingestion, and incremental processing**, enabling downstream modules (RAG, alerts, dashboards) to operate on **continuously updated environmental signals**.

---

## 👤 Ownership & Role Alignment

**Owner:** Aditya Dixit  
**Role:** Real-Time Streaming & Data Processing Engineer

This module fulfills the following responsibilities from the team role assignment:

- Simulate or ingest live environmental data (AQI / pollution)
- Perform real-time ingestion (no batch processing)
- Incrementally process data (filters, rolling logic, severity-ready output)
- Expose clean, reusable outputs for other modules
- Be demo-friendly and hackathon-safe

---

## 🧩 How This Fits Into the Overall System

[ Live / Simulated Sensors ]
↓
Streaming Module ←── YOU OWN THIS
↓
[ RAG + LLM Explanation Engine ]
↓
[ Alerts / API / Dashboard ]


This module acts as the **single source of truth for live environmental data**.

---

## 📁 Module Structure

streaming/
├── init.py
├── data_source.py
├── ingestion.py
├── processor.py
├── test_ingestion.py
└── README.md


> Note: `.venv/` and `__pycache__/` are intentionally ignored using `.gitignore`.

---

## 📄 File-by-File Breakdown

### 🔹 `data_source.py`
**Purpose:**  
Simulates live environmental sensor data such as AQI and pollution metrics.

**Why it exists:**  
- Enables real-time behavior without relying on external APIs  
- Makes the system stable, reproducible, and demo-safe  

**Role Mapping:**  
- Live data simulation  
- Streaming data source

---

### 🔹 `ingestion.py`
**Purpose:**  
Handles continuous ingestion of real-time environmental data.

**Key Characteristics:**  
- Streaming-first design  
- No batch jobs  
- Designed to run continuously during demos  

**Role Mapping:**  
- Real-time ingestion  
- Data pipeline entry point

---

### 🔹 `processor.py`
**Purpose:**  
Processes incoming data into structured, downstream-ready formats.

**Current Responsibilities:**  
- Clean and validate incoming records  
- Prepare structured outputs  
- Ready for extension with:
  - rolling averages
  - severity classification
  - alert thresholds

**Role Mapping:**  
- Real-time data processing  
- Bridge between raw data and intelligence layers

---

### 🔹 `test_ingestion.py`
**Purpose:**  
Validates the ingestion pipeline logic.

**Why it matters:**  
- Demonstrates engineering discipline  
- Ensures correctness in streaming scenarios  

---

## 🔄 End-to-End Data Flow

data_source.py
↓
ingestion.py
↓
processor.py
↓
Structured live data → RAG / Alerts / API / Dashboard


---

## 🔌 Integration Contracts

### 🔹 For RAG / LLM Team
- Consume processed environmental data
- No need to handle raw sensors
- Always receives fresh, streaming data

### 🔹 For Backend / API Team
- Can expose processed data via REST or WebSockets
- No batch synchronization required

### 🔹 For Frontend / Dashboard Team
- Can visualize live AQI and pollution metrics
- Safe to poll or subscribe

> Other modules depend on this streaming pipeline.

---

## ▶️ How to Run Locally

```bash
python ingestion.py

