import time
import subprocess
import logging
import os
import sys
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_log.txt"),
        logging.StreamHandler()
    ]
)

# Get the absolute path to the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(SCRIPT_DIR, "twitter_scraper_env", "Scripts", "python.exe")

def run_scraper():
    """Run the Twitter scraper with the virtual environment"""
    logging.info(f"Starting Twitter scraper at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Direct command without -m flag
        cmd = f'"{VENV_PYTHON}" scraper/__main__.py --tweets=50'
        
        # Run the command
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=SCRIPT_DIR
        )
        
        # Log output and errors
        stdout, stderr = process.communicate(timeout=300)  # 5 minutes timeout
        
        if process.returncode != 0:
            logging.error(f"Error running scraper: {stderr}")
        else:
            logging.info("Scraper completed successfully")
    
    except subprocess.TimeoutExpired:
        logging.warning("Scraper timed out after 5 minutes")
    except Exception as e:
        logging.error(f"Error running scraper: {str(e)}")

def main():
    """Run the Twitter scraper every 60 seconds"""
    logging.info("Starting Twitter scraper scheduler")
    
    # Check if virtual environment exists
    if not os.path.exists(VENV_PYTHON):
        logging.error(f"Virtual environment not found at: {VENV_PYTHON}")
        logging.error("Please make sure the virtual environment is set up correctly")
        return
    
    try:
        while True:
            run_scraper()
            logging.info("Waiting 60 seconds before next run...")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main() 