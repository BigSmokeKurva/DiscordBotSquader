import logging
import discord.utils as utils
from discord import Embed
#
log=logging.getLogger("main")
extra={"moduleName":"BuyRole"}
#

class BuyRole:
    def __init__(self,self2):
        self.self2=self2
        self.roles={}
        for items in self.self2.config.buyrole_roles.split(","):
            items=items.split(":")
            self.roles[int(items[0])]=int(items[1])
        self.rolesList=[]
        for role in self.self2.config.buyrole_roles.split(","):
            role=role.split(":")
            self.rolesList.append(int(role[0]))
    async def buy(self,id,channel,args):
        error=True
        if len(args):
            try:
                args=int(args[0])-1
                roleDict={
                    "id"    :   self.rolesList[args],
                    "price" :   self.roles[self.rolesList[args]],
                }
                error=False
            except:
                await channel.send(self.self2.config._replics["buyroleNoRole"])
                # не найден номер роли
        else:
            await channel.send(self.self2.config._replics["buyroleNoArgs"])
            # укажите аргументы
        if not error:
            balance=await self.self2.iEconomy.csv(id)
            role=utils.get(self.self2.guilds[0].roles,id=roleDict["id"])
            member=self.self2.guilds[0].fetch_member(id)
            if balance>=roleDict["price"]:
                await self.self2.iEconomy.add(id,roleDict["price"]*-1)
                await member.add_roles(role)
                await channel.send(self.self2.config._replics["buyroleSuccessfully"].format(
                    role=role.mention,
                    price=roleDict["price"],
                ))
                log.info(f"{member.id} выдана роль {role}",extra=extra)
            else:
                await channel.send(self.self2.config._replics["buyroleNoMoney"].format(
                    count=(balance-roleDict["price"])*-1,
                    role=role.mention,
                ))
                # недостаточно денег