from locust import TaskSet, task
from test_data import session_data, headers

class SessionRoutes(TaskSet):
    @task
    def test_health(self):
        self.client.get("/session/health")
        
    @task
    def test_get_all_tours(self):
        self.client.post(
            "/session/get-all-tours",
            json=session_data["tour_request"],
            headers=headers
        )

    @task
    def test_assign_tour(self):
        self.client.post(
            "/session/assign-tour-session", 
            json=session_data["assign_tour"],
            headers=headers
        )

    @task
    def test_get_tour_by_session(self):
        self.client.post(
            "/session/get-tour-by-session",
            json=session_data["tour_by_session"],
            headers=headers
        )
            
    @task
    def test_assign_client(self):
        self.client.post(
            "/session/assign-client-session",
            json=session_data["assign_client"],
            headers=headers
        )
            
    @task
    def test_get_sessions_in_tour(self):
        self.client.post(
            "/session/get-all-sessions-in-tour",
            json=session_data["sessions_in_tour"],
            headers=headers
        )

    @task
    def test_get_speakers(self):
        self.client.post(
            "/session/get-speakers-list",
            json={"session_id": session_data["session_code"]["session_id"]},
            headers=headers
        )
            
    @task
    def test_get_current_speaker(self):
        self.client.post(
            "/session/get-current-speaker",
            json={"session_id": session_data["session_code"]["session_id"]},
            headers=headers
        )
            
    @task
    def test_get_broadcast_history(self):
        self.client.post(
            "/session/get-broadcast-history",
            json={"session_id": session_data["session_code"]["session_id"]},
            headers=headers
        )
            
    @task
    def test_get_supported_languages(self):
        self.client.get(
            "/session/get-supported-languages",
            headers=headers
        )
        
    @task
    def test_set_rating(self):
        self.client.post(
            "/session/set-rating",
            json=session_data["rating"],
            headers=headers
        )
            
    @task
    def test_get_by_code(self):
        self.client.post(
            "/session/get-by-code",
            json=session_data["session_code"],
            headers=headers
        )
            
    @task
    def test_get_all_sessions(self):
        self.client.post(
            "/session/get-all-sessions",
            json=session_data["get_all_sessions"],
            headers=headers
        )
            
    @task
    def test_get_chat_in_session(self):
        self.client.post(
            "/session/get-chat-in-session",
            json=session_data["chat_request"],
            headers=headers
        )
            
    @task
    def test_get_checkpoints_tour(self):
        self.client.post(
            "/session/get-checkpoints-tour",
            json=session_data["get_checkpoints"],
            headers=headers
        )