from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    # Define the wait time between tasks for each simulated user
    wait_time = between(1, 2)

    @task(2)  # Simulates loading the homepage
    def view_homepage(self):
        # Simulate a user visiting the homepage and check the response time
        with self.client.get("/", catch_response=True) as response:
            # If the response time exceeds 5 seconds, mark it as a failure
            if response.elapsed.total_seconds() > 5:
                response.failure("Loading time exceeded 5 seconds")

    @task(1)  # Simulates an update action making a booking
    def make_booking(self):
        # Simulate a user making a booking and check the response time
        with self.client.post("/purchasePlaces", data={"club": "Iron Temple", "competition": "Fall Classic", "places": "1"}, catch_response=True) as response:
            # If the update takes more than 2 seconds, mark it as a failure
            if response.elapsed.total_seconds() > 2:
                response.failure("Update took more than 2 seconds")
