from app import app, loadClubs, loadCompetitions 
from flask_testing import TestCase 
from unittest.mock import patch, mock_open

class TestClass(TestCase): 

    clubs = loadClubs() 
    competitions = loadCompetitions() 

    foundClub = [c for c in clubs if c['name'] == "Simply Lift"][0] 
    foundCompetition = [c for c in competitions if c["name"] == "Fall Classic"][0]

    def create_app(self): 
        return app 

    def test_home(self): 
        response = self.create_app().test_client().get("/") 
        self.assert_template_used("index.html") 
        self.assert_context("clubs", self.clubs) 
        assert response.status_code == 200 

    def test_loadClubs(self):
        with patch("builtins.open", mock_open(
            read_data= '{"clubs":[{"name":"test","email":"test","points":"test"}]}'
            )):
            club = loadClubs()
            self.assertEqual(club, [{'name': 'test', 'email': 'test', 'points': 'test'}])

    def test_loadCompetitions(self):
        with patch("builtins.open", mock_open(
            read_data= '{"competitions":[{"name": "test", "date": "test", "numberOfPlaces": "test"}]}'
            )):
            competitions = loadCompetitions()
            self.assertEqual(competitions, [{"name": "test", "date": "test", "numberOfPlaces": "test"}])
                   
        
    def test_display(self): 
        response = self.create_app().test_client().get("/display") 
        self.assert_template_used("display.html") 
        self.assert_context("clubs", self.clubs) 
        assert response.status_code == 200 

    def test_email_validate(self): 
        response = self.create_app().test_client().post("/showSummary", data={"email": self.foundClub["email"]}) 
        self.assert_template_used("welcome.html")
        self.assert_context("competitions", self.competitions) 
        self.assert_context("club", self.foundClub) 
        assert response.status_code == 200 

 
    def test_errorEmail(self): 
        response = self.create_app().test_client().post("/showSummary", data={"email": "test@gmail.com"}) 
        self.assert_template_used("index.html") 
        self.assert_context("clubs", self.clubs) 
        assert response.status_code == 200 

 
    def test_url(self): 
        response = self.create_app().test_client().get(f'/book/{self.foundCompetition["name"]}/{self.foundClub["name"]}') 
        self.assert_template_used("booking.html") 
        self.assert_context("club", self.foundClub) 
        self.assert_context("competition", self.foundCompetition) 
        assert response.status_code == 200 

 
    def test_errorUrl(self): 
        response = self.create_app().test_client().get("/book/name_competition/name_club") 
        self.assert_template_used("welcome.html") 
        self.assert_context("club", "name_club") 
        self.assert_context("competitions", self.competitions) 
        assert response.status_code == 200 


    def test_purchasePlaces(self): 
        places_user = 5 
        self.foundClub["points"] = int(self.foundClub["points"]) 
        self.foundClub["points"] -= places_user 
        self.foundCompetition["numberOfPlaces"] = int(self.foundCompetition["numberOfPlaces"]) 
        self.foundCompetition["numberOfPlaces"] -= places_user 
        response = self.create_app().test_client().post(f"/purchasePlaces", data={"club": self.foundClub["name"], "competition": self.foundCompetition["name"], "places": places_user}) 
        self.assert_template_used("welcome.html") 
        self.assert_context("club", self.foundClub) 
        self.assert_context("competitions", self.competitions) 
        assert response.status_code == 200 


    def test_errorPurchasePlaces(self): 
        places_user = 30 
        self.foundClub["points"] = int(self.foundClub["points"]) 
        self.foundCompetition["numberOfPlaces"] = int(self.foundCompetition["numberOfPlaces"]) 

        response = self.create_app().test_client().post(f"/purchasePlaces", data={"club": self.foundClub["name"], "competition": self.foundCompetition["name"], "places": places_user}) 
        self.assert_template_used("booking.html") 
        self.assert_context("club", self.foundClub) 
        self.assert_context("competition", self.foundCompetition) 
        assert response.status_code == 200 


    def test_logout(self): 
        response = self.create_app().test_client().get("/logout") 
        assert response.request.path == "/logout"
        assert response.status_code == 302 