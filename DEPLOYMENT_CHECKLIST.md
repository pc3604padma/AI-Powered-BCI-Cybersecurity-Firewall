# 📋 SYNORA Deployment Checklist

**Built by Padmanathan and Oviya**

---

## Pre-Deployment Verification

### Code Quality
- [ ] Run syntax check: `python -m py_compile app.py database.py auth.py`
- [ ] No import errors: `python -c "import streamlit; import pymongo; import tensorflow"`
- [ ] No missing dependencies in `requirements.txt`
- [ ] All secret keys use environment variables (no hardcoded secrets)
- [ ] Logging enabled and configured
- [ ] Error handling in place for MongoDB operations

### Testing
- [ ] Test MongoDB connection: `python test_mongodb.py`
- [ ] Test login functionality (create account, login)
- [ ] Test scan functionality (run full scan)
- [ ] Test history retrieval (scan appears in history tab)
- [ ] Test accuracy is between 0-99.9% (not 100%)
- [ ] Test statistics calculations
- [ ] Test all tabs (Dashboard, Scan, History, Statistics, Explainable AI, Research)

### Data
- [ ] MongoDB is accessible and running
- [ ] Database 'synora' exists (or will be created)
- [ ] Sample EEG data is in `data/processed/` directory
- [ ] LSTM model is trained and saved to `models/lstm_autoencoder.h5`

### Documentation
- [ ] README.md is up to date
- [ ] DEPLOYMENT_GUIDE.md is complete
- [ ] QUICK_START.md is accurate
- [ ] Environment variables documented in `.env.example`
- [ ] API endpoints documented (if applicable)

---

## Local Development Deployment

### Setup
- [ ] Python 3.10+ installed
- [ ] Virtual environment created: `python -m venv bci_env`
- [ ] Virtual environment activated: `source bci_env/bin/activate` (macOS/Linux) or `bci_env\Scripts\activate.bat` (Windows)
- [ ] Dependencies installed: `pip install -r requirements.txt`

### MongoDB Setup
- [ ] MongoDB installed locally
- [ ] MongoDB started: `mongod` (or `mongod.exe` on Windows)
- [ ] MongoDB connection verified: `mongo --eval "db.adminCommand('ping')"`
- [ ] Optional: MongoDB Compass installed for GUI management

### Application Testing
- [ ] Start app: `streamlit run app.py`
- [ ] Access at: `http://localhost:8501`
- [ ] Complete login/signup flow
- [ ] Run a scan
- [ ] Verify scan appears in MongoDB
- [ ] Check History tab loads data
- [ ] Verify accuracy display

### Pre-Production Checks
- [ ] Enable production logging: `LOG_LEVEL=INFO` environment variable
- [ ] Configure session timeout: `SESSION_TIMEOUT=3600`
- [ ] Set max login attempts: `MAX_LOGIN_ATTEMPTS=5`
- [ ] Test password reset flow (if implemented)

---

## Docker Deployment

### Prerequisites
- [ ] Docker installed: `docker --version`
- [ ] Docker Compose installed: `docker-compose --version`
- [ ] MongoDB image available: `docker pull mongo:7.0`

### Build & Deploy
- [ ] Build image: `docker build -t synora:latest .`
- [ ] Test local image: `docker run -p 8501:8501 synora:latest`
- [ ] Image runs without errors
- [ ] Port 8501 is accessible

### Docker Compose
- [ ] `docker-compose.yml` is configured
- [ ] MongoDB volume exists: `docker volume create mongodb_data`
- [ ] Start stack: `docker-compose up -d`
- [ ] Verify all services running: `docker-compose ps`
  - [ ] app: running
  - [ ] mongodb: running
  - [ ] mongo-express: running (optional)
- [ ] Access app: `http://localhost:8501`
- [ ] MongoDB data persists after restart

### Cleanup
- [ ] Test graceful shutdown: `docker-compose down`
- [ ] Verify volumes preserved: `docker volume ls | grep mongodb`
- [ ] Test restart: `docker-compose up -d`

---

## Heroku Deployment

### Prerequisites
- [ ] Heroku CLI installed: `heroku --version`
- [ ] Logged into Heroku: `heroku login`
- [ ] Git repository initialized: `git status`
- [ ] All changes committed: `git status` shows nothing
- [ ] MongoDB Atlas account created and cluster ready

### Setup
- [ ] Create Heroku app: `heroku create synora-app`
- [ ] Add MongoDB URI: `heroku config:set MONGODB_URI="mongodb+srv://..."`
- [ ] Add environment: `heroku config:set ENVIRONMENT=production`
- [ ] Configure other vars: `heroku config:set SESSION_TIMEOUT=1800`
- [ ] Verify config: `heroku config`

### Deployment
- [ ] Push to Heroku: `git push heroku main`
- [ ] Build completes without error
- [ ] Dyno starts successfully
- [ ] View logs: `heroku logs --tail` (no critical errors)
- [ ] App responsive: `heroku open`

### Testing
- [ ] Login works
- [ ] Can run scan
- [ ] Data persists in MongoDB Atlas
- [ ] History tab shows previous scans
- [ ] Accuracy displays correctly

### Maintenance
- [ ] Monitor dyno usage: `heroku ps`
- [ ] Check resource usage: `heroku apps:info`
- [ ] Setup alerts for errors
- [ ] Configure auto-dyno scaling (if needed)

---

## AWS EC2 Deployment

### Infrastructure Setup
- [ ] EC2 instance running (Ubuntu 22.04 LTS, t3.medium+)
- [ ] Security group configured:
  - [ ] Port 22 (SSH) from your IP
  - [ ] Port 80 (HTTP)
  - [ ] Port 443 (HTTPS)
  - [ ] Port 8501 (Streamlit - if not behind proxy)
  - [ ] Port 27017 (MongoDB - only if self-hosted)
- [ ] Elastic IP assigned (static IP)
- [ ] DNS/Domain pointing to instance

### Environment Setup
- [ ] SSH access verified: `ssh -i key.pem ubuntu@instance-ip`
- [ ] System updated: `sudo apt-get update && sudo apt-get upgrade -y`
- [ ] Python 3.10+ installed
- [ ] MongoDB installed (if not using managed service)
- [ ] Nginx installed as reverse proxy
- [ ] SSL certificate obtained (Let's Encrypt)

### Application Deployment
- [ ] Repository cloned to `/var/www/`
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Systemd service file created: `/etc/systemd/system/synora.service`
- [ ] Service enabled: `sudo systemctl enable synora`
- [ ] Service started: `sudo systemctl start synora`
- [ ] Service status healthy: `sudo systemctl status synora`

### Reverse Proxy (Nginx)
- [ ] Nginx config created: `/etc/nginx/sites-available/synora`
- [ ] Site enabled: `sudo ln -s /etc/nginx/sites-available/synora /etc/nginx/sites-enabled/`
- [ ] Nginx syntax valid: `sudo nginx -t`
- [ ] Nginx restarted: `sudo systemctl restart nginx`
- [ ] SSL configured with certbot
- [ ] HTTPS redirect functional

### Monitoring
- [ ] View application logs: `sudo journalctl -u synora -f`
- [ ] Check service status: `sudo systemctl status synora`
- [ ] Monitor disk space: `df -h`
- [ ] Monitor memory: `free -h`
- [ ] Monitor CPU: `htop`

---

## Azure App Service Deployment

### Prerequisites
- [ ] Azure CLI installed: `az --version`
- [ ] Logged into Azure: `az login`
- [ ] Subscription selected: `az account show`

### Infrastructure
- [ ] Resource group created: `az group create -n synora-rg -l eastus`
- [ ] App Service plan created: `az appservice plan create ...`
- [ ] Web app created: `az webapp create ...`
- [ ] App Service configured for Python 3.10

### Configuration
- [ ] Application settings configured:
  - [ ] MONGODB_URI
  - [ ] ENVIRONMENT
  - [ ] SESSION_TIMEOUT
- [ ] Connection strings verified (if applicable)
- [ ] Logging enabled

### Deployment
- [ ] Source code published (GitHub, ZIP, etc.)
- [ ] Deployment completed successfully
- [ ] App started: `az webapp start -n synora-app -g synora-rg`
- [ ] App accessible via `https://synora-app.azurewebsites.net`

### Troubleshooting
- [ ] Check deployment logs: `az webapp log tail -n synora-app -g synora-rg`
- [ ] Verify environment variables set correctly
- [ ] Check MongoDB connectivity from Azure

---

## Streamlit Cloud Deployment

### Prerequisites
- [ ] GitHub repository created and pushed
- [ ] Streamlit account created: https://streamlit.io
- [ ] GitHub connected to Streamlit Cloud

### Secrets Management
- [ ] `.streamlit/secrets.toml` created (local only, not committed)
- [ ] Secrets added in Streamlit Cloud dashboard:
  - [ ] `mongodb_uri`
  - [ ] `ENVIRONMENT`
- [ ] `.gitignore` includes `secrets.toml`

### Deployment
- [ ] App deployed from GitHub in Streamlit Cloud
- [ ] Deployment completed successfully
- [ ] App accessible at: `https://yourusername-synora.streamlit.app`
- [ ] No error messages in deployment logs

### Testing
- [ ] App loads without errors
- [ ] Login works
- [ ] Scan functionality works
- [ ] MongoDB connection successful
- [ ] All tabs functional

### Maintenance
- [ ] Auto-deploy enabled for main branch
- [ ] Logs monitored for errors
- [ ] Secrets rotated periodically

---

## Database (MongoDB)

### Local MongoDB
- [ ] MongoDB process running
- [ ] Connection working: `mongo --eval "db.adminCommand('ping')"`
- [ ] Database 'synora' created (auto-created on first use)
- [ ] Collections created:
  - [ ] `users`
  - [ ] `firewall_logs`
  - [ ] `sessions` (if applicable)

### MongoDB Atlas (Cloud)
- [ ] Cluster created and running
- [ ] Database user created with strong password
- [ ] Network access allowed from app servers
- [ ] Connection string obtained
- [ ] Connection string added to environment variables
- [ ] Test connection from app: `python test_mongodb.py`

### Data Backup
- [ ] Backup automated (if applicable)
- [ ] Backup tested and verified
- [ ] No sensitive data in backups

---

## Security Hardening

### Secrets Management
- [ ] All secrets in environment variables
- [ ] `.env` file in `.gitignore`
- [ ] No credentials in code
- [ ] No credentials in logs

### Access Control
- [ ] Strong database passwords set
- [ ] User authentication working
- [ ] Password hashing verified (bcrypt)
- [ ] Session management secure
- [ ] Rate limiting implemented
- [ ] CSRF protection enabled (Streamlit default)

### Encryption
- [ ] HTTPS/TLS enabled in production
- [ ] SSL certificate valid and not expired
- [ ] Database passwords hashed
- [ ] Sensitive data encrypted in transit

### Audit & Logging
- [ ] Application logging enabled
- [ ] Error logging configured
- [ ] Access logs captured
- [ ] Security events logged
- [ ] Log retention policy set
- [ ] Logs reviewed for suspicious activity

### Dependencies
- [ ] No known vulnerabilities: `pip list`
- [ ] Dependencies updated regularly
- [ ] Security patches applied
- [ ] Vulnerable packages identified and fixed

---

## Performance & Monitoring

### Monitoring Setup
- [ ] Application monitoring enabled
- [ ] Database monitoring enabled
- [ ] Infrastructure monitoring enabled
- [ ] Error tracking configured (e.g., Sentry)
- [ ] Performance metrics collected

### Alerts
- [ ] Alert configured for high CPU usage
- [ ] Alert configured for high memory usage
- [ ] Alert configured for database connection failures
- [ ] Alert configured for application errors
- [ ] Alert configured for deployment failures

### Optimization
- [ ] Database indexes created for frequent queries
- [ ] Query performance verified
- [ ] Response times acceptable (<2s)
- [ ] Caching implemented (if applicable)
- [ ] Static assets optimized

---

## Documentation

### User Documentation
- [ ] User guide up to date
- [ ] Screenshot/videos included
- [ ] Troubleshooting guide complete
- [ ] FAQ documented

### Deployment Documentation
- [ ] Deployment procedures documented
- [ ] Configuration documented
- [ ] Environment variables documented
- [ ] Backup/restore procedures documented
- [ ] Disaster recovery plan documented

### Code Documentation
- [ ] Key functions documented with docstrings
- [ ] Architecture documented
- [ ] API endpoints documented (if applicable)
- [ ] Database schema documented

---

## Post-Deployment

### Verification
- [ ] All features tested in production
- [ ] Data integrity verified
- [ ] Performance acceptable
- [ ] No critical errors in logs
- [ ] User access verified

### Communication
- [ ] Users notified of deployment
- [ ] Support team briefed
- [ ] Known issues documented
- [ ] Rollback plan prepared

### Ongoing
- [ ] Monitor for errors 24hr after deployment
- [ ] Respond to user feedback
- [ ] Track performance metrics
- [ ] Plan maintenance window if needed

---

## Rollback Plan

If issues occur post-deployment:

1. [ ] Identify issue and severity
2. [ ] Assess if rollback needed
3. [ ] Backup current state
4. [ ] Execute rollback:
   - **Docker**: `docker-compose down && git checkout previous-tag && docker-compose up`
   - **Heroku**: `heroku releases && heroku rollback v<number>`
   - **AWS**: Redeploy from last known good commit
   - **Azure**: Use deployment slots to switch
5. [ ] Notify affected users
6. [ ] Root cause analysis
7. [ ] Plan corrective action

---

## Final Checklist

- [ ] All items above completed
- [ ] Team approval obtained
- [ ] Backup verified
- [ ] Monitoring active
- [ ] Support team ready
- [ ] Users notified
- [ ] Rollback plan ready

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |
| DevOps | | | |
| Manager | | | |

---

**Deployment Date**: _______________

**Deployment Time**: _______________

**Status**: _______________

**Notes**: 

___________________________________________________________________

___________________________________________________________________

___________________________________________________________________

---

**© 2024 SYNORA - AI Cybersecurity for Brain Interfaces**
