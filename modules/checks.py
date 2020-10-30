#               Импорт не служебных модулей
import logging
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"Checks"}
#

class Checks:
    def __init__(self,self2):
        self.self2=self2
        self.admRoles=[]
        self.admMembers=[]
        for role in self.self2.config.admcheck_admRoles.split(","):
            self.admRoles.append(int(role))
        for id in self.self2.config.admcheck_admMembers.split(","):
            self.admMembers.append(int(id))
    async def admCheck(self,member=None,id=None):
        if not member:
            member=self.self2.guilds[0].fetch_member(id)
        if not id:
            id=member.id
        if id in self.admMembers:
            return True
        for role in member.roles:
            if role.id in self.admRoles:
                return True
    async def validArgsCheck(self,authorID,channel,args):
        if len(args)!=0 and len(args[0])==22:
            try:
                id=int(args[0][3:-1])
                self.self2.guilds[0].fetch_member(id)
                if not id==self.self2.user.id:
                    return id,False
                else:
                    await channel.send(self.self2.config._replics["checksSendBot"]) ###
                    # у бота нет статистики
            except:
                await channel.send(self.self2.config._replics["checksUserNotFound"]) ###
                # не найден
        else:
            await channel.send(self.self2.config._replics["checksUserNotFound"]) ###
            # не найден
        return None,True