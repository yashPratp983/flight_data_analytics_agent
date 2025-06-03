from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import sys
sys.path.append('..')
import tempfile
import shutil
from pydantic import BaseModel
from app.core.processor import auto_analyst
from app.agents.analysis import preprocessing_agent, statistical_analytics_agent, sk_learn_agent
import dspy
import os
### Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

lm = dspy.LM('openai/gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
dspy.configure(lm=lm)
# Initialize FastAPI app
app = FastAPI(
    title="Auto Analyst API",
    description="Automated data analysis system using DSPy agents",
    version="1.0.0"
)


# Define request models
class AnalysisRequest(BaseModel):
    query: str

class AnalysisResponse(BaseModel):
    status: str
    result: dict
    message: str

# Global variable to store the auto_analyst instance
auto_analyst_instance = None

# Define available agents
AVAILABLE_AGENTS = [
    preprocessing_agent, 
    statistical_analytics_agent, 
    sk_learn_agent
]


# @app.post("/upload-files/")
async def upload_files(
    flight_bookings: UploadFile = File(..., description="Flight bookings CSV file"),
    airline_mapping: UploadFile = File(..., description="Airline ID to Name mapping CSV file")
):
        """
        Upload the required CSV files and reinitialize the auto_analyst system
        """
        global auto_analyst_instance
        
    # try:
        # Validate file extensions
        if not flight_bookings.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Flight bookings file must be a CSV")
        if not airline_mapping.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Airline mapping file must be a CSV")
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Save uploaded files to temporary directory
        flight_bookings_path = os.path.join(temp_dir, "flight_bookings.csv")
        airline_mapping_path = os.path.join(temp_dir, "airline_mapping.csv")
        
        # Write flight bookings file
        with open(flight_bookings_path, "wb") as buffer:
            shutil.copyfileobj(flight_bookings.file, buffer)
        
        # Write airline mapping file
        with open(airline_mapping_path, "wb") as buffer:
            shutil.copyfileobj(airline_mapping.file, buffer)
        
        # Reinitialize auto_analyst with uploaded files
        auto_analyst_instance = auto_analyst(
            agents=AVAILABLE_AGENTS,
            flight_bookings_path=flight_bookings_path,
            airline_mapping_path=airline_mapping_path
        )
        
        return {"files": {"flight_bookings": flight_bookings_path,"airline_mapping": airline_mapping_path}}
            
                
            
        
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Failed to upload files: {str(e)}")

@app.post("/analyze/")
async def analyze_with_files(
    query: str,
    flight_bookings: UploadFile = File(...),
    airline_mapping: UploadFile = File(...)
):
        """
        Upload files and perform analysis in a single request
        """
    # try:
        # First upload the files
        upload_response = await upload_files(flight_bookings, airline_mapping)
        
        
        # # Then perform analysis
        auto_analyst_instance = auto_analyst(
            agents=AVAILABLE_AGENTS,
            flight_bookings_path=upload_response['files']['flight_bookings'],
            airline_mapping_path=upload_response['files']['airline_mapping']
        )
        analysis_result = auto_analyst_instance.forward(query)
        print(query)
        return {
            "upload_status": "success",
            "analysis_result": analysis_result
        }
        
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Combined operation failed: {str(e)}")

@app.get("/health/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "auto_analyst_initialized": auto_analyst_instance is not None
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # Assuming this file is named main.py
        host="0.0.0.0",
        port=8000,
        reload=False
    )