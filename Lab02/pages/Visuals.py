# This creates the page for displaying data visualizations.

import streamlit as st
import json
import plotly.express as px
import pandas as pd
import statistics
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json") as f:
    data = json.load(f)

st.header(data["title"])

names = []
points = []
wins = []

for team, stats in data["teams"].items():
    names.append(team)
    points.append(stats["points_per_game"])
    wins.append(stats["wins"])

fig = px.scatter(
    x=points,
    y=wins,
    hover_name=names,
    title="Points Per Game vs. Wins (2026)",
    labels={"x": "Points Per Game", "y": "Wins"},
)
st.plotly_chart(fig)

st.subheader("Compare Teams by Conference")

if "conference" not in st.session_state:
    st.session_state.conference = "Eastern"
st.radio("Choose a conference:", ["Eastern", "Western"], key="conference")

if "stat" not in st.session_state:
    st.session_state.stat = "points_per_game"
st.selectbox(
    "Choose a stat:",
    ["points_per_game", "rebounds_per_game", "assists_per_game"],
    key="stat",
)

bar_teams = []
bar_values = []

for team, stats in data["teams"].items():
    if stats["conference"] == st.session_state.conference:
        bar_teams.append(team)
        bar_values.append(stats[st.session_state.stat])
chart_data = pd.DataFrame({"Team": bar_teams, "Value": bar_values})
st.bar_chart(chart_data, x="Team", y="Value")
#Extra Credit: mean and median
avg = statistics.mean(bar_values)
mid = statistics.median(bar_values)

col1, col2 = st.columns(2)
col1.metric("Mean", round(avg, 1))
col2.metric("Median", round(mid, 1))
# PART 2: GRAPHS FROM data.csv
st.header("WNBA Fan Survey Results")

survey = pd.read_csv("data.csv")

team_counts = survey["favorite_team"].value_counts()

pie = px.pie(
    names=team_counts.index,
    values=team_counts.values,
    title="Favorite WNBA Teams Among Survey Takers",
)
st.plotly_chart(pie)

st.subheader("Favorite Teams of Dedicated Fans")

if "min_games" not in st.session_state:
    st.session_state.min_games = 0
st.slider("Minimum games watched:", 0, 30, key="min_games")

filtered = survey[survey["games_watched"] >= st.session_state.min_games]

if len(filtered) == 0:
    st.write("No fans watched that many games.")
else:
    st.bar_chart(filtered["favorite_team"].value_counts())
