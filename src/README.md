# Citizen Reporting System - Production-Grade Smart City Platform

A complete, real-time civic engagement platform with AI-powered issue detection using YOLO, live environmental monitoring, and WebSocket updates.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                            │
│  React 18 + Vite │ TailwindCSS │ Socket.IO Client │ Leaflet     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                  HTTPS / WebSocket
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│                     APPLICATION LAYER                            │
│  Express.js │ Socket.IO Server │ JWT Auth │ Rate Limiting       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼─────┐    ┌──────▼──────┐    ┌─────▼──────┐
│ AI/ML Layer │    │ Data Layer  │    │  External  │
│             │    │             │    │    APIs    │
│ • YOLOv8    │    │ • MongoDB   │    │ • WAQI     │
│ • OpenCV    │    │ • Redis     │    │ • Nominatim│
│ • Python    │    │ • Bull      │    │ • Weather  │
└─────────────┘    └─────────────┘    └────────────┘
```

## ✨ Key Features

### 🤖 AI-Powered Detection
- **YOLOv8 Integration**: Automatic object detection and classification
- **Real-time Analysis**: Image processing within seconds
- **Confidence Scoring**: ML confidence levels for each detection
- **Multi-class Detection**: Identifies traffic, garbage, potholes, etc.

### 🌍 Real-Time Environmental Data
- **Live AQI Monitoring**: WAQI API integration for air quality
- **Weather Context**: Temperature, humidity, pressure tracking
- **Pollutant Analysis**: PM2.5, PM10, O3, NO2, SO2, CO levels
- **30-Min Updates**: Automated cron job refreshes

### 📡 WebSocket Real-Time Updates
- **Live Issue Feed**: Instant notifications of new reports
- **City Subscriptions**: Filter by location
- **Status Updates**: Real-time resolution tracking
- **Admin Dashboard**: Live statistics and monitoring

### 📍 Geolocation Services
- **Reverse Geocoding**: Coordinates to address conversion
- **Landmark Detection**: Nearby POI identification
- **City Mapping**: Automatic location tagging
- **Distance Calculation**: Haversine formula implementation

## 🚀 Quick Start

### Prerequisites
- Node.js >= 18.0.0
- Python >= 3.8
- MongoDB >= 6.0
- Redis >= 7.0

### Backend Setup

```bash
# Navigate to backend
cd citizen-reporting-system/backend

# Install dependencies
npm install

# Install Python requirements
pip install ultralytics opencv-python numpy --break-system-packages

# Download YOLO model
cd src/ai/yolo/models
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
nano .env

# Required API Keys:
# - WAQI_API_KEY: Get from https://aqicn.org/api/
# - MONGODB_URI: Your MongoDB connection string
# - JWT_SECRET: Random secure string

# Create uploads directory
mkdir -p uploads logs

# Start MongoDB and Redis
sudo systemctl start mongod redis

# Run backend
npm run dev
```

### Frontend Setup

```bash
# Navigate to frontend
cd citizen-reporting-system/frontend

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:5000/api/v1" > .env
echo "VITE_WS_URL=http://localhost:5000" >> .env

# Run frontend
npm run dev
```

### Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api/v1
- **WebSocket**: ws://localhost:5000
- **Health Check**: http://localhost:5000/health

## 📡 API Endpoints

### Authentication
```
POST /api/v1/auth/register    - Register new user
POST /api/v1/auth/login       - User login
```

### Reports
```
POST /api/v1/report           - Submit new report (multipart/form-data)
POST /api/v1/report/analyze   - Analyze image with YOLO
GET  /api/v1/report/:id       - Get report by ID
```

### Issues
```
GET    /api/v1/issues         - Get all issues (paginated, filtered)
GET    /api/v1/issues/live    - Get live/recent issues
PATCH  /api/v1/issues/:id/status  - Update issue status (admin)
POST   /api/v1/issues/:id/upvote  - Upvote an issue
```

### AQI
```
GET  /api/v1/aqi/:city        - Get AQI for city
POST /api/v1/aqi/coordinates  - Get AQI by lat/lng
POST /api/v1/aqi/batch        - Get multiple cities AQI
```

### Analytics
```
GET /api/v1/analytics/stats   - Get statistics (filtered by city)
GET /api/v1/analytics/cities  - Get city-wise distribution
```

## 🎯 YOLO Integration Details

### Detection Flow

```
User uploads image
        ↓
Multer saves to /uploads
        ↓
YOLOService.analyzeImage(path)
        ↓
Python process spawned:
python3 detect.py --image {path} --model yolov8n.pt
        ↓
YOLO detects objects
        ↓
JSON response:
{
  "primaryClass": "car",
  "primaryConfidence": 0.87,
  "detections": [
    { "x": 100, "y": 150, "width": 200, "height": 300, 
      "class": "car", "confidence": 0.87 }
  ]
}
        ↓
Mapped to issue category
        ↓
Stored in MongoDB with confidence score
```

### YOLO Configuration

**Model**: YOLOv8n (Nano - fastest inference)
**Confidence Threshold**: 0.5 (configurable in .env)
**IOU Threshold**: 0.45 (Non-Max Suppression)

**Class Mapping**:
- Traffic objects (car, bus, truck) → `traffic` category
- Waste items (bottle, cup, bowl) → `garbage` category
- Infrastructure → `pothole`, `streetlight` categories

### Python Script (`detect.py`)

The script uses the `ultralytics` library for YOLOv8:

```python
from ultralytics import YOLO

model = YOLO(model_path)
results = model.predict(image, conf=0.5, iou=0.45)
```

Output is structured JSON for Node.js consumption.

## 🌐 Real-Time Data Sources

### WAQI (World Air Quality Index)
- **Endpoint**: `https://api.waqi.info/feed/{city}/?token={key}`
- **Update Frequency**: Every 30 minutes (cron job)
- **Cache Duration**: 30 minutes (in-memory)
- **Data Points**: AQI, PM2.5, PM10, O3, NO2, SO2, CO, weather

### Nominatim (OpenStreetMap)
- **Endpoint**: `https://nominatim.openstreetmap.org/reverse`
- **Rate Limit**: 1 request/second (automatic throttling)
- **User-Agent**: Required (set in .env)
- **Data**: Address, city, state, landmarks, POIs

## 📊 WebSocket Events

### Client → Server
```javascript
socket.emit('register', userId);
socket.emit('join_city', 'Mumbai');
socket.emit('subscribe_issue', issueId);
```

### Server → Client
```javascript
// New issue notification
socket.on('new_issue', (data) => {
  // data.type: 'NEW_ISSUE'
  // data.data: Issue object
  // data.timestamp
});

// Issue update
socket.on('issue_updated', (data) => {
  // data.type: 'ISSUE_UPDATE'
});

// AQI update
socket.on('aqi_update', (data) => {
  // data.city
  // data.data: { aqi, category, pollutants... }
});

// Notification
socket.on('notification', (data) => {
  // data.type: 'NOTIFICATION'
  // data.data.message
});
```

## 🗄️ Database Schema

### Issue Model
```javascript
{
  reporterId: ObjectId,
  title: String,
  description: String,
  category: Enum,
  
  aiAnalysis: {
    detectedClass: String,
    confidence: Number,
    boundingBoxes: Array,
    processedAt: Date
  },
  
  location: {
    type: 'Point',
    coordinates: [longitude, latitude],
    city: String,
    address: String,
    landmark: String
  },
  
  media: [{
    url: String,
    type: Enum['image', 'video']
  }],
  
  status: Enum,
  priority: Enum,
  severity: Enum,
  
  environmentalContext: {
    aqi: Number,
    aqiCategory: String,
    temperature: Number,
    humidity: Number
  },
  
  upvotes: Number,
  viewCount: Number,
  
  timestamps: true
}
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt with salt rounds
- **Rate Limiting**: 100 requests per 15 minutes
- **Helmet.js**: Security headers
- **Input Validation**: express-validator
- **File Upload Limits**: 10MB max file size
- **CORS**: Configured for specific origins

## 📈 Performance Optimizations

- **Redis Caching**: AQI data, geolocation results
- **MongoDB Indexes**: Location (2dsphere), timestamps, city+category
- **Image Optimization**: Sharp for resizing
- **Lazy Loading**: Pagination on all list endpoints
- **WebSocket Rooms**: Targeted broadcasts (city-specific)
- **Cron Job Scheduling**: Off-peak AQI updates

## 🧪 Testing

```bash
# Backend tests
cd backend
npm test

# API health check
curl http://localhost:5000/health

# Test YOLO detection
python3 src/ai/yolo/detect.py --image test.jpg --model src/ai/yolo/models/yolov8n.pt
```

## 🚀 Production Deployment

### Environment Variables (Production)
```bash
NODE_ENV=production
PORT=5000
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
REDIS_URL=redis://redis-host:6379
JWT_SECRET=secure-random-string-256-bits
WAQI_API_KEY=your-production-key
```

### PM2 Process Manager
```bash
npm install -g pm2

# Start backend
pm2 start src/server.js --name citizen-api

# Start with cluster mode
pm2 start src/server.js -i max --name citizen-api
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }

    location /socket.io {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }
}
```

## 📦 Project Structure

```
citizen-reporting-system/
│
├── backend/
│   ├── src/
│   │   ├── routes/          # API route definitions
│   │   ├── controllers/     # Request handlers
│   │   ├── services/        # Business logic
│   │   │   ├── yolo.service.js
│   │   │   ├── aqi.service.js
│   │   │   ├── geolocation.service.js
│   │   │   └── websocket.service.js
│   │   ├── models/          # MongoDB schemas
│   │   ├── middleware/      # Auth, error handling
│   │   ├── utils/           # Logger, helpers
│   │   ├── ai/yolo/         # YOLO integration
│   │   │   ├── detect.py    # Python detection script
│   │   │   └── models/      # YOLO weights
│   │   └── server.js        # Entry point
│   ├── uploads/             # User-uploaded files
│   ├── logs/                # Application logs
│   ├── package.json
│   └── .env
│
└── frontend/
    ├── src/
    │   ├── components/      # Reusable UI components
    │   ├── pages/           # Route pages
    │   ├── services/        # API, WebSocket clients
    │   ├── stores/          # Zustand state management
    │   ├── hooks/           # Custom React hooks
    │   └── App.jsx          # Main app component
    ├── public/
    ├── package.json
    └── .env
```

## 🔧 Troubleshooting

### YOLO Model Not Found
```bash
cd backend/src/ai/yolo/models
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

### Python ultralytics Not Installed
```bash
pip install ultralytics opencv-python numpy --break-system-packages
```

### MongoDB Connection Error
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod
```

### Redis Connection Error
```bash
# Check if Redis is running
sudo systemctl status redis

# Start Redis
sudo systemctl start redis
```

### WebSocket Not Connecting
- Check CORS settings in backend server.js
- Verify WS_CORS_ORIGIN in .env matches frontend URL
- Ensure port 5000 is not blocked by firewall

## 📝 License

MIT License - Production-grade open source

## 🤝 Contributing

This is a production-ready template. Fork and customize for your smart city needs.

---

Built with ❤️ for Smart Cities
```

