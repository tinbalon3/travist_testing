from locust import TaskSet, task
from test_data import monitor_data, headers

class MonitorRoutes(TaskSet):
    @task
    def test_upload_tour(self):
        files = [('file', ('noise.wav', open('noise.wav', 'rb'), 'audio/wav'))]
        self.client.post(
            "/monitor/upload-new-tour",
            files=files,
            headers={"clientId": headers["clientId"]}
        )
            
    @task
    def test_create_tour(self):
        self.client.post(
            "/monitor/create-new-tour",
            json=monitor_data["new_tour"],
            headers=headers
        )
            
    @task
    def test_delete_tour(self):
        self.client.post(
            "/monitor/delete-tour-by-code",
            json=monitor_data["delete_tour"],
            headers=headers
        )
            
    @task
    def test_get_metrics(self):
        self.client.get(
            "/monitor/get-metrics",
            headers=headers
        )