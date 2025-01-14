import subprocess
import time
import webbrowser

def main():
    # Start Flask backend
    flask_process = subprocess.Popen(['python', 'run.py'])
    print("Starting Flask backend...")
    time.sleep(2)  # Give Flask time to start
    
    # Start Streamlit frontend
    print("Starting Streamlit frontend...")
    streamlit_process = subprocess.Popen(['streamlit', 'run', 'frontend/main.py'])
    
    # Open browser after a short delay
    time.sleep(3)
    webbrowser.open('http://localhost:8501')
    
    try:
        # Keep the script running
        streamlit_process.wait()
    finally:
        # Cleanup
        flask_process.terminate()
        streamlit_process.terminate()

if __name__ == "__main__":
    main() 