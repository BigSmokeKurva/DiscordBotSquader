import logging
import pandas
from discord import Embed
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"Economy"}
#

class Economy:
    def __init__(self,self2):
        self.self2=self2
        self.topPositions={}
        for item in self.self2.config.duels_topPositions.split(","):
            item=item.split(":")
            self.topPositions[int(item[0])]=item[1]
        topLineList=self.self2.config._replics["economyTopLine"].split("\:/")
        self.topLine={
            "name":topLineList[0],
            "value":topLineList[1],
            }
    async def run(self,id,command,channel,colour,args):
        if command in self.self2.config.economy_balanceAliases:
            await self.balance(id,channel,args)
        elif command in self.self2.config.economy_topAliases:
            await self.top(id,channel,colour)
    async def balance(self,authorID,channel,args):
        if not len(args):
            id=authorID
            error=False
        else:
            id,error=await self.self2.iChecks.validArgsCheck(authorID,channel,args)
        if not error:
            if not len(args):
                await channel.send(self.self2.config._replics["economy1PBalance"].format(
                    count=int(await self.csv(id)),
                ))
            else:
                await channel.send(self.self2.config._replics["economy2PBalance"].format(
                    user=f"<@!{id}>",
                    count=int(await self.csv(id)),
                ))
    async def top(self,id,channel,colour):
        economyCSV=await self.csv(id,True)
        economyCSV=economyCSV.sort_values(by="balance",ascending=False)
        embed=Embed(colour=colour,title=self.self2.config._replics["economyTopTitle"])
        for position,id in zip(range(1,len(economyCSV.index)+1),economyCSV.index):
            if position>self.self2.config.levels_topLines:
                break
            if position in self.topPositions:
                position=f"{self.topPositions[position]} #{position}"
            else:
                position=f"#{position}"
            try:
                member=utils.get(self.self2.guilds[0].members,id=id).display_name
            except:
                member=self.self2.config._replics["economyTopNoneUser"]
            embed.add_field(
                name=self.topLine["name"].format(
                    position=position,
                    user=member,
                ),
                value=self.topLine["value"].format(
                    balance=int(economyCSV.loc[id,"balance"]),
                ),
                inline=False,
                )
        await channel.send(embed=embed)
    async def csv(self,id,csv=None):
        economyCSV=pandas.read_csv("db/economy.csv",sep=",")
        economyCSV.set_index("id",inplace=True)
        notInEconomyCSV=[]
        if not id in economyCSV.index:
            notInEconomyCSV.append([id,0])
            notInEconomyCSV=pandas.DataFrame(notInEconomyCSV,columns=["id","balance"])
            notInEconomyCSV.set_index("id",inplace=True)
            economyCSV=economyCSV.append(notInEconomyCSV)
        if csv:
            return economyCSV
        else:
            economyCSV.to_csv("db/economy.csv",sep=",")
            return economyCSV.loc[id,"balance"]
    async def add(self,id,value):
        economyCSV=await self.csv(id,True)
        if economyCSV.loc[id,"balance"]+value<0:
            economyCSV.loc[id,"balance"]=0
        else:
            economyCSV.loc[id,"balance"]+=value
        economyCSV.to_csv("db/economy.csv",sep=",")
    async def rolesRewards(self):

        await self.self2.iGlobalTimer.add(60,self.rolesRewards())
