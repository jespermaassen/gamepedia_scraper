from enum import Enum

class Leagues():
    europe = {
        'odds_url': 'https://oddspedia.com/esports/league-of-legends/lec/results/',
        'events': {
            '2020': {
                'spring': 'LEC 2020 Spring',
                'summer': 'LEC 2020 Summer',
            },
            '2019': {
                'spring': 'LEC 2019 Spring',
                'summer': 'LEC 2019 Summer',
            },
            '2018': {
                'spring': 'EU LCS 2018 Spring',
                'summer': 'EU LCS 2018 Summer',
            },
            '2017': {
                'spring': 'EU LCS 2017 Spring',
                'summer': 'EU LCS 2017 Summer',
            }
        }
    },

    north_america = {
        'odds_url': 'https://google.com',
        'events': {
            '2020': {
                'spring': 'LCS 2020 Spring',
                'summer': 'LCS 2020 Summer',
            },
            '2019': {
                'spring': 'LCS 2019 Spring',
                'summer': 'LCS 2019 Summer',
            },
            '2018': {
                'spring': 'NA LCS 2018 Spring',
                'summer': 'NA LCS 2018 Summer',
            },
            '2017': {
                'spring': 'NA LCS 2017 Spring',
                'summer': 'NA LCS 2017 Summer',
            }
        }
    },

    worlds = {
        'odds_url': 'https://google.com',
        'events': {
            '2020': {
                'play-in': 'Worlds 2020 Play-in',
                'main': 'Worlds 2020 Main Event',
            },
            '2019': {
                'play-in': 'Worlds 2019 Play-in',
                'main': 'Worlds 2019 Main Event',
            },
            '2018': {
                'play-in': 'Worlds 2018 Play-in',
                'main': 'Worlds 2018 Event',
            }
        }
    },