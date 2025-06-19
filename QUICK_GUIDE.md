# 🚀 Quick Start Guide

## 📋 Setup trong 5 phút

### 1️⃣ Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Tạo file cấu hình
```bash
python setup_env.py
```
➡️ Nhập API key từ: https://console.anthropic.com/

### 3️⃣ Khởi động Cassandra
```bash
docker run -d --name my-cassandra -p 9042:9042 antranthanh/my-cassandra
```

### 4️⃣ Chạy ứng dụng
```bash
python start.py
```

## ⚡ Hoặc chạy trực tiếp:
- **Web**: `python web_interface.py`
- **CLI**: `python function_calling.py`

## 🎯 Ví dụ câu hỏi:
- "Dữ liệu ô nhiễm ngày 1/5/2004"
- "Dự đoán AQI với PT08_S1_CO=120, C6H6_GT=5.3..."
- "Thống kê trung bình tháng 5/2004"

---
✅ **Ready to go!** 🌍 