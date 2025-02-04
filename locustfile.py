from locust import HttpUser, task, between

class TritonLoadTestUser(HttpUser):
    # Wait time between task executions (can be randomized if desired)
    wait_time = between(1, 3)  # Simulate user delay between requests

    @task
    def send_infer_request(self):
        # Triton server endpoint
        url = "http://localhost:8000/v2/models/bert/infer"

        # Payload for batch input texts
        payload = {
            "inputs": [
                {
                    "name": "text_input",
                    "shape": [4],  # Batch size of 4
                    "datatype": "BYTES",
                    "data": [
                        "What is your name?",
                        "How is the weather today?",
                        "Tell me about Triton server.",
                        "hello"
                    ]
                }
            ],
            "outputs": [
                {
                    "name": "output"
                }
            ]
        }

        # Send POST request to the Triton server
        response = self.client.post(url, json=payload)

        # Check the response status and parse results
        if response.status_code == 200:
            result = response.json()
            if "outputs" in result:
                predicted_labels = result["outputs"][0]["data"]
                print("Predicted labels:", predicted_labels)
            else:
                print("Error in response:", result.get("error", "Unknown error"))
        else:
            print("Request failed with status code:", response.status_code)


