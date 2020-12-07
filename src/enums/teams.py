from enum import Enum

class LECTeams(Enum): 
    """
    Class containing enums for the all teams competing in the LEC
    """
    fnatic = 'Fnatic'
    origin = 'Origen'
    vitality = 'Team Vitality'
    sk_gaming = 'SK Gaming'
    g2_esports = 'G2 Esports'
    mad_lions = 'MAD Lions'
    schalke_04 = 'Schalke 04'
    excel = 'exceL'
    misfits = 'Misfits'
    rogue = 'Rogue'

    @staticmethod
    def all():
        return [e.value for e in LECTeams]

    def __str__(self):
        return str(self.value)

class LCSTeams(Enum): 
    """
    Class containing enums for the all teams competing in the LEC
    """
    flyquest = 'FlyQuest'
    evil_geniuses =  'Evil Geniuses'
    dignitas = 'Team Dignitas'
    cloud9 = 'Cloud9'
    immortals = 'Immortals'
    hundred_thieves = '100 Thieves'
    golden_guardians = 'Golden Guardians'
    tsm = 'Team SoloMid'
    clg = 'CLG'
    liquid = 'Team Liquid'

    @staticmethod
    def all():
        return [e.value for e in LCSTeams]

    def __str__(self):
        return str(self.value)


    