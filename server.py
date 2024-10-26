import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
    return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
    return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_summary', methods=['POST'])
def show_summary():
    email = request.form['email']

    if '@' not in email or '.' not in email.split('@')[-1]:
        flash("Format d'email invalide, veuillez réessayer.")
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == email), None)
    if club:
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )
    else:
        flash("Email non trouvé, veuillez réessayer.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = next((c for c in clubs if c['name'] == club), None)
    found_competition = next(
        (c for c in competitions if c['name'] == competition), None)

    if found_club and found_competition:
        return render_template(
            'booking.html',
            club=found_club,
            competition=found_competition
        )
    else:
        flash("Quelque chose s'est mal passé, veuillez réessayer.")
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = next(
        (c for c in competitions if c['name'] == request.form['competition']),
        None
    )
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    places_required = int(request.form['places'])

    if club is None:
        flash("Club non trouvé.")
        return redirect(url_for('index'))
    if competition is None:
        flash("Compétition non trouvée.")
        return redirect(url_for('index'))

    if places_required <= 0:
        flash("Le nombre de places doit être supérieur à zéro.")
    elif places_required > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places !")
        return redirect(url_for(
            'book',
            competition=competition['name'],
            club=club['name']
        ))
    elif places_required > int(competition['numberOfPlaces']):
        flash("Pas assez de places disponibles pour ce concours.")
        return redirect(url_for(
            'book',
            competition=competition['name'],
            club=club['name']
        ))
    elif places_required > int(club['points']):
        flash("Vous n'avez pas assez de points.")
        return redirect(url_for(
            'book',
            competition=competition['name'],
            club=club['name']
        ))
    else:
        competition['numberOfPlaces'] = int(
            competition['numberOfPlaces']
        ) - places_required
        club['points'] = int(club['points']) - places_required
        flash("Super, réservation terminée !")
        print(
            f"Places restantes: {competition['numberOfPlaces']}, "
            f"Points restants: {club['points']}"
        )

    return render_template(
        'welcome.html', club=club, competitions=competitions)


@app.route('/publicClubPoints')
def public_club_points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.context_processor
def inject_future_competitions():
    future_competitions = [
        comp for comp in competitions
        if datetime.strptime(
            comp['date'], "%Y-%m-%d %H:%M:%S"
            ) > datetime.now()
    ]
    return dict(future_competitions=future_competitions)


if __name__ == "__main__":
    app.run(debug=True)
