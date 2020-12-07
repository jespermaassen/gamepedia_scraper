from enum import Enum

class Queryfields(Enum):
    timestamp = 'ScoreboardGames.DateTime_UTC'
    tournament = 'ScoreboardGames.Tournament'
    team1 = 'ScoreboardGames.Team1'
    team2 = 'ScoreboardGames.Team2'
    winner = 'ScoreboardGames.Winner'
    team1_dragons = 'ScoreboardGames.Team1Dragons'
    team2_dragons = 'ScoreboardGames.Team2Dragons'
    team1_barons = 'ScoreboardGames.Team1Barons'
    team2_barons = 'ScoreboardGames.Team2Barons'
    team1_kills = 'ScoreboardGames.Team1Kills'
    team2_kills = 'ScoreboardGames.Team2Kills'
    team1_gold = 'ScoreboardGames.Team1Gold'
    team2_gold = 'ScoreboardGames.Team2Gold'
    gamelength = 'ScoreboardGames.Gamelength'

    @staticmethod
    def all():
        return [e.value for e in Queryfields]
    
    @staticmethod
    def as_str():
        return ','.join(Queryfields.all())