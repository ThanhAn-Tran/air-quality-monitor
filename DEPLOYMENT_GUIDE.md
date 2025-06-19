# 🚀 Deployment Guide: Host Your Air Quality Monitor

## 📋 Overview
Deploy your AI-powered Air Quality Monitor on **Digital Ocean** using your **GitHub Student Pack** ($200 free credit!).

---

## 🎓 Step 1: Get GitHub Student Pack & Digital Ocean Credits

### 1.1 Apply for GitHub Student Pack
1. Go to: https://education.github.com/pack
2. Click **"Get Student Benefits"**
3. Verify with your **.edu email** or student ID
4. Wait for approval (usually 1-3 days)

### 1.2 Claim Digital Ocean Credits
1. Once approved, go to your GitHub Student Pack dashboard
2. Find **"Digital Ocean"** in the benefits
3. Click **"Get access"** → You'll get **$200 credit**!
4. Create Digital Ocean account or link existing one

---

## 🏗️ Step 2: Choose Your Deployment Method

### 🎯 **Option A: Easy Deployment (Recommended)**
**Keep Gradio Interface** - Deploy as-is, fastest setup

### 🎯 **Option B: Professional Deployment**
**Custom Web Interface** - Convert to HTML/CSS/JavaScript

We'll start with **Option A** (easiest), then show Option B.

---

## 🚀 Option A: Quick Deployment with Gradio

### 2.1 Create Digital Ocean Droplet

1. **Login to Digital Ocean**: https://cloud.digitalocean.com/
2. **Create Droplet**:
   - Click **"Create"** → **"Droplets"**
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6/month = $0.009/hour)
   - **CPU**: Regular Intel (1GB RAM, 1 vCPU)
   - **Datacenter**: Choose closest to your users
   - **Authentication**: SSH Key (recommended) or Password
   - **Hostname**: `air-quality-monitor`
   - Click **"Create Droplet"**

### 2.2 Connect to Your Server

```bash
# Replace YOUR_DROPLET_IP with actual IP
ssh root@YOUR_DROPLET_IP
```

### 2.3 Setup Server Environment

```bash
# Update system
apt update && apt upgrade -y

# Install Python and pip
apt install python3 python3-pip python3-venv git -y

# Install Docker for Cassandra
apt install docker.io -y
systemctl start docker
systemctl enable docker

# Create application directory
mkdir /opt/air-quality-monitor
cd /opt/air-quality-monitor
```

### 2.4 Clone Your Project

```bash
# Clone your repository
git clone https://github.com/ThanhAn-Tran/air-quality-monitor.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.5 Setup Environment Variables

```bash
# Create .env file
nano .env
```

Add your configuration:
```env
# Anthropic API Key
ANTHROPIC_API_KEY=your_actual_api_key_here

# Database Configuration
CASSANDRA_HOSTS=127.0.0.1
CASSANDRA_KEYSPACE=pollution_db

# Web Interface
WEB_PORT=7860
WEB_HOST=0.0.0.0
```

Save with `Ctrl+X`, `Y`, `Enter`

### 2.6 Start Cassandra Database

```bash
# Pull and run your custom Cassandra image
docker run -d --name cassandra-db \
  -p 9042:9042 \
  --restart unless-stopped \
  antranthanh/my-cassandra
```

### 2.7 Create Systemd Service (Auto-start)

```bash
# Create service file
nano /etc/systemd/system/air-quality-monitor.service
```

Add this configuration:
```ini
[Unit]
Description=Air Quality Monitor Web Service
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/air-quality-monitor
Environment=PATH=/opt/air-quality-monitor/venv/bin
ExecStart=/opt/air-quality-monitor/venv/bin/python web_interface.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save and enable the service:
```bash
# Reload systemd and start service
systemctl daemon-reload
systemctl enable air-quality-monitor
systemctl start air-quality-monitor

# Check status
systemctl status air-quality-monitor
```

### 2.8 Configure Firewall

```bash
# Enable firewall
ufw enable

# Allow SSH, HTTP, and your application port
ufw allow ssh
ufw allow 80
ufw allow 7860

# Check status
ufw status
```

### 2.9 Access Your Application

Your app is now live at:
```
http://YOUR_DROPLET_IP:7860
```

---

## 🎯 Option B: Professional Web Interface

### 3.1 Convert Gradio to HTML/CSS

I'll create a custom web interface for you:

```bash
# Create web directory
mkdir -p /opt/air-quality-monitor/web
cd /opt/air-quality-monitor/web
```

### 3.2 Install Additional Dependencies

```bash
# Add to requirements.txt
echo "fastapi>=0.115.0" >> requirements.txt
echo "uvicorn>=0.20.0" >> requirements.txt
echo "jinja2>=3.1.0" >> requirements.txt

# Install
pip install fastapi uvicorn jinja2
```

### 3.3 Create Custom Web Interface

I'll create the files for you - would you like me to build a custom HTML/CSS interface to replace Gradio?

---

## 🔒 Step 3: Security & SSL (Important!)

### 3.1 Setup Domain (Optional but Recommended)

1. **Buy a domain** or use a free subdomain
2. **Point DNS** to your droplet IP
3. **Wait for propagation** (5-60 minutes)

### 3.2 Install SSL Certificate (Free with Let's Encrypt)

```bash
# Install Nginx
apt install nginx certbot python3-certbot-nginx -y

# Create Nginx config
nano /etc/nginx/sites-available/air-quality-monitor
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain
    
    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
# Enable site
ln -s /etc/nginx/sites-available/air-quality-monitor /etc/nginx/sites-enabled/
systemctl restart nginx

# Get SSL certificate
certbot --nginx -d your-domain.com
```

---

## 📊 Step 4: Monitoring & Maintenance

### 4.1 Setup Log Monitoring

```bash
# View application logs
journalctl -u air-quality-monitor -f

# View system resources
htop
df -h
```

### 4.2 Setup Automatic Updates

```bash
# Create update script
nano /opt/update-app.sh
```

Add:
```bash
#!/bin/bash
cd /opt/air-quality-monitor
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
systemctl restart air-quality-monitor
```

Make executable:
```bash
chmod +x /opt/update-app.sh
```

### 4.3 Backup Strategy

```bash
# Backup script
nano /opt/backup.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /opt/backup_$DATE.tar.gz /opt/air-quality-monitor
# Upload to Digital Ocean Spaces or another backup service
```

---

## 💰 Step 5: Cost Optimization

### 5.1 Monitor Usage

- **Basic Droplet**: $6/month ($0.009/hour)
- **Your $200 credit**: ~33 months of hosting!
- **Turn off when not needed**: Save money during development

### 5.2 Scaling Options

As your app grows:
- **Upgrade droplet**: More RAM/CPU
- **Add load balancer**: Handle more users
- **Use managed database**: Replace Docker Cassandra
- **Add CDN**: Faster global access

---

## 🚨 Troubleshooting

### Common Issues:

**🔴 App won't start:**
```bash
# Check logs
journalctl -u air-quality-monitor -n 50

# Check if port is busy
netstat -tulpn | grep 7860
```

**🔴 Database connection error:**
```bash
# Check Cassandra status
docker ps
docker logs cassandra-db
```

**🔴 Can't access from browser:**
```bash
# Check firewall
ufw status
# Check if app is running
systemctl status air-quality-monitor
```

---

## 🎉 You're Live!

Your Air Quality Monitor is now:
- ✅ **Hosted on Digital Ocean**
- ✅ **Auto-starting on boot**
- ✅ **Accessible from anywhere**
- ✅ **Using your $200 student credit**

### 📱 Share Your App:
- **Development**: `http://YOUR_IP:7860`
- **Production**: `https://your-domain.com`

---

## 🔄 Next Steps:

1. **Test your deployment** with sample data
2. **Add monitoring** (UptimeRobot, etc.)
3. **Setup backups** for your data
4. **Consider custom domain** for professional look
5. **Add analytics** to track usage

**Need help?** Create an issue in your GitHub repository!

---

## 🌟 Pro Tips:

- **Use snapshots**: Backup your entire droplet
- **Monitor costs**: Set billing alerts
- **Scale gradually**: Start small, upgrade as needed
- **Keep updating**: Regular security updates
- **Document changes**: Update this guide as you modify

**Congratulations! You're now a cloud deployment expert! 🚀** 