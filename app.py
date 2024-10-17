import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

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
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    # Vérification du format de l'email
    if '@' not in email or '.' not in email.split('@')[-1]:
        flash("Format d'email invalide, veuillez réessayer.")
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == email), None)
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Email non trouvé, veuillez réessayer.")
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Quelque chose s'est mal passé, veuillez réessayer.")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    places_required = int(request.form['places'])

    if club and competition:
        
        if places_required < 0:
            flash("Le nombre de places ne peut pas être négatif.")
        elif places_required > 12:
            flash("Vous ne pouvez pas réserver plus de 12 places !")
        elif places_required > int(competition['numberOfPlaces']):
            flash("Pas assez de places disponibles pour ce concours.")
        elif places_required > int(club['points']):
            flash("Vous n'avez pas assez de points.")
        else:
            
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
            club['points'] = int(club['points']) - places_required
            flash("Super, réservation terminée !")
    return render_template('welcome.html', club=club, competitions=competitions) 

@app.route('/publicClubPoints')
def publicClubPoints():
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.context_processor
def inject_future_competitions():
    future_competitions = [comp for comp in competitions if datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S") > datetime.now()]
    return dict(future_competitions=future_competitions)

if __name__ == "__main__":
    app.run(debug=True)