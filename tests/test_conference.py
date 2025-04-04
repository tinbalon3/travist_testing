from locust import TaskSet, task
from test_data import conference_data, headers

class ConferenceRoutes(TaskSet):
    @task
    def test_single_shot(self):
        self.client.post(
            "/conference/get-single-shot-response", 
            json=conference_data["single_shot_request"],
            headers=headers
        )

    @task
    def test_history(self):
        self.client.post(
            "/conference/get-history-conversation",
            json=conference_data["history_request"],
            headers=headers
        )

    @task
    def test_assign_fb(self):
        self.client.post(
            "/conference/assign-fb-client",
            json=conference_data["assign_fb_request"],
            headers=headers
        )