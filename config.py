import os
from dotenv import load_dotenv

# Load environment variables at import time
load_dotenv()

class Config:
    """Configuration settings from environment variables"""
    
    # Naukri Credentials
    NAUKRI_USERNAME = os.getenv('NAUKRI_USERNAME', 'ksai.revanth.22cse@bmu.edu.in')
    NAUKRI_PASSWORD = os.getenv('NAUKRI_PASSWORD', '8074097091')
    
    # API Keys
    TWOCAPTCHA_API_KEY = os.getenv('TWOCAPTCHA_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCX-8MEBVc-XsQb5iMaXwE6eXo5oSRotzo')
    
    # Search Settings
    JOB_SEARCH_QUERY = os.getenv('JOB_SEARCH_QUERY', 'ai-engineer-fresher')
    MAX_JOBS_PER_CYCLE = int(os.getenv('MAX_JOBS_PER_CYCLE', '10'))
    WAIT_TIME_MIN = int(os.getenv('WAIT_TIME_MIN', '5'))
    WAIT_TIME_MAX = int(os.getenv('WAIT_TIME_MAX', '10'))
    
    # Browser Settings
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    HEADLESS = False
    
    # User Agent to avoid detection
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    @classmethod
    def validate(cls):
        """Validate that all required environment variables are set"""
        required_keys = ['NAUKRI_USERNAME', 'NAUKRI_PASSWORD', 'GEMINI_API_KEY']
        
        missing = [key for key in required_keys if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
