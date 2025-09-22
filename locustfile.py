from locust import HttpUser, task, between
import itertools

# Infinite counter
counter = itertools.count(1)

class EmailUser(HttpUser):
    wait_time = between(1, 3)  # simulate user think time

    @task
    def send_email(self):
        # Generate unique email
        email_id = next(counter)
        to_email = f"test{email_id}@example.com"

        payload = {
            "to": to_email,
            "subject": "Load Test Email",
            "context": {"body": f"This is test email number {email_id}"},
        }

        headers = {"x-api-key": "Testkey123"}

        self.client.post("/send-email", json=payload, headers=headers)