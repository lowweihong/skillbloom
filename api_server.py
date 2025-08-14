#!/usr/bin/env python3
"""
Learning Plan Generator - Backend API Server
FastAPI server that provides REST endpoints for frontend applications
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import json
import logging
from datetime import datetime

from models import UserInput, LearningFormat, CompleteLearningPlan
from workflow import LearningPlanWorkflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Learning Plan Generator API",
    description="AI-powered learning plan generator using LangChain AI 2 and LangGraph",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the learning plan workflow
workflow = LearningPlanWorkflow()

# Request/Response Models
class LearningPlanRequest(BaseModel):
    topic: str
    background: str
    preferred_format: str  # "video", "text", or "audio"
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class LearningPlanResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str
    request_id: str

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    workflow_status: str

# In-memory storage for generated plans (use database in production)
learning_plans = {}

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Learning Plan Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "generate_plan": "/api/v1/generate-plan"
    }

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test workflow initialization
        workflow_status = "healthy" if workflow else "unhealthy"
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="1.0.0",
            workflow_status=workflow_status
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

@app.post("/api/v1/generate-plan", response_model=LearningPlanResponse)
async def generate_learning_plan(request: LearningPlanRequest):
    """Generate a personalized learning plan based on user input"""
    
    try:
        # Validate preferred format
        if request.preferred_format.lower() not in ["video", "text", "audio"]:
            raise HTTPException(
                status_code=400, 
                detail="preferred_format must be 'video', 'text', or 'audio'"
            )
        
        # Convert string format to enum
        format_enum = LearningFormat(request.preferred_format.lower())
        
        # Create UserInput object
        user_input = UserInput(
            topic=request.topic.strip(),
            background=request.background.strip(),
            preferred_format=format_enum,
            max_iterations=1
        )
        
        # Generate unique request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        logger.info(f"Generating learning plan for topic: {request.topic}")
        
        # Generate the learning plan
        learning_plan = workflow.create_learning_plan(user_input)
        
        # Convert to dictionary for JSON response
        plan_data = learning_plan.model_dump()
        
        # Store the plan (in production, use a database)
        learning_plans[request_id] = {
            "plan": plan_data,
            "user_input": request.dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Learning plan generated successfully. Request ID: {request_id}")
        
        return LearningPlanResponse(
            success=True,
            message="Learning plan generated successfully",
            data=plan_data,
            timestamp=datetime.now().isoformat(),
            request_id=request_id
        )
        
    except Exception as e:
        logger.error(f"Error generating learning plan: {e}")
        return LearningPlanResponse(
            success=False,
            message="Failed to generate learning plan",
            error=str(e),
            timestamp=datetime.now().isoformat(),
            request_id=""
        )

@app.get("/api/v1/plan/{request_id}")
async def get_learning_plan(request_id: str):
    """Retrieve a previously generated learning plan by request ID"""
    
    if request_id not in learning_plans:
        raise HTTPException(status_code=404, detail="Learning plan not found")
    
    return {
        "success": True,
        "data": learning_plans[request_id],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/plans")
async def list_learning_plans(limit: int = 10, offset: int = 0):
    """List recently generated learning plans (for admin/monitoring)"""
    
    plan_list = list(learning_plans.items())[offset:offset + limit]
    
    return {
        "success": True,
        "data": {
            "plans": plan_list,
            "total": len(learning_plans),
            "limit": limit,
            "offset": offset
        },
        "timestamp": datetime.now().isoformat()
    }

@app.delete("/api/v1/plan/{request_id}")
async def delete_learning_plan(request_id: str):
    """Delete a learning plan by request ID"""
    
    if request_id not in learning_plans:
        raise HTTPException(status_code=404, detail="Learning plan not found")
    
    del learning_plans[request_id]
    
    return {
        "success": True,
        "message": "Learning plan deleted successfully",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/batch-generate")
async def batch_generate_plans(requests: list[LearningPlanRequest]):
    """Generate multiple learning plans in batch"""
    
    results = []
    
    for i, request in enumerate(requests):
        try:
            # Generate plan for each request
            format_enum = LearningFormat(request.preferred_format.lower())
            
            user_input = UserInput(
                topic=request.topic.strip(),
                background=request.background.strip(),
                preferred_format=format_enum,
                max_iterations=1
            )
            
            learning_plan = workflow.create_learning_plan(user_input)
            plan_data = learning_plan.model_dump()
            
            results.append({
                "index": i,
                "success": True,
                "topic": request.topic,
                "data": plan_data
            })
            
        except Exception as e:
            results.append({
                "index": i,
                "success": False,
                "topic": request.topic,
                "error": str(e)
            })
    
    return {
        "success": True,
        "message": f"Batch processing completed. {len([r for r in results if r['success']])}/{len(requests)} successful",
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 