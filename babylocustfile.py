from locust import HttUser, task

class BabyLocust(HttpUser):
    
    @task
    def baby_locust(self):
        self.client.get(":59898")