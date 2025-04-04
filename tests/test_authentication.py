from locust import TaskSet, task
from test_data import auth_data, headers

class AuthenticationRoutes(TaskSet):
    @task
    def test_health(self):
        self.client.get("/authentication/health")

    @task
    def test_login(self):
        self.client.post(
            "/authentication/login-authentication",
            json=auth_data["login"],
            headers=headers
        )

    @task  
    def test_register(self):
        self.client.post(
            "/authentication/register-authentication",
            json=auth_data["register"],
            headers=headers
        )
            
    @task
    def test_guest_login(self):
        self.client.get(
            "/authentication/get-login-guest",
            headers=headers
        )
        
    @task
    def test_update(self):
        self.client.post(
            "/authentication/update-authentication",
            json=auth_data["update"],
            headers=headers
        )
            
    @task
    def test_google_login(self):
        self.client.get(
            "/authentication/google-login",
            headers=headers
        )
            
    @task  
    def test_google_callback(self):
        self.client.get(
            "/authentication/google-callback?code=test_code",
            headers=headers
        )

    @task
    def test_delete_account(self):
        self.client.post(
            "/authentication/delete-account",
            json=auth_data["delete"],
            headers=headers
        )