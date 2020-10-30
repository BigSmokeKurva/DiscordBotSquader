#               Импорт не служебных модулей
import logging
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"GiveRoles"}
#

class GiveRoles:
    def __init__(self,self2):
        self.self2=self2
        self.roles={}
        for items in self.self2.config.giveroles_giveRolesDict.split(","):
            items=items.split(":")
            self.roles.setdefault(items[0],int(items[1]))
    async def add(self,payload):
        role=utils.get(self.self2.guilds[0].roles,id=self.roles[str(payload.emoji)])
        member=await self.self2.guilds[0].fetch_member(payload.user_id)
        log.info(f"{member.id} выдана роль {role}",extra=extra)
        await member.add_roles(role)
    async def remove(self,payload):
        role=utils.get(self.self2.guilds[0].roles,id=self.roles[str(payload.emoji)])
        member=await self.self2.guilds[0].fetch_member(payload.user_id)
        log.info(f"{member.id} удалена роль {role}",extra=extra)
        await member.remove_roles(role)