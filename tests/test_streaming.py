from locust import TaskSet, task
from test_data import stream_paths, session_data, headers

class StreamingRoutes(TaskSet):
    @task
    def test_audio_stream(self):
        path = stream_paths["audio_stream"].format(
            session_id=session_data["session_code"]["session_id"],
            broadcast_id="latest",
            language="en"
        )
        self.client.get(
            path,
            stream=True,
            headers=headers
        )
        
    @task
    def test_session_playback(self):
        path = stream_paths["playback_stream"].format(
            session_id=session_data["session_code"]["session_id"]
        )
        self.client.get(
            path,
            stream=True,
            headers=headers
        )