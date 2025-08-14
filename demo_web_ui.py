#!/usr/bin/env python3
"""
Demo script for the Learning Plan Generator Web UI
This script demonstrates how to launch and use the Streamlit application
"""

import subprocess
import sys
import time
import webbrowser
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import langchain
        import langgraph
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_env():
    """Check if environment is properly configured"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Please run setup_env.py first to configure your API key")
        return False
    
    print("✅ Environment configuration found")
    return True

def launch_streamlit():
    """Launch the Streamlit application"""
    print("🚀 Launching Learning Plan Generator Web UI...")
    print("📱 Opening web browser...")
    print("🔄 Press Ctrl+C to stop the server")
    print()
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:8501')
    
    # Start browser opening in background
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

def main():
    """Main demo function"""
    print("🎓 Learning Plan Generator - Web UI Demo")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies:")
        print("   pip install -r requirements.txt")
        return
    
    # Check environment
    if not check_env():
        return
    
    print("\n🎯 Ready to launch the web interface!")
    print("\n📋 What you'll be able to do:")
    print("   • Create personalized learning plans")
    print("   • Choose from multiple learning formats")
    print("   • Get detailed resource recommendations")
    print("   • Download plans as JSON files")
    print("   • Track progress with beautiful UI")
    
    print("\n🚀 Launching in 3 seconds...")
    time.sleep(3)
    
    launch_streamlit()

if __name__ == "__main__":
    main() 