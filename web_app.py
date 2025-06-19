#!/usr/bin/env python3
"""
🌍 Air Quality Monitor - Custom Web Interface
Alternative to Gradio with HTML/CSS/JavaScript
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from function_calling import PollutionQueryHandler
from config import Config

# Initialize FastAPI app
app = FastAPI(
    title="Air Quality Monitor",
    description="AI-powered Air Quality Index monitoring system",
    version="1.0.0"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize AI handler
try:
    Config.validate_config()
    ai_handler = PollutionQueryHandler(Config.ANTHROPIC_API_KEY)
except Exception as e:
    print(f"❌ Configuration error: {e}")
    ai_handler = None

# Pydantic models for API
class QueryRequest(BaseModel):
    message: str

class PredictionRequest(BaseModel):
    day: int
    month: int
    year: int
    hour: int
    pt08_s1_co: float
    c6h6_gt: float
    pt08_s5_o3: float
    pt08_s2_nmhc: float
    pt08_s4_no2: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_handler": "available" if ai_handler else "unavailable",
        "version": "1.0.0"
    }

@app.post("/api/query")
async def process_query(request: QueryRequest):
    """Process natural language queries"""
    if not ai_handler:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    try:
        # Process query with AI
        result = ai_handler.call_claude_function(request.message)
        final_result = ai_handler.rewrite_result_with_advice(result)
        
        return {
            "success": True,
            "response": final_result,
            "raw_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing error: {str(e)}")

@app.post("/api/predict")
async def predict_pollution(request: PredictionRequest):
    """Direct pollution prediction"""
    if not ai_handler:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    try:
        result = ai_handler.predict_pollution_level(
            Day=request.day,
            Month=request.month, 
            Year=request.year,
            Hour=request.hour,
            PT08_S1_CO=request.pt08_s1_co,
            C6H6_GT=request.c6h6_gt,
            PT08_S5_O3=request.pt08_s5_o3,
            PT08_S2_NMHC=request.pt08_s2_nmhc,
            PT08_S4_NO2=request.pt08_s4_no2
        )
        
        return {
            "success": True,
            "prediction": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/api/stats/{stat_type}")
async def get_statistics(stat_type: str, start_day: int, start_month: int, 
                        end_day: int, end_month: int, year: int):
    """Get statistical analysis"""
    if not ai_handler:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    try:
        result = ai_handler.statistical_analysis(
            stat_type=stat_type,
            start_day=start_day,
            start_month=start_month,
            end_day=end_day,
            end_month=end_month,
            year=year
        )
        
        return {
            "success": True,
            "statistics": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics error: {str(e)}")

if __name__ == "__main__":
    # Create directories if they don't exist
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    # Run the application
    port = getattr(Config, 'WEB_PORT', 8000)
    host = getattr(Config, 'WEB_HOST', '0.0.0.0')
    
    print(f"🚀 Starting Air Quality Monitor on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port) 