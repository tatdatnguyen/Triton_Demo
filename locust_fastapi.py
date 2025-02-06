from locust import HttpUser, task, between
import random

class InferenceUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8080"  # Explicitly define the host

    @task
    def infer_request(self):
        texts = ["This is a sample input", "Another test sentence", "BERT inference test"]
        payload = {"texts": random.sample(texts, 2)}

        headers = {"Content-Type": "application/json"}
        response = self.client.post("/infer", json=payload, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
