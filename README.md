# 🌍 Air Quality Index Monitor

A smart system for monitoring air pollution levels (AQI) using AI. Built with **Claude API**, **TensorFlow**, and **Cassandra** for scalable data storage.

---

## ✨ Key Features

* 📊 **AQI Prediction** using machine learning models
* 🔍 **Data Query** by day, month, and year
* 📈 **Statistical Analysis**: mean, median, max, min
* 💬 **AI Chatbot** powered by Claude API, supports Vietnamese
* 🌐 **User-Friendly Web UI** built with Gradio
* 💾 **Cassandra Database** for efficient large-scale storage

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/ThanhAn-Tran/air-quality-monitor.git
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file with your Claude API key:

```env
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 5. Start Cassandra via Docker

# Step 1: Pull custom Cassandra image
```bash
docker pull antranthanh/my-cassandra
```

# Step 2: Run the container
```bash
docker run -d --name my-cassandra -p 9042:9042 antranthanh/my-cassandra
```

# Step 3: Check if the container is running
```bash
docker ps
```

### 6. Run the App

```bash
python web_interface.py        # Gradio web app
# or
python function_calling.py     # CLI interface
```

---

## 📁 Project Structure

```
PythonProject/
├── function_calling.py        # Main AI interaction script
├── web_interface.py           # Gradio-based UI
├── cassandra_CRUD.py          # Cassandra DB operations
├── process_data_training.py   # ML training and preprocessing
├── config.py                  # Environment config
├── requirements.txt           # Dependencies list
├── .env                       # API keys (excluded from Git)
├── model_ML/                  # Saved models
└── Data/                      # Raw datasets
```

---

## 🎯 How to Use

### Web Interface

1. Run `python web_interface.py`
2. Open browser at `http://localhost:7860`
3. Ask questions in Vietnamese

### Command Line

```bash
python function_calling.py
```

### Example Questions

* "Cho tôi biết dữ liệu ô nhiễm ngày 1 tháng 5 năm 2004"
* "Dự đoán mức độ ô nhiễm với các thông số..."
* "Thống kê trung bình từ ngày 1 đến 30 tháng 5 năm 2004"

---

## 🧰 Available Tools

* `query_pollution_data_openai()`: Query by date
* `predict_pollution_level()`: ML-based AQI prediction
* `insert_data_to_database()`: Add new records
* `statistical_analysis()`: Summary stats

---

## ⚙️ System Requirements

* Python 3.8+
* Docker (for Cassandra)
* 4GB+ RAM (for ML models)
* 2GB+ disk space

---

## 📊 Pollution Levels

| Level | Description    | Color     |
| ----- | -------------- | --------- |
| 0     | Good           | 🟢 Green  |
| 1     | Moderate       | 🟡 Yellow |
| 2     | Unhealthy      | 🟠 Orange |
| 3     | Very Unhealthy | 🔴 Red    |
| 4     | Hazardous      | ⚫ Black   |

---

## 🔒 Security

* API key stored securely in `.env` file
* `.env` is excluded via `.gitignore`
* No hardcoded secrets in the code

---

## 📦 Deployment Environment

| Tool   | Version           |
| ------ | ----------------- |
| OS     | Windows 11        |
| Docker | v27.3.1           |
| IDE    | PyCharm 2024.3 CE |
| Python | 3.8+              |

Ensure required PyCharm plugins are installed: Docker, dotenv, envfile.

---

## 🧑‍💻 Author

**Trần Thành An**
📧 [antranthanh904@gmail.com](mailto:antranthanh904@gmail.com)
🔗 [GitHub: ThanhAn-Tran](https://github.com/ThanhAn-Tran)

---
