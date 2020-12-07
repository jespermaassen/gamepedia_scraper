import pandas as pd

import io
import requests

url = 'https://oddspedia.com/esports/league-of-legends/lec/results/'
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url)

dfs = pd.read_html(r.text)
df = dfs[0]
df = df.dropna()

team_list = ['Fnatic',
            'Origen',
            'Team Vitality',
            'SK Gaming',
            'G2 Esports',
            'MAD Lions',
            'Schalke 04',
            'exceL',
            'Misfits',
            'Rogue']


final_df = pd.DataFrame()
for index,row in df.iterrows():
    timestamp = str(row[0])[:5]

    if '2020' in row[0]:
        date = row[0]

    if timestamp[3:] == '00':
        if not 'date' in locals():
            date = df.columns[0][0]
        teams = str(row[0][5:])

        for team in team_list:
            x = list(teams.partition(team)[1:])
            x = list(filter(None, x))
            if len(x) == 2:
                outcome = x

        team1 = outcome[0]
        team2 = outcome[1]

        team1_odd = row[2]
        team2_odd = row[3]

        info = {'date': date, 'timestamp': timestamp, 'team1': team1, 'team2': team2, 'team1_odd': team1_odd, 'team2_odd': team2_odd}
        info_df = pd.DataFrame.from_dict(info, orient='index').transpose()
        final_df = pd.concat([final_df, info_df])
        final_df = final_df.reset_index(drop=True)
        final_df.date = pd.to_datetime(final_df.date)


return final_df
print(final_df)

# for k, v in locals().items():
#     print(k)
#     print(v)