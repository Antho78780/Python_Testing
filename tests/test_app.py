from app import app


class TestClassCodeStatus:
    club= "Simply Lift"
    competition = "Spring Festival"
    places = 5

    def test_home(self):
        response = app.test_client().get("/")
        assert response.status_code == 200

    def test_display(self):
        response = app.test_client().get("/display")
        assert response.status_code == 200
    
    def test_email(self):
        email_request = "test@gmail.com"
        response = app.test_client().post("/showSummary", data={"email": email_request})
        assert response.status_code == 200
    
    def test_url(self):
        response = app.test_client().get(f'/book/{self.competition}/{self.club}')
        assert response.status_code == 200
    
    def test_purchasePlaces(self):
        response = app.test_client().post("/purchasePlaces", data={"club": self.club, "competition": self.competition, "places": self.places})
        assert response.status_code == 200
    
    def test_logout(self):
        response = app.test_client().get("/logout")
        assert response.status_code == 302


