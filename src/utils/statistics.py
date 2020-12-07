import mwclient
import pandas as pd
import numpy as np

from statistics import mean, mode

def average_gametime(df):
    gametimes = []
    for i in df.Gamelength.values:
        i = str(i.replace(":","."))
        i = float(i)
        gametimes.append(i)

    try:
        mean_gametimes = (round(mean(gametimes),2))
    except:
        mean_gametimes = np.nan

    return mean_gametimes

def teams_games(team, df):
    x = df[(df['Team1'] == team) | (df['Team2'] == team)]
    return x

def team_stats(teamname, df):
    # Returns a Dataframe with only the games played by the selected team
    df      = teams_games(teamname, df)
    # Prepare empty dataframe to collect statistics for selected team
    final_df = pd.DataFrame()

    for index, row in df.iterrows():
        if row.Team1 == teamname:
            opponent = row.Team2
            startdate = index
            if row.Winner == '1':
                result = 'won'

            elif row.Winner == '2':
                result = 'lost'

        elif row.Team2 == teamname:
            opponent = row.Team1
            if row.Winner == '2':
                result = 'won'

            elif row.Winner == '1':
                result = 'lost'

        if result == 'won':
            winning_dict = {'startdatetime': startdate,
                            'startdate': pd.to_datetime(startdate).date(),
                            'team': teamname,
                            'result': 'won',
                            'opponent': opponent,
                            'dragons': row.WinDragons,
                            'barons': row.WinBarons,
                            'kills': row.WinKills,
                            'gold': row.WinGold,
                            'Gamelength': row.Gamelength}

            winning_df = pd.DataFrame.from_dict(winning_dict, orient='index').transpose()
            final_df = pd.concat([final_df, winning_df])
        
        elif result == 'lost':
            losing_dict = {'startdatetime': startdate,
                            'startdate': pd.to_datetime(startdate).date(),
                            'team': teamname,
                            'result': 'lost',
                            'opponent': opponent,
                            'dragons': row.WinDragons,
                            'barons': row.WinBarons,
                            'kills': row.WinKills,
                            'gold': row.WinGold,
                            'Gamelength': row.Gamelength}

            losing_df = pd.DataFrame.from_dict(losing_dict, orient='index').transpose()
            final_df = pd.concat([final_df, losing_df])

    # final_df = final_df.set_index('startdate')
    final_df.reset_index(inplace = True, drop=True)
    return final_df

def team_versus_team_averages(team1, team2, df):
    team1_df = teams_games(team1, df)
    team2_df = teams_games(team2, df)

    team1_stats = team_stats(teamname='Fnatic', df=df)
    team2_stats = team_stats(teamname='G2 Esports', df=df)

    team1_wins = team1_stats[team1_stats.result == 'won']
    team1_losses = team1_stats[team1_stats.result == 'lost']

    team2_wins = team2_stats[team2_stats.result == 'won']
    team2_losses = team2_stats[team2_stats.result == 'lost']

    team1_dict = {'Name': team1,
                    'kills': team1_stats.kills.mean(),
                    'kills_when_winning': team1_wins.kills.mean(),
                    'kills_when_losing': team1_losses.kills.mean(),
                    'dragons': team1_stats.dragons.mean(),
                    'dragons_when_winning': team1_wins.dragons.mean(),
                    'dragons_when_losing': team1_losses.dragons.mean(),
                    'barons': team1_stats.barons.mean(),
                    'barons_when_winning': team1_wins.barons.mean(),
                    'barons_when_losing': team1_losses.barons.mean(),
                    'gamelength': average_gametime(team1_stats),
                    'gamelength_when_winning': average_gametime(team1_wins),
                    'gamelength_when_losing': average_gametime(team1_losses),
    }

    team2_dict = {'Name': team2,
                    'kills': team2_stats.kills.mean(),
                    'kills_when_winning': team2_wins.kills.mean(),
                    'kills_when_losing': team2_losses.kills.mean(),
                    'dragons': team2_stats.dragons.mean(),
                    'dragons_when_winning': team2_wins.dragons.mean(),
                    'dragons_when_losing': team2_losses.dragons.mean(),
                    'barons': team2_stats.barons.mean(),
                    'barons_when_winning': team2_wins.barons.mean(),
                    'barons_when_losing': team2_losses.barons.mean(),
                    'gamelength': average_gametime(team2_stats),
                    'gamelength_when_winning': average_gametime(team2_wins),
                    'gamelength_when_losing': average_gametime(team2_losses),
                    
    }

    team1_final = pd.DataFrame.from_dict(team1_dict, orient='index').transpose()
    team2_final = pd.DataFrame.from_dict(team2_dict, orient='index').transpose()

    final_df = pd.concat([team1_final, team2_final])

    return final_df