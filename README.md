# 🌍 Air Quality Index Monitor

Hệ thống giám sát chỉ số chất lượng không khí (AQI) với AI tích hợp sử dụng Claude API, TensorFlow, và Cassandra database.

## ✨ Tính năng chính

- 📊 **Dự đoán AQI**: Sử dụng machine learning để dự đoán mức độ ô nhiễm
- 🔍 **Truy vấn dữ liệu**: Tìm kiếm dữ liệu theo ngày/tháng/năm
- 📈 **Phân tích thống kê**: Thống kê mean, median, max, min của dữ liệu
- 💬 **AI Chat**: Tương tác bằng tiếng Việt với Claude AI
- 🌐 **Web Interface**: Giao diện web thân thiện với Gradio
- 💾 **Lưu trữ dữ liệu**: Cassandra database để lưu trữ dữ liệu lớn

## 🚀 Cài đặt nhanh

### 1. Clone repository
```bash
git clone <your-repo-url>
cd PythonProject
```

### 2. Tạo virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình API key
Tạo file `.env` và thêm API key của bạn:
```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 5. Khởi động Cassandra
```bash
docker run -d --name my-cassandra -p 9042:9042 antranthanh/my-cassandra
```

### 6. Chạy ứng dụng
```bash
python web_interface.py  # Web interface
# hoặc
python function_calling.py  # Command line
```

## 📁 Cấu trúc project

```
PythonProject/
├── 🧠 function_calling.py      # AI handler chính
├── 🌐 web_interface.py         # Giao diện web Gradio
├── 💾 cassandra_CRUD.py        # Database operations
├── 📊 process_data_training.py # Xử lý và train model
├── ⚙️ config.py               # Cấu hình hệ thống
├── 🔧 requirements.txt        # Dependencies
├── 📋 .env                    # Environment variables
├── 🤖 model_ML/               # Trained AI models
└── 📈 Data/                   # Datasets
```

## 🎯 Cách sử dụng

### Web Interface
1. Chạy `python web_interface.py`
2. Mở browser tại `http://localhost:7860`
3. Nhập câu hỏi bằng tiếng Việt

### Command Line
```bash
python function_calling.py
```

### Ví dụ câu hỏi
- "Cho tôi biết dữ liệu ô nhiễm ngày 1 tháng 5 năm 2004"
- "Dự đoán mức độ ô nhiễm với các thông số: ngày 15, tháng 6, năm 2024..."
- "Thống kê trung bình ô nhiễm từ ngày 1 đến 30 tháng 5 năm 2004"

## 🛠️ Các công cụ có sẵn

1. **query_pollution_data_openai**: Truy vấn dữ liệu theo ngày/tháng/năm
2. **predict_pollution_level**: Dự đoán mức độ ô nhiễm
3. **insert_data_to_database**: Thêm dữ liệu mới vào database
4. **statistical_analysis**: Phân tích thống kê dữ liệu

## 🔧 Yêu cầu hệ thống

- Python 3.8+
- Docker (cho Cassandra)
- RAM: 4GB+ (cho TensorFlow)
- Disk: 2GB+ free space

## 📊 Mức độ ô nhiễm

- **0**: Thấp (Tốt) 🟢
- **1**: Trung bình (Ổn định) 🟡
- **2**: Cao (Kém) 🟠
- **3**: Nguy hiểm (Rất kém) 🔴
- **4**: Rất nguy hại (Cực kém) ⚫

## 🔒 Bảo mật

- ✅ API keys được lưu trong file `.env`
- ✅ File `.env` được gitignore
- ✅ Không có hardcode API keys trong source code

## 🐛 Troubleshooting

### Lỗi API Key
```
ValueError: ANTHROPIC_API_KEY is required
```
**Giải pháp**: Kiểm tra file `.env` và đảm bảo API key đúng

### Lỗi Cassandra
```
cassandra.cluster.NoHostAvailable
```
**Giải pháp**: Đảm bảo Docker container đang chạy:
```bash
docker start my-cassandra
```

### Lỗi TensorFlow
```
Could not load model
```
**Giải pháp**: Kiểm tra file `model_ML/air_quality_model.h5` tồn tại

## 🤝 Đóng góp

1. Fork project
2. Tạo feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push branch: `git push origin feature/new-feature`
5. Tạo Pull Request

---
⭐ Nếu project hữu ích, đừng quên star repo nhé! 