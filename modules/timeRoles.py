import logging
import datetime
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"TimeRoles"}
#

class TimeRoles:
    def __init__(self,self2):
        self.self2=self2
        self.roles={}
        for items in self.self2.config.timeroles_roles.split(","):
            items=items.split(":")
            self.roles[int(items[0])]=int(items[1])
    async def check(self):
        today=datetime.datetime.today()
        for member in self.self2.guilds[0].members:
            days=(today-member.joined_at).days
            if days in self.roles:
                role=utils.get(self.self2.guilds[0].roles,id=self.roles[days])
                if not role in member.roles:
                    await member.add_roles(role)
                    log.info(f"{member.id} выдана роль {role}",extra=extra)
        await self.self2.iGlobalTimer.add(self.self2.config.timeroles_time,self.check())
