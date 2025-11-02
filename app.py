from flask import Flask, render_template, request
import pandas as pd
from analysis import get_venue_insights, get_prediction

app = Flask(__name__)

# Load dataset
df = pd.read_csv('dataset/ipl.csv')

# Dropdown options
venues = sorted(df['venue'].dropna().unique())
teams = sorted(set(df['team1'].dropna().unique()) | set(df['team2'].dropna().unique()))

@app.route('/', methods=['GET', 'POST'])
def index():
    insights = None
    prediction = None

    if request.method == 'POST':
        mode = request.form['mode']
        venue = request.form['venue']
        team1 = request.form['team1']
        team2 = request.form['team2']
        toss_winner = request.form.get('toss_winner', None)
        toss_decision = request.form.get('toss_decision', None)

        if mode == 'insight':
            insights = get_venue_insights(df, venue, team1, team2)
        else:
            prediction = get_prediction(df, venue, team1, team2)

    return render_template('index.html',
                           venues=venues,
                           teams=teams,
                           insights=insights,
                           prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
