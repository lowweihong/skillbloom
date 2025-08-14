#!/usr/bin/env python3
"""
Launcher script for the Learning Plan Generator Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    
    # Check if we're in the virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in a virtual environment")
        print("Please activate the virtual environment first:")
        print("   source venv/bin/activate")
        print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run setup_env.py first to configure your API key.")
        return
    
    print("🚀 Launching Learning Plan Generator...")
    print("📱 Opening web browser...")
    print("🔄 Press Ctrl+C to stop the server")
    print()
    
    try:
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main() 