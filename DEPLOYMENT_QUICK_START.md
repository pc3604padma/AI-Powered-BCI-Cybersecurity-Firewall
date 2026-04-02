# 🚀 SYNORA Deployment - Quick Reference Card

**Built by Padmanathan and Oviya**

---

## Start Here 👇

### 🏠 Local Development (Windows)
```bash
setup.bat
streamlit run app.py
# Access: http://localhost:8501
```

### 🏠 Local Development (macOS/Linux)
```bash
source bci_env/bin/activate
pip install -r requirements.txt
streamlit run app.py
# Access: http://localhost:8501
```

### 🐳 Docker
```bash
docker-compose up -d
# Access: http://localhost:8501
# MongoDB: http://localhost:8081
```

### ☁️ Heroku
```bash
heroku create synora-app
heroku config:set MONGODB_URI="mongodb+srv://..."
git push heroku main
heroku open
```

### ☁️ Streamlit Cloud
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" → Select your repo
4. Add secrets in Streamlit Cloud dashboard

---

## ⚡ Quick Commands

| Task | Command |
|------|---------|
| **Test MongoDB** | `python test_mongodb.py` |
| **Check syntax** | `python -m py_compile app.py database.py` |
| **View logs (Docker)** | `docker-compose logs -f app` |
| **View logs (Heroku)** | `heroku logs --tail` |
| **List dependencies** | `pip list` |
| **Update deps** | `pip install -r requirements.txt --upgrade` |
| **Build Docker image** | `docker build -t synora .` |
| **Stop Docker** | `docker-compose down` |
| **Restart Heroku app** | `heroku restart` |

---

## 📂 Key Files

```
requirements.txt ..................... Python dependencies
.streamlit/config.toml .............. App configuration
.env.example ......................... Environment variables template
Dockerfile ........................... Container image definition
docker-compose.yml .................. Local deployment (3 services)
Procfile ............................ Heroku deployment config
setup.sh ............................ Heroku initialization
setup.py ............................ Python package metadata
test_mongodb.py ..................... Database diagnostics
```

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **DEPLOYMENT_GUIDE.md** | How to deploy (6 platforms) |
| **DEPLOYMENT_CHECKLIST.md** | Pre/post deployment verification |
| **TROUBLESHOOTING_FAQ.md** | Problem solving & FAQs |
| **DEPLOYMENT_FILES_INDEX.md** | This file explanation |
| **QUICK_START.md** | Getting started (existing) |

---

## 🔐 Environment Variables

Create `.env` file:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
MONGODB_URI=mongodb://localhost:27017/
ENVIRONMENT=development
SESSION_TIMEOUT=3600
LOG_LEVEL=INFO
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **MongoDB won't connect** | `mongod` (start MongoDB) then `python test_mongodb.py` |
| **Port 8501 in use** | `streamlit run app.py --server.port 8502` |
| **Import errors** | `pip install -r requirements.txt` |
| **Docker won't build** | `docker build -t synora . --no-cache` |
| **Heroku deployment fails** | `heroku logs --tail` to see errors |

---

## 📊 Deployment Comparison

| Platform | Setup Time | Cost | Scalability |
|----------|-----------|------|-------------|
| **Local** | 5 min | Free | Low |
| **Docker** | 10 min | Free | Medium |
| **Streamlit Cloud** | 5 min | Free-$5/mo | Medium |
| **Heroku** | 10 min | $7-50/mo | High |
| **AWS EC2** | 20 min | $10-100+/mo | Very High |
| **Azure App** | 15 min | $10-100+/mo | Very High |

---

## ✅ Pre-Deployment Checklist

- [ ] `python test_mongodb.py` passes
- [ ] `streamlit run app.py` runs without errors
- [ ] All tests pass: `python -c "import streamlit; import pymongo; import tensorflow"`
- [ ] `.env` configured with correct MongoDB URI
- [ ] Read DEPLOYMENT_CHECKLIST.md
- [ ] Backup existing data (if applicable)
- [ ] Have rollback plan ready

---

## 🚨 Common Issues

### ❌ "MongoDB connection refused"
```bash
mongod  # Start MongoDB
# Then run:
python test_mongodb.py
```

### ❌ "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
# Verify:
python -c "import streamlit; print(streamlit.__version__)"
```

### ❌ "App crashes on login"
```bash
# Verify auth.py syntax
python -m py_compile auth.py
# Check bcrypt
python -c "import bcrypt; print(bcrypt.__version__)"
```

### ❌ "Docker container can't reach MongoDB"
```bash
# In app, use service name:
MONGODB_URI=mongodb://mongodb:27017/
# NOT localhost!
```

---

## 🎯 Deployment Paths

### Path 1: Test Locally First
```
1. setup.bat (Windows) or setup.sh (Linux)
2. streamlit run app.py
3. Test manually (login, scan, history)
4. Read DEPLOYMENT_CHECKLIST.md
5. Choose platform (2-5 below)
```

### Path 2: Docker (Recommended for testing)
```
1. docker-compose up
2. Test at http://localhost:8501
3. Review docker-compose.yml
4. Push to Docker Hub (optional)
5. Deploy to server with: docker-compose up -d
```

### Path 3: Streamlit Cloud (Easiest)
```
1. Push to GitHub
2. Go to streamlit.io/cloud
3. Click "New app"
4. Select your repo → app.py
5. Add MongoDB URI in Secrets
6. Done! App deploys automatically
```

### Path 4: Heroku (Production-grade, $7+/mo)
```
1. heroku login
2. heroku create synora-app
3. heroku config:set MONGODB_URI="..."
4. git push heroku main
5. heroku open
```

### Path 5: AWS/Azure (Most control, $10+/mo)
```
1. See DEPLOYMENT_GUIDE.md for full steps
2. Launch EC2/App Service
3. Clone repository
4. pip install -r requirements.txt
5. Configure systemd service
6. Start application
```

---

## 📞 Support Resources

1. **Check existing docs**: All `.md` files in root
2. **Database issues**: `python test_mongodb.py`
3. **Application errors**: Check Streamlit logs
4. **Docker issues**: `docker-compose logs -f`
5. **Heroku issues**: `heroku logs --tail`
6. **See TROUBLESHOOTING_FAQ.md** for 30+ solutions

---

## 🎓 Learning Resources

- **Streamlit**: https://docs.streamlit.io/
- **MongoDB**: https://docs.mongodb.com/
- **Docker**: https://docs.docker.com/
- **Heroku**: https://devcenter.heroku.com/
- **PyMongo**: https://pymongo.readthedocs.io/

---

## 🔄 Maintenance Tasks

### Daily
- Check application logs for errors
- Monitor database size

### Weekly
- Review error logs
- Check resource usage
- Update security patches

### Monthly
- Update requirements.txt: `pip list --outdated`
- Backup MongoDB data
- Review user feedback
- Test disaster recovery

### Quarterly
- Full security audit
- Performance optimization
- Dependency updates
- Documentation review

---

## 📈 Success Metrics (Post-Deployment)

- ✅ App loads in <3 seconds
- ✅ Login/signup works reliably
- ✅ Scans complete in <10 seconds
- ✅ History displays accurately
- ✅ Accuracy shows 0-99.9% range
- ✅ MongoDB logs persist correctly
- ✅ No critical errors in logs
- ✅ User reports positive feedback

---

## 🎯 Next Steps

1. **Choose your deployment platform**
2. **Follow the guide for that platform** (see DEPLOYMENT_GUIDE.md)
3. **Complete pre-deployment checklist** (see DEPLOYMENT_CHECKLIST.md)
4. **Deploy to staging first** (test in safe environment)
5. **Monitor logs post-deployment** (24 hours minimum)
6. **Perform user acceptance testing**
7. **Deploy to production**
8. **Monitor production environment** (ongoing)

---

## 🚀 Ready to Deploy?

1. Read **DEPLOYMENT_GUIDE.md** for your platform
2. Complete **DEPLOYMENT_CHECKLIST.md**
3. Use **TROUBLESHOOTING_FAQ.md** if issues arise
4. Reference **DEPLOYMENT_FILES_INDEX.md** for file explanations

---

**Status**: ✅ PRODUCTION-READY

**Last Updated**: April 2024

**Built by Padmanathan and Oviya**  
**© 2024 SYNORA - AI Cybersecurity for Brain Interfaces**
