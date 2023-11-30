import requests
from locust import HttpUser, task

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


class FastServePerfUser(HttpUser):
    @task
    def hello_world(self):
        data = {
            "prompt": "An astronaut riding a green horse",
            "negative_prompt": "ugly, blurry, poor quality",
        }
        base_url = self.client.base_url
        response = self.client.post("/endpoint", headers=headers, json=data)
        response.raise_for_status()
