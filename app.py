import json
import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']  
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'
   
competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():

    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        flash("The email is not found")
        return render_template("index.html", clubs=clubs)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    date_now = datetime.datetime.now()
    date_tournament = datetime.datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    placesRequired = int(request.form['places'])
    club["points"] = int(club["points"])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])

    if placesRequired <= club["points"] and placesRequired > 0 and placesRequired <= competition["numberOfPlaces"] and date_tournament >= date_now and placesRequired <= 12:
        club["points"] -= placesRequired
        competition["numberOfPlaces"]-=placesRequired
        flash('Great-booking complete!') 
        return render_template('welcome.html', club=club, competitions=competitions) 
    else:
        flash("Something went wrong-please try again")
        return render_template("booking.html", club=club, competition=competition)

@app.route("/display")
def display():
    return render_template("display.html", clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))