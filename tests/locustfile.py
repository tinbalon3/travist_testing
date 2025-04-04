from locust import HttpUser, between
from test_conference import ConferenceRoutes
from test_authentication import AuthenticationRoutes  
from test_session import SessionRoutes
from test_monitor import MonitorRoutes
from test_streaming import StreamingRoutes

class ApiUser(HttpUser):
    """API test user class that simulates users accessing the API endpoints"""
    
    # Wait 1-5s between tasks
    wait_time = between(1, 5)
    
    # Define task sets with their relative weights
    tasks = {
        ConferenceRoutes: 2,    # Conference APIs - moderate load
        AuthenticationRoutes: 1, # Auth APIs - lower load
        SessionRoutes: 3,        # Session APIs - higher load
        MonitorRoutes: 1,        # Monitor APIs - lower load
        StreamingRoutes: 2       # Streaming APIs - moderate load 
    }
    
    def on_start(self):
        """Called when a User starts running"""
        # Any initialization code can go here
        pass