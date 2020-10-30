import logging
import pandas
import datetime
import discord.utils as utils
from discord import Embed
#
log=logging.getLogger("main")
extra={"moduleName":"Levels"}
#

class Levels:
    def __init__(self,self2):
        self.self2=self2
        self.oneUse=True
        self.topPositions={}
        for item in self.self2.config.duels_topPositions.split(","):
            item=item.split(":")
            self.topPositions[int(item[0])]=item[1]
        topLineList=self.self2.config._replics["levelsTopLine"].split("\:/")
        self.topLine={
            "name":topLineList[0],
            "value":topLineList[1],
            }
    async def run(self,id,command,channel,colour,args):
        if command in self.self2.config.levels_topAliases: # топ
            await self.top(id,channel,colour)
        elif command in self.self2.config.levels_personalInfoAliases: # level
            await self.personalInfo(id,channel,args)
    async def levels(self,msg):
        if self.oneUse:
            self.oneUse=False
            self.channel=self.self2.get_channel(self.self2.config.main_broudcastChannel)
        # read
        id=msg.author.id
        levelsCSV=await self.csv(id,True)
        content=msg.content
        user={
            "level"       :   levelsCSV.loc[id,"level"],
            "exp"         :   levelsCSV.loc[id,"exp"],
            "today"       :   datetime.datetime.strptime(levelsCSV.loc[id,"today"],'%Y-%m-%d'),
            "dayreset"    :   datetime.datetime.strptime(levelsCSV.loc[id,"dayreset"],'%Y-%m-%d'),
            "explimit"    :   levelsCSV.loc[id,"explimit"],
        }
        today=datetime.date.today()
        today=datetime.datetime(today.year,today.month,today.day)
        # write
        if len(content)>self.self2.config.levels_lenMsg:
            exp=0
            if user["dayreset"]<today: # dayreset
                user["dayreset"]=today+datetime.timedelta(self.self2.config.levels_lengthWeek)
                user["explimit"]=0
            if user["today"]!=today: # todaybonus
                exp+=self.self2.config.levels_todayBonus
                user["today"]=today
            exp+=self.self2.config.levels_expMsg
            if exp+user["explimit"]>self.self2.config.levels_weekLimit: # explimit
                exp-=exp+user["explimit"]-self.self2.config.levels_weekLimit
            user["exp"]+=exp
            user["explimit"]+=exp
            if user["exp"]>=self.self2.config.levels_newLvl: # newlvl
                user["exp"]-=self.self2.config.levels_newLvl
                user["level"]+=1
                await self.channel.send(self.self2.config._replics["levelsLevelUp"].format(
                    user=f"<@!{id}>",
                    lvl=user["level"],
                ))
                await self.self2.iEconomy.add(id,self.self2.config.levels_moneyLevelUp)
                log.info(f"{id} повысил уровень до {user['level']}.",extra=extra)
        # save
        levelsCSV.loc[id,"level"]   =       user["level"]
        levelsCSV.loc[id,"exp"]     =       user["exp"]
        levelsCSV.loc[id,"today"]   =       f"{user['today'].year}-{user['today'].month}-{user['today'].day}"
        levelsCSV.loc[id,"dayreset"]=       f"{user['dayreset'].year}-{user['dayreset'].month}-{user['dayreset'].day}"
        levelsCSV.loc[id,"explimit"]=       user["explimit"]

        levelsCSV.to_csv("db/levels.csv",sep=",")
        await self.self2.iLaV.check(id)
        return True
    async def csv(self,id,csv=None,item=None):
        levelsCSV=pandas.read_csv("db/levels.csv",sep=",")
        levelsCSV.set_index("id",inplace=True)
        notInLevelsCSV=[]
        if not id in levelsCSV.index:
            stub=str(datetime.date.today()+datetime.timedelta(self.self2.config.levels_lengthWeek))
            notInLevelsCSV.append([id,0,0,stub,stub,0])
            notInLevelsCSV=pandas.DataFrame(notInLevelsCSV,columns=["id","level","exp","today","dayreset","explimit"])
            notInLevelsCSV.set_index("id",inplace=True)
            levelsCSV=levelsCSV.append(notInLevelsCSV)
        if csv:
            return levelsCSV
        levelsCSV.to_csv("db/levels.csv",sep=",")
        if item:
            if item is list:
                items={}
                for key in item:
                    items[key]=levelsCSV.loc[id,key]
                return items
            else:
                return levelsCSV.loc[id,item]
        else:
            return {
                "level"     :   levelsCSV.loc[id,"level"],
                "exp"       :   levelsCSV.loc[id,"exp"],
                "today"     :   levelsCSV.loc[id,"today"],
                "dayreset"  :   levelsCSV.loc[id,"dayreset"],
                "explimit"  :   levelsCSV.loc[id,"explimit"],
            }
    async def top(self,id,channel,colour):
        levelsCSV=await self.csv(id,True)
        levelsCSV.to_csv("db/levels.csv",sep=",")
        levelsCSV=levelsCSV.sort_values(by="level",ascending=False)
        embed=Embed(colour=colour,title=self.self2.config._replics["levelsTopTitle"])
        for position,id in zip(range(1,len(levelsCSV.index)+1),levelsCSV.index):
            if position>self.self2.config.levels_topLines:
                break
            if position in self.topPositions:
                position=f"{self.topPositions[position]} #{position}"
            else:
                position=f"#{position}"
            try:
                member=(await self.self2.guilds[0].fetch_member(id)).display_name
            except:
                member=self.self2.config._replics["levelsTopNoneUser"]
            embed.add_field(
                name=self.topLine["name"].format(
                    position=position,
                    user=member,
                ),
                value=self.topLine["value"].format(
                    lvl=levelsCSV.loc[id,"level"],
                    exp=self.self2.config.levels_newLvl*levelsCSV.loc[id,"level"]+levelsCSV.loc[id,"exp"],
                ),
                inline=False,
                )
        await channel.send(embed=embed)
    async def personalInfo(self,authorID,channel,args):
        if not len(args):
            id=authorID
            error=False
        else:
            id,error=await self.self2.iChecks.validArgsCheck(authorID,channel,args)
        if not error:
            user=await self.csv(id)
            if len(args)==0:
                await channel.send(self.self2.config._replics["levels1PLevel"].format(
                    user=f"<@!{id}>",
                    lvl=user["level"],
                    count=5000-user["exp"],
                ))
            else:
                await channel.send(self.self2.config._replics["levels2PLevel"].format(
                    user=f"<@!{id}>",
                    lvl=user["level"],
                    count=5000-user["exp"],
                ))