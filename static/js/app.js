// Air Quality Monitor - Frontend JavaScript

class AirQualityApp {
    constructor() {
        this.initializeEventListeners();
        this.checkSystemHealth();
    }

    initializeEventListeners() {
        // Chat functionality
        document.getElementById('userInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        // Prediction form
        document.getElementById('predictionForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.makePrediction();
        });
    }

    async checkSystemHealth() {
        try {
            const response = await fetch('/health');
            const health = await response.json();
            
            if (health.ai_handler === 'unavailable') {
                this.showSystemMessage('⚠️ Hệ thống AI hiện không khả dụng. Vui lòng kiểm tra cấu hình API key.', 'warning');
            }
        } catch (error) {
            this.showSystemMessage('❌ Không thể kết nối đến server. Vui lòng thử lại sau.', 'error');
        }
    }

    showLoading(show = true) {
        const overlay = document.getElementById('loadingOverlay');
        if (show) {
            overlay.classList.add('show');
        } else {
            overlay.classList.remove('show');
        }
    }

    addMessageToChat(message, type = 'user') {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        if (type === 'assistant') {
            messageDiv.innerHTML = `<i class="fas fa-robot"></i> ${message}`;
        } else if (type === 'user') {
            messageDiv.innerHTML = `<i class="fas fa-user"></i> ${message}`;
        } else {
            messageDiv.innerHTML = message;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    showSystemMessage(message, type = 'info') {
        const iconMap = {
            'info': 'fas fa-info-circle',
            'warning': 'fas fa-exclamation-triangle',
            'error': 'fas fa-times-circle',
            'success': 'fas fa-check-circle'
        };
        
        this.addMessageToChat(`<i class="${iconMap[type]}"></i> ${message}`, 'system');
    }

    async sendMessage() {
        const userInput = document.getElementById('userInput');
        const message = userInput.value.trim();
        
        if (!message) return;

        // Add user message to chat
        this.addMessageToChat(message, 'user');
        userInput.value = '';

        // Show loading
        this.showLoading(true);

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const result = await response.json();

            if (result.success) {
                this.addMessageToChat(result.response, 'assistant');
            } else {
                this.showSystemMessage('❌ Có lỗi xảy ra khi xử lý câu hỏi của bạn.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showSystemMessage('❌ Không thể gửi tin nhắn. Vui lòng thử lại.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async makePrediction() {
        const formData = {
            day: parseInt(document.getElementById('day').value),
            month: parseInt(document.getElementById('month').value),
            year: parseInt(document.getElementById('year').value),
            hour: parseInt(document.getElementById('hour').value),
            pt08_s1_co: parseFloat(document.getElementById('pt08_s1_co').value),
            c6h6_gt: parseFloat(document.getElementById('c6h6_gt').value),
            pt08_s5_o3: parseFloat(document.getElementById('pt08_s5_o3').value),
            pt08_s2_nmhc: parseFloat(document.getElementById('pt08_s2_nmhc').value),
            pt08_s4_no2: parseFloat(document.getElementById('pt08_s4_no2').value)
        };

        const resultDiv = document.getElementById('predictionResult');
        resultDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang dự đoán...';

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success && result.prediction) {
                const prediction = result.prediction;
                const level = prediction.pollution_level;
                const description = prediction.description;

                // Determine result class based on pollution level
                const levelClasses = ['good', 'moderate', 'unhealthy-sensitive', 'unhealthy', 'very-unhealthy'];
                const levelIcons = ['🟢', '🟡', '🟠', '🔴', '⚫'];
                const levelClass = levelClasses[level] || 'good';
                const levelIcon = levelIcons[level] || '🟢';

                resultDiv.className = `prediction-result ${levelClass}`;
                resultDiv.innerHTML = `
                    ${levelIcon} <strong>Mức độ ô nhiễm: ${description}</strong><br>
                    <small>Chỉ số: ${level}/4</small>
                `;

                // Add to chat as well
                this.addMessageToChat(
                    `Kết quả dự đoán: ${levelIcon} <strong>${description}</strong> (${level}/4)`, 
                    'assistant'
                );
            } else {
                resultDiv.className = 'prediction-result';
                resultDiv.innerHTML = '❌ Không thể thực hiện dự đoán. Vui lòng thử lại.';
            }
        } catch (error) {
            console.error('Prediction error:', error);
            resultDiv.className = 'prediction-result';
            resultDiv.innerHTML = '❌ Lỗi kết nối. Vui lòng thử lại sau.';
        }
    }

    // Utility function to format datetime for API calls
    formatDateTime(day, month, year, hour) {
        return `${day}/${month}/${year} ${hour}:00`;
    }

    // Sample queries for demonstration
    showSampleQueries() {
        const samples = [
            "Dữ liệu ô nhiễm ngày 1 tháng 5 năm 2004",
            "Dự đoán mức độ ô nhiễm với PT08_S1_CO=120, C6H6_GT=5.3, PT08_S5_O3=45.2, PT08_S2_NMHC=220.7, PT08_S4_NO2=34.1",
            "Thống kê trung bình ô nhiễm từ ngày 1 đến 30 tháng 5 năm 2004",
            "Thêm dữ liệu ô nhiễm ngày 10/4/2007 lúc 8h với các thông số..."
        ];

        this.showSystemMessage(`
            💡 Bạn có thể thử các câu hỏi mẫu:<br>
            ${samples.map(q => `• "${q}"`).join('<br>')}
        `, 'info');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.airQualityApp = new AirQualityApp();
    
    // Show sample queries after a short delay
    setTimeout(() => {
        window.airQualityApp.showSampleQueries();
    }, 2000);
});

// Add some helper functions for better UX
window.sendMessage = () => window.airQualityApp.sendMessage();

// Auto-resize textareas and inputs
document.addEventListener('input', (e) => {
    if (e.target.tagName === 'TEXTAREA') {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to send message
    if (e.ctrlKey && e.key === 'Enter') {
        window.airQualityApp.sendMessage();
    }
    
    // Escape to clear input
    if (e.key === 'Escape') {
        const userInput = document.getElementById('userInput');
        userInput.value = '';
        userInput.focus();
    }
}); 