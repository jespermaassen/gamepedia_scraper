import mwclient
import pandas as pd
import numpy as np

from statistics import mean, mode
import datetime

from utils.statistics import team_stats, average_gametime, team_versus_team_averages
from utils.fetch_odds import fetch_oddspedia

# Make sure the DataFrame prints are not cut of
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


def extract_cargoquery(response):
    data = response.get("cargoquery")

    df = pd.DataFrame(columns=get_cargoquery_columns(response))
    for i in data:
        x = pd.DataFrame.from_dict(i.get("title"), orient="index").transpose()
        df = pd.concat([df, x])

    return df


def get_cargoquery_columns(response):
    return response.get("cargoquery")[0].get("title").keys()


def get_scoreboards(tables, fields, where, order_by):
    site = mwclient.Site("lol.gamepedia.com", path="/")
    response = site.api(
        "cargoquery",
        limit="max",
        tables=tables,
        fields=fields,
        where=where,
        order_by=order_by,
    )

    # Convert the response into a pandas DataFrame
    df = extract_cargoquery(response)
    # Remove the useless datetime column
    df = df.drop("DateTime UTC__precision", axis=1)
    # Set the correct datetime column as the index
    df = df.set_index("DateTime UTC")

    windragons = []
    winbarons = []
    winkills = []
    wingold = []
    lossdragons = []
    lossbarons = []
    losskills = []
    lossgold = []

    for index, row in df.iterrows():
        if row.Winner == "1":
            windragons.append(row.Team1Dragons)
            winbarons.append(row.Team1Barons)
            winkills.append(row.Team1Kills)
            wingold.append(row.Team1Gold)

            lossdragons.append(row.Team2Dragons)
            lossbarons.append(row.Team2Barons)
            losskills.append(row.Team2Kills)
            lossgold.append(row.Team2Gold)

        elif row.Winner == "2":
            windragons.append(row.Team2Dragons)
            winbarons.append(row.Team2Barons)
            winkills.append(row.Team2Kills)
            wingold.append(row.Team2Gold)

            lossdragons.append(row.Team1Dragons)
            lossbarons.append(row.Team1Barons)
            losskills.append(row.Team1Kills)
            lossgold.append(row.Team1Gold)

    df["WinDragons"] = list(map(int, windragons))
    df["LossDragons"] = list(map(int, lossdragons))
    df["WinBarons"] = list(map(int, winbarons))
    df["LossBarons"] = list(map(int, lossbarons))
    df["WinKills"] = list(map(int, winkills))
    df["Losskills"] = list(map(int, losskills))
    df["WinGold"] = list(map(int, wingold))
    df["LossGold"] = list(map(int, lossgold))

    try:
        df["TotalDragons"] = df.Team1Dragons.astype(int) + df.Team2Dragons.astype(int)
    except:
        pass

    try:
        df["TotalBarons"] = df.Team1Barons.astype(int) + df.Team2Barons.astype(int)
    except:
        pass

    try:
        df["TotalKills"] = df.Team1Kills.astype(int) + df.Team2Kills.astype(int)
    except:
        pass

    try:
        df["TotalGold"] = df.Team1Gold.astype(int) + df.Team2Gold.astype(int)
    except:
        pass

    df = df.drop(
        [
            "Team1Dragons",
            "Team2Dragons",
            "Team1Barons",
            "Team2Barons",
            "Team1Kills",
            "Team2Kills",
            "Team1Gold",
            "Team2Gold",
        ],
        axis=1,
    )

    return df


queryfields = "ScoreboardGames.DateTime_UTC, \
                ScoreboardGames.Tournament, \
                ScoreboardGames.Team1, \
                ScoreboardGames.Team2, \
                ScoreboardGames.Winner, \
                ScoreboardGames.Team1Dragons, \
                ScoreboardGames.Team2Dragons, \
                ScoreboardGames.Team1Barons, \
                ScoreboardGames.Team2Barons, \
                ScoreboardGames.Team1Kills, \
                ScoreboardGames.Team2Kills, \
                ScoreboardGames.Team1Gold, \
                ScoreboardGames.Team2Gold, \
                ScoreboardGames.Gamelength, "

df = get_scoreboards(
    tables="ScoreboardGames",
    fields=queryfields,
    where="ScoreboardGames.Tournament = 'LCS 2020 Summer'",
    order_by="ScoreboardGames.DateTime_UTC",
)

odds = fetch_oddspedia(league="LCS")
team1_odds = []
team2_odds = []


for index, row in df.iterrows():
    date = pd.to_datetime(index).date()
    date2 = date - datetime.timedelta(days=1)
    date3 = date + datetime.timedelta(days=1)

    team1 = row.Team1
    team2 = row.Team2

    if team1 == "Rogue (European Team)":
        team1 = "Rogue"
    if team2 == "Rogue (European Team)":
        team2 = "Rogue"

    if team1 == "FC Schalke 04 Esports":
        team1 = "Schalke 04"
    if team2 == "FC Schalke 04 Esports":
        team2 = "Schalke 04"

    if team1 == "Misfits Gaming":
        team1 = "Misfits"
    if team2 == "Misfits Gaming":
        team2 = "Misfits"

    if team1 == "Excel Esports":
        team1 = "exceL"
    if team2 == "Excel Esports":
        team2 = "exceL"

    if team1 == "Evil Geniuses.NA":
        team1 = "Evil Geniuses"
    if team2 == "Evil Geniuses.NA":
        team2 = "Evil Geniuses"

    if team1 == "Counter Logic Gaming":
        team1 = "CLG"
    if team2 == "Counter Logic Gaming":
        team2 = "CLG"

    if team1 == "Dignitas":
        team1 = "Team Dignitas"
    if team2 == "Dignitas":
        team2 = "Team Dignitas"

    try:
        odds.date = pd.to_datetime(odds.date)
        matching_game = odds[
            (odds.team1.isin([team1, team2]))
            & (odds.team2.isin([team2, team1]))
            & (odds.date.astype(str).isin([str(date), str(date2), str(date3)]))
        ]
        team1_odd = matching_game.team1_odd.iat[0]
        team2_odd = matching_game.team2_odd.iat[0]

        team1_odds.append(team1_odd)
        team2_odds.append(team2_odd)

    except:
        team1_odds.append("0")
        team2_odds.append("0")

df["Team1Odd"] = team1_odds
df["Team2Odd"] = team2_odds
