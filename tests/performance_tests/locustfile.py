from locust import HttpUser, task

class projectPerfTest(HttpUser):

    @task
    def home(self):
        response = self.client.get("/")
    
    @task
    def display(self):
        response = self.client.get("/display")
    
    @task
    def logout(self):
        response = self.client.get("/logout")

    @task
    def login(self):
        response = self.client.post("/showSummary", {"email": "test@gmail.com"})
        
    @task
    def purchasePlaces(self):
        response = self.client.post("/purchasePlaces", {"club": "Simply Lift", "competition": "Spring Festival", "places": 5})
    
    @task
    def url(self):
        response = self.client.get("/book/Spring Festival/Simply Lift")