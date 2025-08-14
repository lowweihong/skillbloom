#!/usr/bin/env python3
"""
Startup script for the Learning Plan Generator Backend API
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import requests
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_environment():
    """Check environment configuration"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Creating default .env file...")
        
        # Create basic .env file
        env_content = """# Learning Plan Generator Environment Variables
# Generated automatically by start_backend.py

# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_api_key_here

# Single iteration workflow
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ .env file created")
        print("⚠️  Please update GOOGLE_API_KEY in the .env file")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    else:
        print("✅ .env file found")
        return True

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Learning Plan Generator Backend API...")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Please configure your API key before starting the server")
        return False
    
    print("\n📋 Server Configuration:")
    print("   Host: 0.0.0.0 (accessible from any IP)")
    print("   Port: 8000")
    print("   API Documentation: http://localhost:8000/docs")
    print("   Health Check: http://localhost:8000/health")
    print("   Frontend Example: Open frontend_example.html in your browser")
    
    print("\n🔌 API Endpoints:")
    print("   POST /api/v1/generate-plan - Generate learning plan")
    print("   GET  /api/v1/plan/{id} - Retrieve plan by ID")
    print("   GET  /api/v1/plans - List recent plans")
    print("   DELETE /api/v1/plan/{id} - Delete plan")
    print("   POST /api/v1/batch-generate - Generate multiple plans")
    
    print("\n🌐 Frontend Integration:")
    print("   • Use frontend_example.html for web interface")
    print("   • Use frontend_client.py for Python applications")
    print("   • CORS enabled for cross-origin requests")
    
    print("\n🚀 Starting server...")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Import and run the server
        from api_server import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Server stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        return False

def main():
    """Main function"""
    print("🎓 Learning Plan Generator - Backend API Server")
    print("=" * 60)
    
    if start_server():
        print("✅ Server stopped successfully")
    else:
        print("❌ Server failed to start")
        sys.exit(1)

if __name__ == "__main__":
    main() 