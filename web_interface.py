import gradio as gr
from function_calling import PollutionQueryHandler
from config import Config

# Validate configuration before starting
Config.validate_config()

# Initialize AI handler
handler = PollutionQueryHandler(Config.ANTHROPIC_API_KEY)

def chat(prompt):
    """Process user queries and return AI responses"""
    try:
        result = handler.call_claude_function(prompt)
        final_result = handler.rewrite_result_with_advice(result)
        return final_result
    except Exception as e:
        return f"❌ Error processing request: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Air Quality Monitor", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🌍 Air Quality Index Monitoring System")
    gr.Markdown("### Intelligent Air Pollution Analysis with AI")
    
    gr.Markdown("""
    **🔍 What you can ask:**  
    - **Predict pollution**: "Dự đoán mức độ ô nhiễm vào ngày 15 tháng 3 năm 2025 lúc 10 giờ với PT08_S1_CO 120.5, C6H6_GT 5.3, PT08_S5_O3 45.2, PT08_S2_NMHC 220.7, PT08_S4_NO2 34.1"  
    - **Query data**: "Tôi muốn biết chất lượng không khí vào ngày 20 tháng 5 năm 2004"  
    - **Statistics**: "Tính trung bình dữ liệu ô nhiễm từ 17 tháng 3 năm 2004 đến 17 tháng 4 năm 2004"  
    - **Add data**: "Thêm chất lượng không khí vào ngày 10 tháng 4 năm 2007, lúc 8 giờ sáng với các thông số..."
    """)

    with gr.Row():
        with gr.Column(scale=4):
            textbox = gr.Textbox(
                label="Enter your query (Vietnamese):",
                placeholder="Nhập câu hỏi bằng tiếng Việt về chất lượng không khí...",
                lines=2
            )
        with gr.Column(scale=1):
            submit_btn = gr.Button("🚀 Submit", variant="primary", size="lg")
    
    output = gr.Textbox(
        label="AI Response:",
        lines=15,
        show_copy_button=True
    )

    # Event handler
    submit_btn.click(fn=chat, inputs=textbox, outputs=output)
    textbox.submit(fn=chat, inputs=textbox, outputs=output)

    gr.Markdown("""
    ---
    **💡 Features:**
    - 🤖 AI-powered analysis using Claude
    - 📊 Machine learning predictions  
    - 💾 Cassandra database integration
    - 📈 Statistical analysis
    - 🌐 Web-based interface
    """)

if __name__ == "__main__":
    print("🌐 Starting web interface...")
    print("⏳ Loading TensorFlow models (this may take a moment)...")
    
    try:
        demo.launch(
            share=True,
            server_name="0.0.0.0",
            server_port=None,  # Auto-find available port
            show_error=True,
            quiet=False,
            inbrowser=True
        )
    except OSError as e:
        print(f"❌ Port error: {e}")
        print("🔄 Trying different port...")
        demo.launch(
            share=True,
            server_name="0.0.0.0",
            server_port=7861,  # Alternative port
            show_error=True,
            quiet=False,
            inbrowser=True
        )
