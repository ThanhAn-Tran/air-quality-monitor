#!/bin/bash
# 🚀 Air Quality Monitor - Quick Deploy Script for Digital Ocean

echo "🌍 Air Quality Monitor - Digital Ocean Deployment"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

print_status "Starting deployment process..."

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing Python, Git, and Docker..."
apt install python3 python3-pip python3-venv git docker.io nginx -y

# Start and enable Docker
print_status "Starting Docker service..."
systemctl start docker
systemctl enable docker

# Create application directory
print_status "Creating application directory..."
mkdir -p /opt/air-quality-monitor
cd /opt/air-quality-monitor

# Clone the repository
print_status "Cloning repository..."
if [ -d ".git" ]; then
    print_warning "Repository already exists, pulling latest changes..."
    git pull origin main
else
    git clone https://github.com/ThanhAn-Tran/air-quality-monitor.git .
fi

# Create virtual environment
print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment file
print_status "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || cat > .env << EOF
# Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Database Configuration
CASSANDRA_HOSTS=127.0.0.1
CASSANDRA_KEYSPACE=pollution_db

# Web Interface
WEB_PORT=7860
WEB_HOST=0.0.0.0
EOF
    print_warning "Please edit .env file and add your actual API key!"
    print_warning "nano /opt/air-quality-monitor/.env"
fi

# Start Cassandra
print_status "Starting Cassandra database..."
docker run -d --name cassandra-db \
  -p 9042:9042 \
  --restart unless-stopped \
  antranthanh/my-cassandra

# Create systemd service
print_status "Creating systemd service..."
cat > /etc/systemd/system/air-quality-monitor.service << EOF
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
EOF

# Enable and start service
print_status "Enabling and starting service..."
systemctl daemon-reload
systemctl enable air-quality-monitor

# Configure firewall
print_status "Configuring firewall..."
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443
ufw allow 7860

print_status "Deployment completed!"
echo ""
echo "🎉 Your Air Quality Monitor is ready!"
echo ""
echo "📋 Next steps:"
echo "1. Edit your API key: nano /opt/air-quality-monitor/.env"
echo "2. Start the service: systemctl start air-quality-monitor"
echo "3. Check status: systemctl status air-quality-monitor"
echo "4. Access your app: http://YOUR_SERVER_IP:7860"
echo ""
echo "🔧 Useful commands:"
echo "- View logs: journalctl -u air-quality-monitor -f"
echo "- Restart service: systemctl restart air-quality-monitor"
echo "- Update app: cd /opt/air-quality-monitor && git pull"
echo ""
print_warning "Don't forget to replace 'your_api_key_here' in .env file!" 