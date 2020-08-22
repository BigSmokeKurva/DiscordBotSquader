#               Импорт не служебных модулей
import discord as ds
#               Импорт служебных модулей
from _modules._configParser import ConfigParser
from _modules._events       import Events
from _modules._logging      import Logger
from _modules._globalTimer  import GlobalTimer
from _modules._commands     import Commands
#               Импорт функциональных модулей
from modules.antispam       import AntiSpam
from modules.serverStatus   import ServerStatus
from modules.admMSG         import AdmMSG
from modules.giveRoles      import GiveRoles
from modules.checks         import Checks
from modules.timeVoice      import TimeVoice
from modules.duels          import Duels
from modules.bdNullCheck    import NullCheck
from modules.levels         import Levels
from modules.statistics     import Statistics
from modules.economy        import Economy
from modules.buyrole        import BuyRole
from modules.PVC            import PersonalVoiceChannels
from modules.timeRoles      import TimeRoles
from modules.LaV_rewards    import LevelsAndVoiceRewards
from modules.music          import Music
#
print("""
██████╗░██╗░██████╗░░██████╗███╗░░░███╗░█████╗░██╗░░██╗███████╗██╗░░██╗██╗░░░██╗██████╗░██╗░░░██╗░█████╗░
██╔══██╗██║██╔════╝░██╔════╝████╗░████║██╔══██╗██║░██╔╝██╔════╝██║░██╔╝██║░░░██║██╔══██╗██║░░░██║██╔══██╗
██████╦╝██║██║░░██╗░╚█████╗░██╔████╔██║██║░░██║█████═╝░█████╗░░█████═╝░██║░░░██║██████╔╝╚██╗░██╔╝███████║
██╔══██╗██║██║░░╚██╗░╚═══██╗██║╚██╔╝██║██║░░██║██╔═██╗░██╔══╝░░██╔═██╗░██║░░░██║██╔══██╗░╚████╔╝░██╔══██║
██████╦╝██║╚██████╔╝██████╔╝██║░╚═╝░██║╚█████╔╝██║░╚██╗███████╗██║░╚██╗╚██████╔╝██║░░██║░░╚██╔╝░░██║░░██║
╚═════╝░╚═╝░╚═════╝░╚═════╝░╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝
""")
#
class Bot(ds.Client,Events):
    def __init__(self):
        #       other
        super().__init__()
        self.oneUse         =       True
        #       _modules
        self.iConfigParser  =       ConfigParser()
        self.config         =       self.iConfigParser.parser()
        self.iGlobalTimer   =       GlobalTimer()
        self.iCommands      =       Commands(self)
        #       modules
        self.iAntiSpam      =       AntiSpam(self)
        self.iServerStatus  =       ServerStatus(self)
        self.iGiveRoles     =       GiveRoles(self)
        self.iAdmMSG        =       AdmMSG(self)
        self.iChecks        =       Checks(self)
        self.iTimeVoice     =       TimeVoice(self)
        self.iDuels         =       Duels(self)
        self.iNullCheck     =       NullCheck(self)
        self.iLevels        =       Levels(self)
        self.iStatistics    =       Statistics(self)
        self.iEconomy       =       Economy(self)
        self.iBuyRole       =       BuyRole(self)
        self.iPVC           =       PersonalVoiceChannels(self)
        self.iTimeRoles     =       TimeRoles(self)
        self.iLaV           =       LevelsAndVoiceRewards(self)
        self.iMusic         =       Music(self)
    def _run(self):
        self.run(self.config.main_token)

if __name__ == "__main__":
    Logger()
    Bot()._run()