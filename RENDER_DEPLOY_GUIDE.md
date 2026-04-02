# Render Deployment Configuration for Streamlit

## Step-by-Step Deployment

### 1. **Prerequisites**
- GitHub account with repo pushed
- Render account (https://render.com)
- MongoDB Atlas account OR use Render's managed MongoDB

### 2. **Create Render Services**

#### Option A: MongoDB on Render
```yaml
# Done in render.yaml - Render will provision MongoDB

MONGODB_URI=mongodb://synora-mongodb:27017/
MONGODB_DB=synora
```

#### Option B: MongoDB Atlas (Recommended)
1. Create free cluster at https://cloud.mongodb.com
2. Get connection string: `mongodb+srv://user:pass@cluster.mongodb.net/synora`
3. Add to Render environment:
   ```
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/synora?retryWrites=true&w=majority
   MONGODB_DB=synora
   ```

### 3. **Deploy Web Service**

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Select your GitHub repo
4. Configure:
   - **Name**: `synora-bci-firewall`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --logger.level warning`
   - **Plan**: Standard (or Starter)

5. Add environment variables:
   ```
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_LOGGER_LEVEL=warning
   MONGODB_URI=<your_mongodb_uri>
   MONGODB_DB=synora
   ```

6. Click **"Create Web Service"** → Wait 5-10 minutes for deployment

### 4. **Health Check Configuration**

Render will automatically use:
- **Health Check Path**: `/_stcore/health`
- **Check Interval**: 10s
- **Timeout**: 5s

### 5. **Auto-Deploy on Push**

Render automatically redeploys when you push to GitHub:
```bash
git add .
git commit -m "Deployment optimization for Render"
git push origin main  # Auto-triggers Render rebuild
```

### 6. **Monitoring**

View live logs:
- Render Dashboard → **Logs** tab
- Watch deployment progress in real-time

### 7. **Cost Optimization**

| Plan | Monthly | Best For |
|------|---------|----------|
| **Starter** | Free | Testing/Demo |
| **Standard** | $12 | Production |
| **Pro** | $25+ | High traffic |

**Recommended**: Start with Standard Plan for better performance.

---

## Performance on Render

### Expected Load Times
- **Cold start** (first request): 15-20s (Streamlit startup)
- **Warm start** (subsequent requests): <2s (with caching)
- **Rebuild on push**: 3-5 minutes (docker build + deployment)

### Render Advantages
✅ Free SSL/TLS certificate  
✅ Auto-scaling (Pro plan)  
✅ GitHub auto-deploy  
✅ No inactive instance spin-down (paid plans)  
✅ Native PostgreSQL/MySQL support  

### Render Limitations
⚠️ Starter plan goes to sleep after 15 min inactivity  
⚠️ No GPU (for ML models, but TensorFlow CPU is fine)  
⚠️ 0.5GB RAM on Starter (upgrade to Standard for 2GB)  

---

## Troubleshooting

### Issue: "Port not accessible"
**Fix**: Ensure `--server.port $PORT` uses Render's dynamic port

### Issue: "MongoDB connection failed"
**Fix**: 
1. Check MongoDB URI in environment variables
2. Whitelist Render IP in MongoDB Atlas (use 0.0.0.0/0 for simplicity)
3. Test connection: `python -c "from pymongo import MongoClient; print(MongoClient('<URI>'))"`

### Issue: "App crashes after deployment"
**Fix**:
1. Check logs: `render.com → Logs`
2. Ensure all dependencies in `requirements.txt`
3. Verify model files exist: `models/lstm_autoencoder.h5`

### Issue: "Slow startup on Render"
**Solution**:
- Streamlit is already optimized with caching
- Use **Standard Plan** (2GB RAM vs 0.5GB Starter)
- Pre-warm with simple dashboard on startup

---

## Deployment Checklist ✅

- [ ] `requirements.txt` updated with all packages
- [ ] `models/lstm_autoencoder.h5` committed to repo
- [ ] Environment variables configured in Render dashboard
- [ ] MongoDB connection tested locally
- [ ] `.streamlit/config.toml` optimized (done)
- [ ] `.gitignore` excludes `bci_env/`, `logs/`, pycache
- [ ] Latest code pushed to GitHub
- [ ] Render service created and logs checked
- [ ] App accessible at `https://<service-name>.onrender.com`

---

## Next Steps

1. Push this config to GitHub:
   ```bash
   git add render.yaml RENDER_DEPLOY_GUIDE.md
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. Go to https://render.com/dashboard
3. Create new Web Service from GitHub repo
4. Select Python environment
5. Set build/start commands (see above)
6. Add MongoDB URI to environment
7. Deploy!

Your app will be live at: `https://<synora-bci-firewall>.onrender.com`

---
**Optimized for**: Render Platform  
**Streamlit Version**: 1.39.0  
**Python**: 3.10  
**Last Updated**: April 2, 2026
