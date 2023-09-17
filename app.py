import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings
import plotly.express as px

warnings.filterwarnings('ignore', category=FutureWarning)


## Data from https://datahub.io/sports-data/spanish-la-liga#resource-spanish-la-liga_zip

seasons = [f"season-{i}{i+1}" for i in range(10, 19)]  
dataframes = []

for season in seasons:
    filename = f'spanish-la-liga_zip/data/{season}_csv.csv'
    
    try:
        temp_df = pd.read_csv(filename)
        temp_df['season'] = season 
        dataframes.append(temp_df)
    except FileNotFoundError:
        print(f"File for {season} not found!")

df = pd.concat(dataframes, ignore_index=True)
columns_to_keep = ['season','HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HTHG', 'HTAG', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC']
df = df[columns_to_keep]
print(df.head())

def compute_stat_per_game(df, team_column, stat_column, selected_team):
    team_df = df[df[team_column] == selected_team]
    total_stat = team_df[stat_column].sum()
    games = len(team_df)
    return round(total_stat / games, 2) if games != 0 else 0

def compute_team_stat(df, home_col, away_col, metric_function):
    home_stats = df.groupby('HomeTeam').agg({home_col: metric_function}).rename(columns={home_col: "Home"})
    away_stats = df.groupby('AwayTeam').agg({away_col: metric_function}).rename(columns={away_col: "Away"})
    
    total_stats = home_stats.add(away_stats, fill_value=0)

    total_stats['Total'] = total_stats['Home'] + total_stats['Away']

    return total_stats.sort_values(by='Total', ascending=False)



def main():
    sns.set_style("whitegrid")
    st.set_page_config(layout="wide", page_icon=":soccer:", page_title="La Liga Analysis")
    st.markdown("""
        <style>
            body {
                background-color: #ffffff;
            }
            .reportview-container .main .block-container {
                background-color: #ffffff;
                color: #000000;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("La Liga Analysis Over 10 Years")
    st.write("Analyze the performance of La Liga teams over the past decade using various statistics.")

    ### TEAM STATS ###
    st.subheader("Individual Team Statistics")
    st.write("View performance statistics for a selected team, differentiating between home and away games.")

    teams = df['HomeTeam'].unique()
    selected_team = st.selectbox("Select a Team to View Stats:", teams)

    stat_options = {
        "Goals per Game": [('HomeTeam', 'FTHG', 'AwayTeam', 'FTAG')],
        "Shots per Game": [('HomeTeam', 'HST', 'AwayTeam', 'AST')],
        "Fouls per Game": [('HomeTeam', 'HF', 'AwayTeam', 'AF')],
        "Halftime Goals per Game": [('HomeTeam', 'HTHG', 'AwayTeam', 'HTAG')],
        "Corners per Game": [('HomeTeam', 'HC', 'AwayTeam', 'AC')]
    }
    selected_stat = st.selectbox("Choose a Statistic to Display:", list(stat_options.keys()))

    home_column, home_stat, away_column, away_stat = stat_options[selected_stat][0]
    home_stat_value = compute_stat_per_game(df, home_column, home_stat, selected_team)
    away_stat_value = compute_stat_per_game(df, away_column, away_stat, selected_team)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{selected_stat} by {selected_team}")
        st.write(f"Home: {home_stat_value}")
        st.write(f"Away: {away_stat_value}")

    fig = px.bar(x=["Home", "Away"], y=[home_stat_value, away_stat_value],
                color=["Home", "Away"], labels={'y': selected_stat, 'x': 'Location'},
                title=f"{selected_stat} by {selected_team}")
    st.plotly_chart(fig)





    ### TEAM COMPARISON ###
    st.subheader("Comparison Across Teams")
    st.write("Compare the performance metrics of all teams. Choose a particular stat and a metric (mean, median, etc.) to visualize team-wide comparisons.")

    stat_options = {
        'Goals per game': ('FTHG', 'FTAG'),
        'Shots per game': ('HST', 'AST'),
        'Halftime goals per game': ('HTHG', 'HTAG'),
        'Fouls per game': ('HF', 'AF'),
    }

    metrics_options = {
        'Mean': 'mean',
        'Median': 'median',
        'Max': 'max',
        'Min': 'min'
    }

    selected_stat = st.selectbox("Select a Stat to View:", list(stat_options.keys()))
    selected_metric = st.selectbox("Select a Metric:", list(metrics_options.keys()))

    home_col, away_col = stat_options[selected_stat]
    metric_function = metrics_options[selected_metric]

    team_stats = compute_team_stat(df, home_col, away_col, metric_function)

    fig, ax = plt.subplots(figsize=(20, 10))
    fig.patch.set_facecolor('#ffffff')

    sns.barplot(x=team_stats.index, y=team_stats['Total'], ax=ax, palette="viridis")
    ax.set_title(f"{selected_stat} ({selected_metric}) for Each Team", color='white')
    ax.set_ylabel(selected_stat, color='white')
    ax.tick_params(axis='x', colors='white', rotation=45)
    ax.tick_params(axis='y', colors='white')

    st.pyplot(fig)






    ### GLOBAL STATS ###
    st.subheader("League-wide Statistics Per Season")
    st.write("Analyze the aggregate performance of all teams in La Liga season by season. You can view the absolute values or normalize them on a per-game basis.")

    stats_options = {
        'Total Goals': ('FTHG', 'FTAG'),
        'Total Shots': ('HST', 'AST'),
        'Halftime Goals': ('HTHG', 'HTAG'),
        'Total Fouls': ('HF', 'AF'),
    }
    selected_stat = st.selectbox("Select a Stat to View:", list(stats_options.keys()))

    mode_options = ["Absolute", "Per Game"]
    selected_mode = st.selectbox("Select a Mode:", mode_options)

    home_col, away_col = stats_options[selected_stat]

    if selected_mode == "Absolute":
        stats_per_season = df.groupby('season').apply(lambda x: x[home_col].sum() + x[away_col].sum())
        display_message = f"The season with the most {selected_stat.lower()} was {{}} with {{}} {selected_stat.lower()}."
    else:  
        stats_per_season = df.groupby('season').apply(lambda x: (x[home_col].sum() + x[away_col].sum()) / len(x))
        display_message = f"The season with the highest {selected_stat.lower()} per game was {{}} with an average of {{}} {selected_stat.lower()} per game."

    max_stat_season = stats_per_season.idxmax()
    st.write(display_message.format(max_stat_season, round(stats_per_season[max_stat_season], 2)))

    fig, ax1 = plt.subplots(figsize=(15, 5))
    fig.patch.set_facecolor('#ffffff')

    ax1.bar(stats_per_season.index, stats_per_season.values, color='blue')
    title = f"{selected_stat} per Season" if selected_mode == "Absolute" else f"{selected_stat} per Game per Season"
    ax1.set_title(title, color='white')
    ax1.set_xlabel("Season", color='white')
    ax1.set_ylabel(selected_stat, color='white')
    ax1.tick_params(axis='both', colors='white')

    st.pyplot(fig)


if __name__ == "__main__":
    main()
