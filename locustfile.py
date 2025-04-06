from locust import HttpUser, task, between


class FastAPITestUser(HttpUser):
    wait_time = between(3, 5)  # 요청 간 대기 시간

    @task(1)
    def get_item(self):
        self.client.get(f"/items/")

    @task(1)  # POST 요청 실행
    def create_item(self):
        data = {"name": "Test Item", "description": "This is a test item."}
        self.client.post("/items/", json=data)
