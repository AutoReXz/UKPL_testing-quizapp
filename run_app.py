"""
Simple runner script for the Streamlit Quiz App
Usage: python run_app.py
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application."""
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        streamlit_app_path = os.path.join(script_dir, "streamlit_quiz_app.py")
        
        print("🚀 Starting Quiz Application...")
        print("📝 Opening browser automatically...")
        print("🔗 If browser doesn't open, go to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            streamlit_app_path, 
            "--server.headless", "false",
            "--server.runOnSave", "true",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user.")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
