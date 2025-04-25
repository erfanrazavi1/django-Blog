from locust import HttpUser, task


class MyUser(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            data={"email": "erfan6235@gmail.com", "password": "123"},
        )
        if response.status_code == 200:
            response = response.json()
            self.client.headers = {
                "Authorization": f'Bearer {response.get("access",None)}'
            }
        else:
            print("Login failed")

    @task
    def post_list(self):
        self.client.get("/blog/api/v1/post/")
