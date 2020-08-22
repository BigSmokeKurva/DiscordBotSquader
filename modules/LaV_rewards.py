import logging
import datetime
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"LaV"}
#

class LevelsAndVoiceRewards:
    def __init__(self,self2):
        self.self2=self2
        self.roles=[]
        for item in self.self2.config.lav_roles.split(","):
            item=item.split(":")
            role=int(item[1])
            item=item[0].split("/")
            level=int(item[0])
            time=int(item[1])
            self.roles.append({
                "level" : level,
                "time"  : time,
                "role"  : role,
            })
    async def check(self,id):
        level   =   await self.self2.iLevels.csv(id,item='level')
        time    =   await self.self2.iTimeVoice.csv(id)//60
        for items in self.roles:
            if level>=items["level"] and time>=items["time"]:
                role    =   utils.get(self.self2.guilds[0].roles,id=items["role"])
                member  =   utils.get(self.self2.guilds[0].members,id=id)
                if not role in member.roles:
                    await member.add_roles(role)
                    log.info(f"{member.id} выдана роль {role}",extra=extra)