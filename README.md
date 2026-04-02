# 🚀 SYNORA v2.0 - AI-Powered BCI Cybersecurity Firewall

**Built by Padmanathan and Oviya**

An intelligent anomaly detection system that monitors EEG signals in real-time to detect and block cybersecurity threats using advanced LSTM deep learning models.

---

## ⚡ Quick Start

### Local Development (Windows)
```bash
setup.bat
streamlit run app.py
# Opens at http://localhost:8501
```

### Local Development (macOS/Linux)
```bash
python -m venv bci_env
source bci_env/bin/activate  # or bci_env\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

### Docker
```bash
docker-compose up -d
# App: http://localhost:8501 | MongoDB: http://localhost:8081
```

### Cloud Deployment
- **Streamlit Cloud**: Push to GitHub → https://streamlit.io/cloud → Select repo
- **Heroku**: `heroku create synora-app` + add MONGODB_URI secret
- **AWS/Azure**: Use Docker image with container registry

> **Prerequisites**: MongoDB running locally or cloud connection string in environment

---

## 🎯 Key Features

### 1. 📊 Dashboard
- Real-time system health monitoring
- Performance metrics and statistics
- Visual status indicators

### 2. 🔍 Firewall Scanner
- Scan EEG data for anomalies
- Real-time threat detection
- Detailed decision breakdowns (ALLOW/BLOCK/QUARANTINE)

### 3. 📈 History & Reports
- Firewall scan history with timestamps
- Aggregate statistics and trends
- Export professional PDF reports
- Multi-session tracking

### 4. ⚔️ Attack Simulation
- 4 attack patterns: Random, Gradient, Persistent, Burst
- Configurable intensity (1-5 levels)
- Duration control (1-60 seconds)
- Real-time threat tracking

### 5. 🧠 AI Explainability
- Understand firewall decisions
- Feature importance visualization
- Anomaly score breakdown

### 6. ⚙️ Configuration
- Model threshold adjustment
- Database management
- System settings

---

## 📦 What's Inside

```
models/
  └── lstm_autoencoder.h5    # Pre-trained deep learning model
scripts/
  ├── bci_firewall.py        # Main firewall logic
  ├── lstm_detector.py       # Anomaly detection engine
  ├── email_alerts.py        # Security notifications
  ├── blockchain_logger.py   # Immutable audit trails
  └── extract_features.py    # EEG feature extraction
data/
  ├── raw/                   # Raw EEG signals (S001-S044+)
  └── processed/             # Extracted features
logs/                        # Scan and system logs
```

---

## 🔧 Common Commands

| Task | Command |
|------|---------|
| Run locally | `streamlit run app.py` |
| Train model | `python scripts/train_anomaly_model.py` |
| Test firewall | `python scripts/test_anomaly_model.py` |
| Start MongoDB | `mongod` (Windows) / `brew services start mongodb-community` (Mac) |
| Stop MongoDB | `mongod.exe --shutdown` (Windows) / `brew services stop mongodb-community` (Mac) |
| View logs | Logs tab in app or `logs/` directory |

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Make sure MongoDB is running
mongod              # Windows
mongod --config /usr/local/etc/mongod.conf  # macOS
sudo systemctl start mongodb  # Linux

# Verify connection
python -c "from pymongo import MongoClient; MongoClient().admin.command('ping')"
```

### Virtual Environment Issues
```bash
# Recreate environment if needed
python -m venv bci_env
bci_env\Scripts\activate        # Windows
source bci_env/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

### Streamlit Memory Error
```bash
# Run with optimized settings
streamlit run app.py --logger.level=error --client.maxMessageSize=200
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
pip install reportlab pymongo streamlit tensorflow scikit-learn pandas numpy matplotlib
```

---

## 📋 Requirements

- **Python 3.8+**
- **MongoDB** (local or Atlas)
- **TensorFlow & Keras** (LSTM model)
- **Streamlit** (UI framework)
- **Scikit-learn** (ML utilities)
- **Pandas & NumPy** (data processing)

See `requirements.txt` for complete dependency list.

---

## 🚀 Deployment Checklist

- [ ] MongoDB connection verified
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] LSTM model loaded (`models/lstm_autoencoder.h5`)
- [ ] Environment variables set (MONGODB_URI, EMAIL credentials)
- [ ] Port 8501 available
- [ ] API keys configured (for email alerts, blockchain logging)

---

## 📞 Support

- **Email**: Check EMAIL_ALERTS_SETUP.md for configuration
- **Logs**: Navigate to ⚙️ Configuration → View Logs
- **Debug**: Run tests with `python scripts/test_anomaly_model.py`

---

## 📄 License

See LICENSE file for terms.