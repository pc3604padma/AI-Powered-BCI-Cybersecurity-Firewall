# 🆘 SYNORA Troubleshooting & FAQs

**Built by Padmanathan and Oviya**

---

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [MongoDB Connection](#mongodb-connection)
3. [Application Errors](#application-errors)
4. [Performance Issues](#performance-issues)
5. [Docker Issues](#docker-issues)
6. [Deployment Issues](#deployment-issues)
7. [FAQ](#faq)

---

## Installation Issues

### ❌ "Python not found"

**Problem**: `Python not found` or `python: command not found`

**Solutions**:
1. **Install Python**
   - Windows: Download from https://www.python.org/downloads/
   - macOS: `brew install python3`
   - Linux: `sudo apt-get install python3 python3-pip`

2. **Add Python to PATH** (Windows)
   - During installation, check "Add Python to PATH"
   - Or manually add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python310`

3. **Verify Installation**
   ```bash
   python --version  # or python3 --version
   ```

---

### ❌ "Virtual environment won't activate"

**Problem**: `bci_env\Scripts\activate.bat` doesn't work

**Solutions**:
1. **Windows - Use .bat file**
   ```bash
   bci_env\Scripts\activate.bat
   ```

2. **Windows - Use PowerShell**
   ```powershell
   bci_env\Scripts\Activate.ps1
   # If error about execution policy:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **macOS/Linux - Use source**
   ```bash
   source bci_env/bin/activate
   ```

4. **Recreate environment if broken**
   ```bash
   rm -rf bci_env
   python3 -m venv bci_env
   source bci_env/bin/activate
   ```

---

### ❌ "pip install fails"

**Problem**: `ERROR: Could not install packages` during `pip install -r requirements.txt`

**Solutions**:
1. **Upgrade pip**
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Clear pip cache**
   ```bash
   pip cache purge
   pip install -r requirements.txt
   ```

3. **Install packages individually to identify problematic one**
   ```bash
   pip install streamlit==1.39.0
   pip install pandas==2.2.3
   # etc...
   ```

4. **Check system dependencies** (especially for numpy, tensorflow)
   - macOS: `brew install openblas` (for numpy)
   - Linux: `sudo apt-get install libatlas-base-dev`

5. **Use pre-built wheels**
   ```bash
   pip install --only-binary :all: -r requirements.txt
   ```

---

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Problem**: Import error after pip install

**Solutions**:
1. **Verify virtual environment is activated**
   ```bash
   which python  # Should show path to venv
   ```

2. **Verify package is installed**
   ```bash
   pip list | grep streamlit
   ```

3. **Install package explicitly**
   ```bash
   pip install streamlit==1.39.0
   ```

4. **Check for multiple Python installations**
   ```bash
   where python  # Shows all Python executables
   # Use the correct one in PATH
   ```

---

## MongoDB Connection

### ❌ "MongoDB connection refused"

**Problem**: `Error: connect ECONNREFUSED 127.0.0.1:27017`

**Solutions**:
1. **Start MongoDB**
   ```bash
   mongod  # or mongod.exe on Windows
   ```

2. **Verify MongoDB is running**
   ```bash
   mongo --eval "db.adminCommand('ping')"
   # Should return: { ok: 1 }
   ```

3. **Check MongoDB port**
   ```bash
   # Windows
   netstat -ano | findstr :27017
   
   # macOS/Linux
   lsof -i :27017
   ```

4. **Change MongoDB port in code**
   ```python
   # In database.py
   client = MongoClient("mongodb://localhost:27018/")  # Change port to 27018
   ```

5. **Clear MongoDB lock file** (if corrupted)
   ```bash
   rm /var/lib/mongodb/mongod.lock  # Linux
   rm /usr/local/var/mongodb/mongod.lock  # macOS
   ```

---

### ❌ "Authentication failed for MongoDB"

**Problem**: `Error: Authentication failed`

**Solutions**:
1. **Use correct credentials**
   ```python
   # In database.py
   uri = "mongodb://username:password@localhost:27017/"
   client = MongoClient(uri)
   ```

2. **Check user exists**
   ```bash
   mongo
   > use admin
   > db.getUsers()
   ```

3. **Reset password**
   ```bash
   mongo --username admin --password
   > db.changeUserPassword("admin", "newpassword")
   ```

4. **Create user if missing**
   ```bash
   mongo
   > use admin
   > db.createUser({user:"admin", pwd:"password", roles:["root"]})
   ```

---

### ❌ "MongoDB Atlas connection fails"

**Problem**: Can't connect to cloud MongoDB

**Solutions**:
1. **Verify connection string**
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/database`
   - Get from MongoDB Atlas Dashboard → Connect

2. **Whitelist IP address**
   - Atlas Dashboard → Network Access
   - Add your IP (or 0.0.0.0/0 for testing only)

3. **Check credentials**
   - Double-check username and password in connection string
   - Use URL encoding for special characters: `@` → `%40`

4. **Test connection string**
   ```bash
   mongosh "mongodb+srv://username:password@cluster.mongodb.net/"
   ```

5. **Verify database exists**
   ```python
   from pymongo import MongoClient
   client = MongoClient("mongodb+srv://user:pass@cluster.mongodb.net/")
   print(client.list_database_names())
   ```

---

## Application Errors

### ❌ "streamlit run app.py fails to start"

**Problem**: Streamlit exits immediately with error

**Solutions**:
1. **Check for syntax errors**
   ```bash
   python -m py_compile app.py
   # If no output, syntax is OK
   ```

2. **Run with debug info**
   ```bash
   streamlit run app.py --logger.level=debug
   ```

3. **Check imports**
   ```bash
   python -c "import app"
   # Check for ImportError
   ```

4. **Increase verbosity**
   ```bash
   STREAMLIT_LOGGER_LEVEL=debug streamlit run app.py
   ```

---

### ❌ "Streamlit app crashes on login"

**Problem**: App crashes when submitting login form

**Solutions**:
1. **Check bcrypt installation**
   ```bash
   python -c "import bcrypt; print(bcrypt.__version__)"
   ```

2. **Verify auth.py syntax**
   ```bash
   python -m py_compile auth.py
   ```

3. **Test authentication directly**
   ```python
   from auth import verify_password, hash_password
   
   hashed = hash_password("testpass")
   print(verify_password("testpass", hashed))  # Should be True
   ```

4. **Check MongoDB is running**
   ```bash
   python test_mongodb.py
   ```

---

### ❌ "Accuracy always shows 0% or 100%"

**Problem**: Model accuracy not varying

**Solutions**:
1. **Check variance logic in app.py (line 209-217)**
   ```python
   # Should have:
   random_variance = np.random.uniform(-2.5, 0)
   accuracy = max(0, accuracy + random_variance)
   accuracy = min(accuracy, 99.9)
   ```

2. **Verify LSTM model is trained**
   ```bash
   ls -la models/lstm_autoencoder.h5
   # File should exist and be >1MB
   ```

3. **Check training data quality**
   - Verify `data/processed/eeg_features_labeled.csv` exists
   - Has both normal and malicious samples

4. **Reset model if needed**
   ```bash
   python train_lstm.py
   ```

---

### ❌ "NoPasswordSupplied error in MongoDB"

**Problem**: MongoDB auth error when logging in

**Solutions**:
1. **Disable authentication for testing**
   ```bash
   mongod --noauth
   ```

2. **Or use correct credentials**
   ```python
   # In database.py
   uri = "mongodb://admin:password@localhost:27017/"
   ```

3. **Check user exists**
   ```bash
   mongo
   > use admin
   > db.getUsers()
   ```

---

## Performance Issues

### ⚠️ "App is slow to load"

**Problem**: Streamlit app takes >5 seconds to load

**Solutions**:
1. **Enable caching**
   ```python
   @st.cache_data
   def load_model():
       return load_lstm_model()
   ```

2. **Use session state properly**
   ```python
   if 'model' not in st.session_state:
       st.session_state.model = load_model()
   ```

3. **Check database query performance**
   ```python
   import time
   start = time.time()
   stats = get_firewall_stats(email)
   print(f"Query took {time.time()-start:.2f}s")
   ```

4. **Add database indexes**
   ```python
   db['firewall_logs'].create_index('email')
   db['firewall_logs'].create_index('timestamp', -1)
   ```

---

### ⚠️ "Memory usage is high"

**Problem**: App consuming lots of RAM

**Solutions**:
1. **Clear session cache**
   ```python
   # Streamlit automatically clears on app rerun
   # But can manually clear:
   st.cache_data.clear()
   ```

2. **Process data in chunks** (not all at once)
   ```python
   # Don't load entire dataset at once
   df = pd.read_csv("data.csv", chunksize=1000)
   ```

3. **Monitor LSTM model memory**
   ```bash
   python -c "
   from models.lstm_autoencoder import load_model
   import psutil
   model = load_model()
   # Check current memory
   p = psutil.Process()
   print(f'Memory: {p.memory_info().rss / 1024 / 1024:.2f} MB')
   "
   ```

---

### ⚠️ "Database queries are slow"

**Problem**: History/Statistics take >2 seconds to load

**Solutions**:
1. **Add MongoDB indexes**
   ```python
   # In database.py initialization
   from pymongo import ASCENDING, DESCENDING
   
   db['firewall_logs'].create_index([('email', ASCENDING)])
   db['firewall_logs'].create_index([('timestamp', DESCENDING)])
   db['users'].create_index([('email', ASCENDING)], unique=True)
   ```

2. **Optimize aggregation pipeline**
   ```python
   # Use $match early to filter docs
   # Use projections to select only needed fields
   pipeline = [
       {"$match": {"email": user_email}},
       {"$project": {"email": 1, "accuracy": 1, "timestamp": 1}},
       {"$group": {...}}
   ]
   ```

3. **Limit results**
   ```python
   # Get last 100 scans, not all
   history = list(collection.find().limit(100).sort("timestamp", -1))
   ```

---

## Docker Issues

### ❌ "Docker build fails"

**Problem**: `docker build -t synora .` fails

**Solutions**:
1. **Check Dockerfile exists**
   ```bash
   ls -la Dockerfile
   ```

2. **Check syntax**
   ```bash
   docker build -t synora . --no-cache
   ```

3. **Common issues**
   ```dockerfile
   # Check for missing files referenced in Dockerfile
   COPY requirements.txt .  # File must exist
   
   # Check base image availability
   FROM python:3.10-slim  # Image must exist
   ```

4. **Build with verbose output**
   ```bash
   docker build -t synora . --progress=plain
   ```

---

### ❌ "docker-compose up fails"

**Problem**: `docker-compose up` exits with error

**Solutions**:
1. **Check docker-compose.yml syntax**
   ```bash
   docker-compose config
   # Shows errors if any
   ```

2. **Check volumes exist**
   ```bash
   docker volume ls | grep mongodb
   # Create if missing:
   docker volume create mongodb_data
   ```

3. **Check port conflicts**
   ```bash
   # Windows/macOS
   netstat -ano | findstr :8501
   netstat -ano | findstr :27017
   
   # Linux
   lsof -i :8501
   lsof -i :27017
   ```

4. **View detailed logs**
   ```bash
   docker-compose up
   # Don't use -d flag to see logs
   ```

---

### ⚠️ "Container can't connect to MongoDB"

**Problem**: App container can't reach MongoDB container

**Solutions**:
1. **Check docker-compose.yml links/networks**
   ```yaml
   # Should have:
   networks:
     - synora_network
   
   # And services on same network
   services:
     app:
       networks:
         - synora_network
   ```

2. **Use service name, not localhost**
   ```python
   # In app, connect to:
   # client = MongoClient("mongodb://mongodb:27017/")
   # NOT localhost
   ```

3. **Check container logs**
   ```bash
   docker logs <container_name>
   docker-compose logs mongodb
   ```

4. **Verify MongoDB is accepting connections**
   ```bash
   docker exec mongodb mongosh --eval "db.adminCommand('ping')"
   ```

---

## Deployment Issues

### ❌ "Heroku deployment fails"

**Problem**: `git push heroku main` fails

**Solutions**:
1. **Check Procfile exists**
   ```bash
   cat Procfile
   # Should have: web: sh setup.sh && streamlit run app.py ...
   ```

2. **Check setup.sh exists**
   ```bash
   cat setup.sh
   ```

3. **View build logs**
   ```bash
   heroku logs --tail
   ```

4. **Common Procfile issues**
   ```
   # WRONG - missing quotes
   web: streamlit run app.py --server.port $PORT
   
   # CORRECT - with quotes
   web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

5. **Check buildpacks**
   ```bash
   heroku buildpacks
   # Should show: heroku/python
   ```

---

### ❌ "App runs but no data displays"

**Problem**: App works but history/stats are empty

**Solutions**:
1. **Check MongoDB URI is correct**
   ```bash
   heroku config | grep MONGODB_URI
   ```

2. **Verify database exists**
   ```bash
   heroku run "python -c \"from pymongo import MongoClient; \
     c = MongoClient('$MONGODB_URI'); \
     print(c.list_database_names())\""
   ```

3. **Check logs for connection errors**
   ```bash
   heroku logs --tail
   # Look for MongoDB errors
   ```

4. **Test database directly**
   ```bash
   # Go to MongoDB Atlas Dashboard
   # Click "Connect" -> "Compass"
   # Use connection string to verify data exists
   ```

---

### ❌ "AWS EC2 deployment not working"

**Problem**: App accessible but not loading properly

**Solutions**:
1. **Check instance security group**
   - Verify port 80, 443, 8501 are open

2. **Check Nginx configuration**
   ```bash
   sudo nginx -t
   # Should show: successful
   ```

3. **Check systemd service**
   ```bash
   sudo systemctl status synora
   # Should show: active (running)
   ```

4. **View application logs**
   ```bash
   sudo journalctl -u synora -f
   # Should not show errors
   ```

5. **Restart service**
   ```bash
   sudo systemctl restart synora
   sudo systemctl restart nginx
   ```

---

## FAQ

### Q: How often should I update dependencies?

**A**: At least monthly for security patches. Check with:
```bash
pip list --outdated
```

For Streamlit/TensorFlow, only update when deployment is ready due to compatibility issues.

---

### Q: Can I use MongoDB Atlas instead of local MongoDB?

**A**: Yes! Replace connection string in `database.py`:
```python
client = MongoClient("mongodb+srv://username:password@cluster.mongodb.net/synora")
```

Get connection string from MongoDB Atlas Dashboard → Connect

---

### Q: What's the minimum server size for production?

**A**: 
- CPU: 2 cores (t3.small on AWS)
- RAM: 2GB minimum, 4GB recommended
- Storage: 10GB for MongoDB + app
- Bandwidth: Depends on users (100+ concurrent users needs larger instance)

---

### Q: How do I backup MongoDB data?

**A**: 
```bash
# Local backup
mongodump --out /backup/synora

# Local restore
mongorestore /backup/synora

# Cloud backup (Atlas handles automatically)
# But can use:
mongodump --uri "mongodb+srv://..." --out /backup
```

---

### Q: Can I run multiple instances behind a load balancer?

**A**: Yes! Use:
- Load Balancer (AWS ELB, Azure LB, Nginx)
- Shared MongoDB (single instance or MongoDB Atlas)
- Shared session storage (optional, for Streamlit cache)

---

### Q: How do I scale for thousands of users?

**A**: 
1. Use managed services (Heroku, AWS, Azure)
2. Enable auto-scaling for app servers
3. Use MongoDB Atlas for database scaling
4. Add CDN for static content
5. Implement request caching

---

### Q: Is the app HIPAA compliant?

**A**: Not by default. For HIPAA compliance:
- Enable encryption at rest and in transit
- Implement audit logging
- Use role-based access control (RBAC)
- Enable data masking
- Use BAA (Business Associate Agreement) with cloud providers
- Regular security audits

---

### Q: Can I integrate with email alerts?

**A**: Yes! File `email_alerts.py` exists. Configure:
```python
# In app.py
from email_alerts import send_alert

if malicious_count > threshold:
    send_alert(email, "Threat detected", details)
```

---

### Q: How do I add custom authentication (SSO)?

**A**: Modify `auth.py` to add:
- OAuth 2.0 integration (Google, Azure AD)
- SAML support
- LDAP integration

Example with Google OAuth:
```python
from google.oauth2 import id_token
from google.auth.transport import requests

token = request.args.get('token')
idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
email = idinfo['email']
```

---

### Q: Where are application logs stored?

**A**:
- Local: Check Streamlit logs in `~/.streamlit/logs`
- Docker: `docker logs <container_id>`
- Heroku: `heroku logs --tail`
- AWS EC2: `/var/log/synora.log` or `journalctl -u synora`
- Azure: Application Insights dashboard

---

### Q: How do I enable HTTPS locally for testing?

**A**:
```bash
# Generate self-signed cert
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Update .streamlit/config.toml
[server]
sslCertFile = "cert.pem"
sslKeyFile = "key.pem"
```

---

### Q: Can I run the app without Streamlit (e.g., as API)?

**A**: Yes, structure the logic into:
1. Backend API (Flask/FastAPI)
2. Frontend (React/Vue)
3. Database (MongoDB)

But current app.py is tightly coupled to Streamlit. Refactoring needed for full separation.

---

### Q: What's the maximum file size for EEG data uploads?

**A**: Currently limited to available RAM. To increase:
```python
# In app.py
@st.cache_resource
def upload_file():
    st.file_uploader("Upload EEG", type=['csv'], key='eeg_upload')
    # Default is 200MB in Streamlit config
```

Increase in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500  # MB
```

---

### Q: How do I debug LSTM model predictions?

**A**:
```bash
# Run prediction test
python scripts/test_anomaly_model.py

# Visualize results
python scripts/explain_firewall_decision.py

# Check model accuracy
python calibrate_threshold.py
```

---

### Q: Can I integrate with external threat intelligence feeds?

**A**: Yes! Implement in app.py:
```python
import requests

def check_threat_database(packet_hash):
    # Query external API
    response = requests.get(f"https://api.threat-feed.com/check/{packet_hash}")
    return response.json()
```

---

## Still Having Issues?

1. **Check existing logs**: Check any `.md` files in project for known issues
2. **Run diagnostics**: `python test_mongodb.py`
3. **Test independently**: Isolate the failing component
4. **Review git changes**: `git log --oneline` to see what changed
5. **Search online**: Most Python/MongoDB/Streamlit errors are well-documented
6. **Contact support**: Email to project maintainers

---

**Built by Padmanathan and Oviya**  
**© 2024 SYNORA - AI Cybersecurity for Brain Interfaces**
