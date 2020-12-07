
import requests
import pandas as pd
import numpy as np
import mwclient

from enums.cargoquery import *
from enums.leagues import *
from enums.teams import *

class DataCollector():
    """
    Data Collection class that connects to the gamepedia API over with mwclient
    """
    def __init__(self,  league: Leagues, year: str, event: str):
        # Setup client and constants
        self.site = mwclient.Site('lol.gamepedia.com', path='/')
        self.league = league[0]['events'][year][event]
        self.odds_url = league[0]['odds_url']

        # Get match results
        self.historical_results = self._get_historical_results()
        self.historical_results = self._expand_result_statistics()

    def _get_teams(self) -> None:
        """
        Checks which league/region is selected and assigns the Teams Enum accordingly
        """
        if self.league == League.lec:
            self.teams = LECTeams
        elif self.league == League.lcs:
            self.teams = LCSTeams
        elif self.league == League.lck:
            self.teams = LCKTeams
        else:
            raise ValueError(f'{self.league} has no teams Enum')
    
    def _get_historical_results(self) -> None:
        response = self.site.api("cargoquery",
                                limit="max",
                                tables="ScoreboardGames",
                                fields=Queryfields.as_str(),
                                where=f"ScoreboardGames.Tournament = '{self.league}'",
                                order_by="ScoreboardGames.DateTime_UTC")
        
        return self._extract_cargoquery(response)

    def _extract_cargoquery(self, response):
        data = response.get('cargoquery')

        df = pd.DataFrame(columns=self._get_cargoquery_columns(response))
        for i in data:
            x = pd.DataFrame.from_dict(i.get('title'), orient='index').transpose()
            df = pd.concat([df, x])

        # Remove useless datetime column, set correct column as index
        if 'DateTime UTC__precision' in df.columns:
            df = df.drop('DateTime UTC__precision', axis=1)
            df = df.set_index('DateTime UTC')
        
        return df

    def _expand_result_statistics(self):
        windragons = []
        winbarons  = []
        winkills   = []
        wingold    = []
        lossdragons = []
        lossbarons  = []
        losskills   = []
        lossgold    = []

        for index, row in self.historical_results.iterrows():
            if row.Winner == '1':
                windragons.append(row.Team1Dragons)
                winbarons.append(row.Team1Barons)
                winkills.append(row.Team1Kills)
                wingold.append(row.Team1Gold)

                lossdragons.append(row.Team2Dragons)
                lossbarons.append(row.Team2Barons)
                losskills.append(row.Team2Kills)
                lossgold.append(row.Team2Gold)

            elif row.Winner == '2':
                windragons.append(row.Team2Dragons)
                winbarons.append(row.Team2Barons)
                winkills.append(row.Team2Kills)
                wingold.append(row.Team2Gold)

                lossdragons.append(row.Team1Dragons)
                lossbarons.append(row.Team1Barons)
                losskills.append(row.Team1Kills)
                lossgold.append(row.Team1Gold)

        self.historical_results['WinDragons'] = list(map(int, windragons))
        self.historical_results['LossDragons'] = list(map(int, lossdragons))
        self.historical_results['WinBarons'] = list(map(int, winbarons))
        self.historical_results['LossBarons'] = list(map(int, lossbarons))
        self.historical_results['WinKills'] = list(map(int, winkills))
        self.historical_results['Losskills'] = list(map(int, losskills))
        self.historical_results['WinGold'] = list(map(int, wingold))
        self.historical_results['LossGold'] = list(map(int, lossgold))

        
        self.historical_results['TotalDragons'] = self.historical_results.Team1Dragons.astype(int) + self.historical_results.Team2Dragons.astype(int) 
        self.historical_results['TotalBarons'] = self.historical_results.Team1Barons.astype(int) + self.historical_results.Team2Barons.astype(int)  
        self.historical_results['TotalKills'] = self.historical_results.Team1Kills.astype(int) + self.historical_results.Team2Kills.astype(int)          
        self.historical_results['TotalGold'] = self.historical_results.Team1Gold.astype(int) + self.historical_results.Team2Gold.astype(int)
        
        # Drop the base Column that are not aware of winning vs losing team
        self.historical_results = self.historical_results.drop(['Team1Dragons', 'Team2Dragons', 'Team1Barons', 'Team2Barons', 'Team1Kills', 'Team2Kills', 'Team1Gold', 'Team2Gold'], axis=1)

        self._add_winner()

        return self.historical_results

    def _add_winner(self):
        self.historical_results["WinningTeam"] = np.where(self.historical_results["Winner"] == 1, self.historical_results['Team1'], self.historical_results['Team2'])

    def _get_cargoquery_columns(self, response):
        return response.get('cargoquery')[0].get('title').keys()
    
    def get_dataframe(self):
        return self.historical_results

    def get_odds(self) -> pd.DataFrame:
        raise DeprecationWarning("Odd URLS broken. fetching odds currently deprecated")
        df = pd.read_html(requests.get(self.odds_url).text)[0].dropna()

        historical_odds = pd.DataFrame()
        for index,row in df.iterrows():
            timestamp = str(row[0])[:5]

            if '2020' in row[0]:       
                date = row[0]

            if ':' in timestamp:
                if not 'date' in locals():
                    date = df.columns[0][0]
                teams = str(row[0][5:])

                for team in self.teams.all():
                    x = list(teams.partition(team)[1:])
                    x = list(filter(None, x))
                    if len(x) == 2:
                        outcome = x

                info = {'date': date, 'timestamp': timestamp, 'team1': outcome[0], 'team2': outcome[1], 'team1_odd': row[2], 'team2_odd': row[3]}
                info_df = pd.DataFrame.from_dict(info, orient='index').transpose()
                historical_odds = pd.concat([historical_odds, info_df]).reset_index(drop=True)
                historical_odds.date = pd.to_datetime(historical_odds.date)

        return historical_odds


class GameStatistics():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f'{self.data}'
    
    def avg_game_time(self):
        pass


if __name__ == '__main__':
    data = DataCollector(league=Leagues.worlds, year='2020', event='main').get_dataframe()
    
    

