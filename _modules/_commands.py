#               Импорт не служебных модулей
import logging
from discord import Embed ###
#
log=logging.getLogger("main")
extra={"moduleName":"Commands"}
#

class Commands:
    def __init__(self,self2):
        self.self2=self2
        self.aliasesList=[]
        for value in self.self2.config._aliases.values():
            self.aliasesList+=value
    async def run_command(self,msg):
        command,*args=msg.content.lower().split(" ")
        command=command[len(self.self2.config.main_commandPrefix):]
        if command in self.aliasesList:
            log.info(f"{msg.author.id} использовал команду {msg.content}",extra=extra)
            for key in self.self2.config._aliases:
                if command in self.self2.config._aliases[key]:
                    handler=getattr(self,key)
                    await handler(msg,command,args)
                    return
        else:
            return True
    #   AdmMSG
    async def command_admmsg(self,msg,command,args):
        if await self.self2.iChecks.admCheck(member=msg.author):
            await self.self2.iAdmMSG.sendMSG(msg.channel,args)
    #   Duels
    async def command_duels(self,msg,command,args):
        if msg.channel.id==self.self2.config.duels_channel:
            await self.self2.iDuels.run(msg.author.id,command,msg.channel,msg.author.colour,args)
    #   Levels
    async def command_levels(self,msg,command,args):
        await self.self2.iLevels.run(msg.author.id,command,msg.channel,msg.author.colour,args)
    #   Statistics
    async def command_statistics(self,msg,command,args):
        await self.self2.iStatistics.statistic(msg.author.id,msg.channel,msg.author.colour,args)
    #   Economy
    async def command_economy(self,msg,command,args):
        await self.self2.iEconomy.run(msg.author.id,command,msg.channel,msg.author.colour,args)
    #   BuyRole
    async def command_buyrole(self,msg,command,args):
        await self.self2.iBuyRole.buy(msg.author.id,msg.channel,args)
    #   PVCKick
    async def command_pvc_kick(self,msg,command,args):
        await self.self2.iPVC.kick(msg.author.id,msg.channel,args)
    #   Music
    async def command_music(self,msg,command,args):
        await self.self2.iMusic.run(msg)
    #   Dev commands
    async def command_dev(self,msg,command,args):
        if not msg.author.id in self.self2.config.dev_devolopers:
            return
        channel=msg.channel
        if command=="botping":
            await channel.send(int(self.self2.latency*1000))
        elif command=="bot":
            await channel.send("""
░██████╗░██████╗░██╗░░░██╗░█████╗░██████╗░███████╗██████╗░
██╔════╝██╔═══██╗██║░░░██║██╔══██╗██╔══██╗██╔════╝██╔══██╗
╚█████╗░██║██╗██║██║░░░██║███████║██║░░██║█████╗░░██████╔╝
░╚═══██╗╚██████╔╝██║░░░██║██╔══██║██║░░██║██╔══╝░░██╔══██╗
██████╔╝░╚═██╔═╝░╚██████╔╝██║░░██║██████╔╝███████╗██║░░██║
╚═════╝░░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝
                                     by ☑ βϊg₴₥∅ᶄě₭űŗ√ẫ ☑
""")
        elif command=="regaloh":
            await channel.send("""
██████╗░███████╗░██████╗░░█████╗░██╗░░░░░░█████╗░██╗░░██╗
██╔══██╗██╔════╝██╔════╝░██╔══██╗██║░░░░░██╔══██╗██║░░██║
██████╔╝█████╗░░██║░░██╗░███████║██║░░░░░██║░░██║███████║
██╔══██╗██╔══╝░░██║░░╚██╗██╔══██║██║░░░░░██║░░██║██╔══██║
██║░░██║███████╗╚██████╔╝██║░░██║███████╗╚█████╔╝██║░░██║
╚═╝░░╚═╝╚══════╝░╚═════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝
""")
        elif command=="bs":
            print(self.self2.get_all_members())