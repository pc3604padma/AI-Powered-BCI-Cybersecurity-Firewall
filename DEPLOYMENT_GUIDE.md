# SYNORA Deployment Guide

> Complete guide to deploy SYNORA on various platforms

**Built by Padmanathan and Oviya**

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Streamlit Cloud](#streamlit-cloud)
3. [Docker Deployment](#docker-deployment)
4. [Heroku Deployment](#heroku-deployment)
5. [AWS Deployment](#aws-deployment)
6. [Azure Deployment](#azure-deployment)
7. [Self-Hosted (Linux/Ubuntu)](#self-hosted)

---

## 🏠 Local Development

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/bci_cybersecurity_project.git
cd bci_cybersecurity_project

# 2. Create virtual environment
python -m venv bci_env
bci_env\Scripts\activate  # Windows
source bci_env/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start MongoDB
mongod.exe  # Windows
brew services start mongodb-community  # macOS
sudo systemctl start mongodb  # Linux

# 5. Run application
streamlit run app.py
```

**Access**: http://localhost:8501

---

## ☁️ Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account
- GitHub repository with your code

### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

2. **Create Streamlit Cloud Secrets**

Create `.streamlit/secrets.toml` (in project root):
```toml
mongodb_uri = "mongodb+srv://username:password@cluster.mongodb.net/"
database_name = "synora"
```

3. **Deploy on Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo and `app.py`
   - Advanced settings → Add secrets from `.streamlit/secrets.toml`

4. **Monitor Deployment**
   - View logs in Streamlit Cloud dashboard
   - Access your app at: https://yourusername-synora.streamlit.app

### Environment Variables

In Streamlit Cloud dashboard:
- Secrets Manager → Add:
  - `mongodb_uri`: Your MongoDB Atlas connection string
  - `ENVIRONMENT`: production

---

## 🐳 Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose (optional but recommended)

### Option 1: Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

**Access**:
- Application: http://localhost:8501
- MongoDB Compass: http://localhost:27017 (from local machine)
- MongoDB Express (Admin UI): http://localhost:8081

### Option 2: Manual Docker

```bash
# Build image
docker build -t synora:latest .

# Run container
docker run -p 8501:8501 \
  -e MONGODB_URI="mongodb://host.docker.internal:27017/" \
  synora:latest

# Run with MongoDB
docker run -p 27017:27017 -d --name mongodb mongo:7.0
docker run -p 8501:8501 \
  -e MONGODB_URI="mongodb://mongodb:27017/" \
  --link mongodb:mongodb \
  synora:latest
```

### Docker Hub Deployment

```bash
# Tag image
docker tag synora:latest yourusername/synora:1.0.0

# Push to Docker Hub
docker push yourusername/synora:1.0.0

# Run from Docker Hub
docker run -p 8501:8501 yourusername/synora:1.0.0
```

---

## 🚀 Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Heroku account
- MongoDB Atlas account

### Steps

1. **Create Heroku App**
```bash
heroku login
heroku create your-app-name
```

2. **Add MongoDB URI**
```bash
heroku config:set MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
heroku config:set ENVIRONMENT=production
```

3. **Deploy**
```bash
git push heroku main
```

4. **View Logs**
```bash
heroku logs --tail
```

5. **Access App**
```bash
heroku open
```

### Troubleshooting Heroku

```bash
# Check config
heroku config

# View all logs
heroku logs

# Restart dyno
heroku restart

# Scale dynos
heroku ps:scale web=1
```

---

## 🌐 AWS Deployment

### Option 1: AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize Beanstalk**
```bash
eb init -p python-3.10 synora-app
```

3. **Create Environment**
```bash
eb create synora-env
```

4. **Add Environment Variables**
```bash
eb setenv MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```

5. **Deploy**
```bash
eb deploy
```

6. **Open Application**
```bash
eb open
```

### Option 2: AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: Allow ports 8501, 27017 (if local MongoDB)

2. **SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies**
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip mongodb wget
sudo systemctl start mongodb
```

4. **Deploy Application**
```bash
git clone https://github.com/yourusername/bci_cybersecurity_project.git
cd bci_cybersecurity_project
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

5. **Run as Service**
```bash
# Create systemd service file
sudo nano /etc/systemd/system/synora.service
```

Add:
```ini
[Unit]
Description=SYNORA BCI Security
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bci_cybersecurity_project
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable synora
sudo systemctl start synora
```

---

## ☁️ Azure Deployment

### Option 1: Azure App Service

1. **Create Azure CLI**
```bash
az login
az group create --name synora-rg --location eastus
```

2. **Create App Service**
```bash
az appservice plan create --name synora-plan -g synora-rg --sku B1 --is-linux
az webapp create -n synora-app -g synora-rg -p synora-plan --runtime "PYTHON|3.10"
```

3. **Configure App**
```bash
az webapp config appsettings set -n synora-app -g synora-rg \
  --settings MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```

4. **Deploy from GitHub**
```bash
az webapp deployment source config-zip -n synora-app -g synora-rg \
  --src deployment.zip
```

### Option 2: Azure Container Instances

```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image synora:latest .

# Deploy
az container create --resource-group synora-rg \
  --name synora-container \
  --image myregistry.azurecr.io/synora:latest \
  --ports 8501 \
  --environment-variables MONGODB_URI="..."
```

---

## 🖥️ Self-Hosted (Linux/Ubuntu)

### Full Setup Guide

```bash
# 1. Update system
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install dependencies
sudo apt-get install -y \
  python3.10 \
  python3-pip \
  git \
  mongodb \
  nginx

# 3. Clone repository
cd /var/www
sudo git clone https://github.com/yourusername/bci_cybersecurity_project.git
cd bci_cybersecurity_project

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install Python packages
pip install -r requirements.txt

# 6. Create systemd service
sudo tee /etc/systemd/system/synora.service > /dev/null <<EOF
[Unit]
Description=SYNORA BCI Security Application
After=network.target mongodb.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/bci_cybersecurity_project
Environment="PATH=/var/www/bci_cybersecurity_project/venv/bin"
ExecStart=/var/www/bci_cybersecurity_project/venv/bin/streamlit run app.py \
  --server.port 8501 \
  --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 7. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable synora
sudo systemctl start synora

# 8. Configure Nginx reverse proxy
sudo tee /etc/nginx/sites-available/synora > /dev/null <<'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Streamlit specific
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# 9. Enable Nginx site
sudo ln -s /etc/nginx/sites-available/synora /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. Setup SSL (Let's Encrypt)
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Monitoring & Maintenance

```bash
# Check service status
sudo systemctl status synora

# View logs
sudo journalctl -u synora -f

# Restart service
sudo systemctl restart synora

# Check MongoDB
sudo systemctl status mongodb
mongo --eval "db.adminCommand('ping')"
```

---

## 📊 Deployment Comparison

| Platform | Cost | Ease | Scalability | Maintenance |
|----------|------|------|-------------|-------------|
| Streamlit Cloud | Free-Pro | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Minimal |
| Docker | Low | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Low |
| Heroku | Low-Mid | ⭐⭐⭐⭐ | ⭐⭐⭐ | Low |
| AWS EC2 | Low | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium |
| Azure App | Low | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Low |
| Self-Hosted | Low | ⭐⭐ | ⭐⭐ | High |

---

## 🔒 Security Checklist

- [ ] Change default MongoDB credentials
- [ ] Use HTTPS/SSL certificates
- [ ] Set strong session timeouts
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable audit logging
- [ ] Regular backups
- [ ] Monitor resource usage

---

## 🆘 Troubleshooting

### Common Issues

**Port 8501 in use**
```bash
streamlit run app.py --server.port 8502
```

**MongoDB connection failed**
```bash
# Check MongoDB is running
mongod --version
# Start MongoDB
mongod.exe  # Windows
brew services start mongodb-community  # macOS
```

**Memory errors**
- Reduce packet scan size
- Upgrade server resources
- Enable caching

**Slow performance**
- Check network latency
- Optimize LSTM model
- Add CDN for static files
- Scale horizontally

---

## 📞 Support

For deployment issues:
1. Check `requirements.txt` compatibility
2. Verify MongoDB connection
3. Check environment variables
4. Review application logs
5. Consult platform-specific documentation

---

**© 2024 SYNORA - AI Cybersecurity for Brain Interfaces**
