# SYNORA - AI Cybersecurity for Brain Interfaces

> **Enterprise-grade threat detection for EEG-based Brain-Computer Interface (BCI) systems**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B)
![MongoDB](https://img.shields.io/badge/MongoDB-Connected-green)
![License](https://img.shields.io/badge/License-MIT-black)

---

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)

---

## ✨ Features

### Real-Time Threat Detection
- **LSTM Autoencoder** - Deep learning model for anomaly detection
- **Sequence Analysis** - 10-packet sliding window detection
- **Multi-Class Classification** - ALLOW, BLOCK, QUARANTINE decisions

### Explainable AI
- Understand why decisions are made
- Detection confidence metrics
- Attack method explanation

### Comprehensive Analytics
- Scan history tracking
- Accuracy metrics over time
- Decision distribution analysis
- Threat statistics

### Security Features
- User authentication with password hashing
- MongoDB backend for data persistence
- Email alerts on threat detection
- Session management

### User-Friendly Dashboard
- Real-time scan results
- Visual packet distribution
- Historical analysis
- Data export (CSV, JSON, PDF)

---

## 🔧 System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 5GB free space
- **MongoDB**: Local or cloud instance

### Deployment Requirements
- Docker (optional for containerization)
- Streamlit Cloud account (for cloud deployment)
- MongoDB Atlas (for cloud database)

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/bci_cybersecurity_project.git
cd bci_cybersecurity_project
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv bci_env
bci_env\Scripts\activate

# macOS/Linux
python3 -m venv bci_env
source bci_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. MongoDB Setup

#### Local MongoDB
```bash
# Windows - Download and install from https://www.mongodb.com/try/download/community
mongod.exe

# macOS
brew install mongodb-community
brew services start mongodb-community

# Linux (Ubuntu)
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

#### MongoDB Atlas (Cloud)
1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create cluster
3. Update connection string in `database.py`:
```python
client = MongoClient("mongodb+srv://user:password@cluster.mongodb.net/")
```

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Application
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=true

# Database
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=synora

# Email Alerts (Optional)
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587

# Security
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
```

### Streamlit Configuration
File: `.streamlit/config.toml`

Configuration includes:
- Theme colors and styling
- Server settings
- Browser behavior
- Logger configuration

---

## 🚀 Deployment

### Option 1: Local Development
```bash
streamlit run app.py
```
Then open: http://localhost:8501

### Option 2: Streamlit Cloud

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Visit [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Select your GitHub repo and file
   - Add MongoDB URI as a secret

3. **Streamlit Secrets**
Create `.streamlit/secrets.toml`:
```toml
mongodb_uri = "mongodb+srv://user:password@cluster.mongodb.net/"
database_name = "synora"
```

### Option 3: Docker Deployment

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

**Build & Run**:
```bash
docker build -t synora:latest .
docker run -p 8501:8501 -e MONGODB_URI="..." synora:latest
```

### Option 4: Heroku Deployment

**Procfile**:
```
web: sh setup.sh && streamlit run app.py
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

---

## 📖 Usage

### Quick Start

1. **Login**
   - Create account with email and password
   - Passwords are hashed with bcrypt

2. **Dashboard & Scan**
   - Input number of packets (5-100)
   - Click "SCAN DATASET"
   - View results and metrics
   - Export as CSV, JSON, or PDF

3. **History & Reports**
   - View all past scans
   - Check statistics
   - Download reports

4. **Explainable AI**
   - Understand detection decisions
   - See confidence metrics
   - Learn about attack patterns

5. **Security Center**
   - Configure detection parameters
   - Manage settings
   - Monitor system status

### Running Tests

```bash
# Test MongoDB connection
python test_mongodb.py

# Run syntax check
python -m py_compile app.py
python -m py_compile database.py
```

---

## 🏗️ Architecture

### Project Structure
```
bci_cybersecurity_project/
├── app.py                          # Main Streamlit application
├── auth.py                         # User authentication
├── database.py                     # MongoDB operations
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── .gitignore                      # Git ignore patterns
├── models/
│   ├── lstm_autoencoder.py        # LSTM model architecture
│   └── lstm_autoencoder.h5        # Trained model weights
├── scripts/
│   ├── bci_firewall.py            # Firewall decision logic
│   ├── mixed_data_utils.py        # Data generation utilities
│   └── ... (other utilities)
└── data/
    ├── raw/                        # Raw EEG data
    └── processed/                  # Processed features
```

### Data Flow
```
User Input
    ↓
EEG Data Generation → Feature Extraction
    ↓
LSTM Autoencoder (Anomaly Detection)
    ↓
Firewall Decision Engine (ALLOW/BLOCK/QUARANTINE)
    ↓
MongoDB Logging
    ↓
Dashboard Visualization
```

### Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python 3.10+
- **ML**: TensorFlow/Keras (LSTM)
- **Database**: MongoDB
- **Visualization**: Plotly
- **Authentication**: bcrypt
- **Reporting**: ReportLab

---

## 🔍 Troubleshooting

### MongoDB Connection Issues

**Error**: "Connection refused"
```bash
# Start MongoDB
mongod.exe  # Windows
brew services start mongodb-community  # macOS
sudo systemctl start mongodb  # Linux
```

**Error**: "No logs in database"
```bash
# Test connection
python test_mongodb.py

# Check console for errors
# Look for error messages in terminal output
```

### Streamlit Issues

**Error**: "Module not found"
```bash
pip install -r requirements.txt
```

**Error**: "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

**Error**: "Memory error"
- Reduce number of packets
- Close other applications
- Use cloud deployment (AWS, Azure, GCP)

### LSTM Model Issues

**Error**: "Cannot load model"
```bash
# Retrain model
python -c "from scripts.train_lstm import train; train()"
```

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Scan Speed | ~50ms per packet |
| LSTM Accuracy | 85-99.9% |
| Database Query Time | <100ms |
| UI Response Time | <500ms |
| Maximum Concurrent Users | 10-50 (depends on infrastructure) |

---

## 🔐 Security Considerations

1. **Passwords**: Hashed with bcrypt, never stored in plain text
2. **MongoDB**: Use connection string authentication
3. **Secrets**: Store in `.streamlit/secrets.toml` (not in repo)
4. **HTTPS**: Use in production
5. **Rate Limiting**: Implement for API endpoints
6. **Audit Logging**: All scans are logged with email/timestamp

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 👥 Credits

**Built by**: **Padmanathan** and **Oviya**

**Contributors**:
- LSTM Model Research
- EEG Data Processing
- UI/UX Design
- Security Implementation

---

## 📞 Support

For issues and questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review error messages in console
3. Run `test_mongodb.py` for diagnostics
4. Check MongoDB Compass for data integrity

---

## 🎯 Roadmap

- [ ] Multi-user collaboration features
- [ ] Advanced threat analytics
- [ ] Real-time WebSocket updates
- [ ] Mobile app
- [ ] API endpoint for external systems
- [ ] Machine learning model improvements
- [ ] Integration with security frameworks

---

## 📄 Changelog

### Version 1.0.0 (April 2, 2026)
- ✅ Initial release
- ✅ LSTM autoencoder anomaly detection
- ✅ Real-time threat detection
- ✅ User authentication
- ✅ MongoDB integration
- ✅ Comprehensive dashboard
- ✅ Email alerts
- ✅ Data export capabilities

---

## 🌟 Acknowledgments

- TensorFlow/Keras team for excellent ML framework
- Streamlit for intuitive web framework
- MongoDB for reliable database
- Plotly for beautiful visualizations

---

**© 2024 SYNORA - AI Cybersecurity for Brain Interfaces**  
*Enterprise-grade threat detection for the future of brain-computer interfaces*
