import pandas as pd
import matplotlib.pyplot as plt
import os

def get_venue_insights(df, venue, team1, team2):
    """Return analytical insight for given venue & teams"""
    venue_df = df[df['venue'] == venue]

    t1_wins = venue_df[venue_df['winner'] == team1].shape[0]
    t2_wins = venue_df[venue_df['winner'] == team2].shape[0]
    total = venue_df.shape[0]

    toss_wins = venue_df[venue_df['toss_winner'].notna()].shape[0]
    toss_effect = (venue_df[venue_df['toss_winner'] == venue_df['winner']].shape[0] / toss_wins * 100) if toss_wins > 0 else 0

    # Compute percentages
    t1_percent = round((t1_wins / total) * 100, 2) if total > 0 else 0
    t2_percent = round((t2_wins / total) * 100, 2) if total > 0 else 0

    # Generate bar graph
    chart_path = create_graph(team1, team2, t1_percent, t2_percent, venue)

    return {
        'venue': venue,
        'team1': team1,
        'team2': team2,
        'team1_wins': t1_wins,
        'team2_wins': t2_wins,
        'total_matches': total,
        'team1_percent': t1_percent,
        'team2_percent': t2_percent,
        'toss_effect': round(toss_effect, 2),
        'chart': chart_path
    }

def get_prediction(df, venue, team1, team2):
    """Return prediction-style output"""
    insights = get_venue_insights(df, venue, team1, team2)
    if insights['team1_wins'] > insights['team2_wins']:
        likely_winner = insights['team1']
        probability = round(insights['team1_percent'], 2)
    elif insights['team2_wins'] > insights['team1_wins']:
        likely_winner = insights['team2']
        probability = round(insights['team2_percent'], 2)
    else:
        likely_winner = "Uncertain (Equal performance)"
        probability = 50

    return f"🏆 Based on previous data at {venue}, {likely_winner} is more likely to win ({probability}% confidence)."


def create_graph(team1, team2, t1_percent, t2_percent, venue):
    """Create bar chart and save in static folder"""
    charts_dir = os.path.join('static', 'charts')
    os.makedirs(charts_dir, exist_ok=True)

    plt.figure(figsize=(5,4))
    plt.bar([team1, team2], [t1_percent, t2_percent], color=['gold', 'deepskyblue'])
    plt.title(f'Win Percentage at {venue}', fontsize=12, fontweight='bold')
    plt.ylabel('Win %')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    chart_file = f"{team1}_{team2}_chart.png".replace(" ", "_")
    chart_path = os.path.join(charts_dir, chart_file)
    plt.tight_layout()
    plt.savefig(chart_path, transparent=True)
    plt.close()

    return chart_file
