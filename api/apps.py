from django.apps import AppConfig
import threading
import time
import random
import requests
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class PingService:
    def __init__(self, url, min_interval=5, max_interval=14):
        """
        Initialize the self-ping service
        
        :param url: The URL to ping
        :param min_interval: Minimum interval time (in minutes)
        :param max_interval: Maximum interval time (in minutes)
        """
        self.url = url
        self.min_interval = min_interval  # minutes
        self.max_interval = max_interval  # minutes
        self.is_running = False
        self.thread = None
    
    def start(self):
        """Start the ping service"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._ping_loop)
        self.thread.daemon = True  # Set as a daemon thread, so it exits when the main program exits
        self.thread.start()
        logger.info(f"Ping service started, will ping {self.url} every {self.min_interval}-{self.max_interval} minutes")
    
    def stop(self):
        """Stop the ping service"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1)
        logger.info("Ping service stopped")
    
    def _ping_loop(self):
        """Ping loop logic"""
        while self.is_running:
            try:
                wait_time = random.randint(self.min_interval, self.max_interval) * 60
                print(f"Preparing to wait {wait_time/60} minutes before pinging {self.url}")
                time.sleep(wait_time)
                
                response = requests.get(self.url, timeout=10)
                print(f"Pinged {self.url} successfully! Status code is {response.status_code}")
            except Exception as e:
                print(f"Ping failed, error: {str(e)}")

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'  # Replace with your app name
    
    def ready(self):
        """Called when the Django app is ready"""
        # Ensure this doesn't run during Django management commands (like migrate)
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0] or 'uvicorn' in sys.argv[0]:
            # App URL, replace with your actual URL
            app_url = 'https://anti-memo-frontend-test-11-20-2024.onrender.com/login'
            app_url2 = 'https://anti-memo-backend-test-11-20-2024.onrender.com/api/token/'
            
            # Create and start ping service
            ping_service = PingService(url=app_url, min_interval=5, max_interval=14)
            ping_service.start()
            
            # Create and start another ping service
            ping_service2 = PingService(url=app_url2, min_interval=5, max_interval=14)
            ping_service2.start()

# Use the above code in apps.py
# Then add this in __init__.py:
# default_app_config = 'myapp.apps.MyAppConfig'  # Replace 'myapp' with your app name