#               Импорт не служебных модулей
import logging
import pandas
import random
from discord import Embed
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"Duels"}
#

class Duels:
    def __init__(self,self2):
        self.self2=self2
        self.duelsDict={}
        self.topPositions={}
        for item in self.self2.config.duels_topPositions.split(","):
            item=item.split(":")
            self.topPositions[int(item[0])]=item[1]
        topLineList=self.self2.config._replics["duelsTopLine"].split("\:/")
        self.topLine={
            "name":topLineList[0],
            "value":topLineList[1],
            }
    async def run(self,id,command,channel,colour,args):
        if command in self.self2.config.duels_shotAliases: # выстрел
            await self.shot(id,channel,args)
        elif len(args)!=0:
            if args[0] in self.self2.config.duels_consentAliases: # принять
                await self.consent(id,channel,args)
            elif args[0] in self.self2.config.duels_rejectionAliases: # отказ
                await self.rejection(id,channel,args)
            elif args[0] in self.self2.config.duels_topAliases: # топ
                await self.top(id,channel,colour,args)
            elif len(args)>1 and f"{args[0]} {args[1]}" in self.self2.config.duels_personalInfoAliases: # моя стата
                await self.personalInfo(id,channel,args)
            else: # инвайт
                await self.invite(id,channel,args)
    async def _append(self,authorID,id,name):
        self.duelsDict[authorID]={
            "opponent"      :   id,
            "status"        :   "wait",
            "name"          :   name,
            "shot"          :   False,
            "count_shots"   :   0,
        }
        self.duelsDict[id]={
            "opponent"      :   authorID,
            "status"        :   "sended",
            "name"          :   name,
            "shot"          :   False,
            "count_shots"   :   0,
        }
    async def _remove(self,id,channel,noConsent=None):
        if noConsent:
            await channel.send(self.self2.config._replics["duelsNoAnswer"].format(
                user=f"<@!{self.duelsDict[id]['opponent']}>",
                user2=f"<@!{id}>",
            ))
            log.info(f"{self.duelsDict[id]['opponent']} не ответил на запрос {id}.",extra=extra)
            # не принял запрос на дуэль
        del self.duelsDict[self.duelsDict[id]["opponent"]]
        del self.duelsDict[id]
    async def _firstShot(self,id):
        if random.randint(0,1):
            self.duelsDict[id]["shot"]=True
            return id
        else:
            self.duelsDict[self.duelsDict[id]["opponent"]]["shot"]=True
            return self.duelsDict[id]["opponent"]
    async def _win(self,id,channel,noShot=None):
        if noShot:
            if self.duelsDict[id]["shot"] is True:
                id=self.duelsDict[id]["opponent"]
            await channel.send(self.self2.config._replics["duelsNoShot"].format(
                user=f"<@!{id}>",
                user2=f"<@!{self.duelsDict[id]['opponent']}>",
            ))
            # не произвел выстрела
        else:
            await channel.send(self.self2.config._replics["duelsShotWin"].format(
                user=f"<@!{id}>",
                user2=f"<@!{self.duelsDict[id]['opponent']}>",
            ))
            # победа
        log.info(f"{id} победил пользователя {self.duelsDict[id]['opponent']}.",extra=extra)
        duelsCSV=await self.csv(id,True)
        duelsCSV.loc[id,"wins"]+=1
        duelsCSV.loc[self.duelsDict[id]["opponent"],"loses"]+=1
        duelsCSV.to_csv("db/duels.csv",sep=",")
        await self.self2.iEconomy.add(id,self.self2.config.duels_moneyWin)
        await self.self2.iEconomy.add(self.duelsDict[id]["opponent"],self.self2.config.duels_moneyLose)
        await self._remove(id,channel)
    async def _draw(self,id,channel):
        duelsCSV=await self.csv(id,True)
        duelsCSV.loc[id,"draws"]+=1
        duelsCSV.loc[self.duelsDict[id]["opponent"],"draws"]+=1
        duelsCSV.to_csv("db/duels.csv",sep=",")
        await channel.send(self.self2.config._replics["duelsDraw"].format(
            user=f"<@!{id}>",
            user2=f"<@!{self.duelsDict[id]['opponent']}>",
        ))
        log.info(f"У {id} ничья с {self.duelsDict[id]['opponent']}.",extra=extra)
        await self._remove(id,channel)
    async def csv(self,id=None,iCSV=None,item=None,top=None):
        duelsCSV=pandas.read_csv("db/duels.csv",sep=",")
        duelsCSV.set_index("id",inplace=True)
        notInDuelsCSV=[]
        if iCSV:
            for _id in [id,self.duelsDict[id]["opponent"]]:
                if not _id in duelsCSV.index:
                    notInDuelsCSV.append([_id,0,0,0])
            notInDuelsCSV=pandas.DataFrame(notInDuelsCSV,columns=["id","wins","loses","draws"])
            notInDuelsCSV.set_index("id",inplace=True)
            duelsCSV=duelsCSV.append(notInDuelsCSV)
            return duelsCSV
        else:
            if not id in duelsCSV.index:
                notInDuelsCSV.append([id,0,0,0])
                notInDuelsCSV=pandas.DataFrame(notInDuelsCSV,columns=["id","wins","loses","draws"])
                notInDuelsCSV.set_index("id",inplace=True)
                duelsCSV=duelsCSV.append(notInDuelsCSV)
                duelsCSV.to_csv("db/duels.csv",sep=",")
            if item:
                if item is list:
                    items={}
                    for key in item:
                        items[key]=duelsCSV.loc[id,key]
                    return items
                else:
                    return duelsCSV.loc[id,item]
            elif top:
                return duelsCSV
            else:
                return {
                    "wins"  :   duelsCSV.loc[id,"wins"],
                    "loses" :   duelsCSV.loc[id,"loses"],
                    "draws" :   duelsCSV.loc[id,"draws"],
                }
    #   принять
    async def consent(self,id,channel,args):
        error=True
        if id in self.duelsDict and self.duelsDict[id]["status"]=="sended":
            error=False
        else:
            await channel.send(self.self2.config._replics["duelsNullConsent"].format(
                user=f"<@!{id}>"
            ))
            # нет запросов на дуэль
        if not error:
            await self.self2.iGlobalTimer.remove(self.duelsDict[id]["name"])
            self.duelsDict[id]["status"]="playing"
            self.duelsDict[self.duelsDict[id]["opponent"]]["status"]="playing"
            await self.shot(id,channel,[])
    #   отказаться
    async def rejection(self,id,channel,args):
        error=True
        if id in self.duelsDict:
            if self.duelsDict[id]["status"]!="playing":
                error=False
            else:
                await channel.send(self.self2.config._replics["duelsEscape"].format(
                    user=f"<@!{self.duelsDict[id]['opponent']}>",
                    user2=f"<@!{id}>",
                ))
                # сдался
        else:
            await channel.send(self.self2.config._replics["duelsNullRejection"])
            # нет запросов на дуэль
        if not error:
            await self.self2.iGlobalTimer.remove(self.duelsDict[id]["name"])
            log.info(f"{id} отказался от дуэли с {self.duelsDict[id]['opponent']}.",extra=extra)
            await self._remove(id,channel)
            await channel.send(self.self2.config._replics["duelsRejection"].format(
                user=f"<@!{id}>",
            ))
            # отказ от дуэли
    #   топ
    async def top(self,id,channel,colour,args):
        duelsCSV=await self.csv(id,top=True)
        duelsCSV=duelsCSV.sort_values(by="wins",ascending=False)
        embed=Embed(colour=colour,title=self.self2.config._replics["duelsTopTitle"])
        for position,id in zip(range(1,len(duelsCSV.index)+1),duelsCSV.index):
            if position>self.self2.config.duels_topLines:
                break
            if position in self.topPositions:
                position=f"{self.topPositions[position]} #{position}"
            else:
                position=f"#{position}"
            try:
                member=(await self.self2.guilds[0].fetch_member(id)).display_name
            except:
                member=self.self2.config._replics["duelsTopNoneUser"]
            embed.add_field(
                name=self.topLine["name"].format(
                    position=position,
                    user=member,
                ),
                value=self.topLine["value"].format(
                    wins=duelsCSV.loc[id,"wins"],
                    draws=duelsCSV.loc[id,"draws"],
                    loses=duelsCSV.loc[id,"loses"],
                ),
                inline=False,
                )
        await channel.send(embed=embed)
    #   моя стата
    async def personalInfo(self,id,channel,args):
        stat=await self.csv(id)
        await channel.send(self.self2.config._replics["duelsStatistics"].format(
            user=f"<@!{id}>",
            wins=stat["wins"],
            draws=stat["draws"],
            loses=stat["loses"],
        ))
    #   выстрел
    async def shot(self,id,channel,args):
        error=True
        if id in self.duelsDict:
            if self.duelsDict[id]["status"]=="playing":
                if not self.duelsDict[id]["shot"] is False is self.duelsDict[self.duelsDict[id]["opponent"]]["shot"]:
                    if self.duelsDict[id]["shot"] is True:
                        error=False
                    else:
                        await channel.send(self.self2.config._replics["duelsQueue"].format(
                            user=f"<@!{self.duelsDict[id]['opponent']}>",
                        ))
                        # не ваш черед стрелять
                else:
                    firstUser=await self._firstShot(id)
                    await self.self2.iGlobalTimer.add(self.self2.config.duels_timeShot,self._win(id,channel,True),self.duelsDict[id]["name"])
                    await channel.send(self.self2.config._replics["duelsConsent"].format(
                        user=f"<@!{id}>",
                        user2=f"<@!{self.duelsDict[id]['opponent']}>",
                        firstUser=f"<@!{firstUser}>",
                    ))
                    log.info(f"{id} принял запрос от {self.duelsDict[id]['opponent']}! Первый выстрел - {firstUser}.",extra=extra)
            else:
                await channel.send(self.self2.config._replics["duelsNoConsent"])
                # оппонент не принял дуэль
        else:
            await channel.send(self.self2.config._replics["duelsNoDuel"])
            # вы не в дуэли
        if not error:
            await self.self2.iGlobalTimer.remove(self.duelsDict[id]["name"])
            if not random.randint(0,self.self2.config.duels_shotChance): # победа
                await self._win(id,channel)
            else: # промах
                self.duelsDict[id]["count_shots"]+=1
                self.duelsDict[self.duelsDict[id]["opponent"]]["count_shots"]+=1
                if self.duelsDict[id]["count_shots"]==self.self2.config.duels_draw:
                    await self._draw(id,channel) # ничья
                    return
                self.duelsDict[id]["shot"]=False
                self.duelsDict[self.duelsDict[id]["opponent"]]["shot"]=True
                await self.self2.iGlobalTimer.add(self.self2.config.duels_timeShot,self._win(id,channel,True),self.duelsDict[id]["name"])
                await channel.send(self.self2.config._replics["duelsShotLose"].format(
                    user=f"<@!{id}>",
                    user2=f"<@!{self.duelsDict[id]['opponent']}>",
                ))
    #   инвайт
    async def invite(self,authorID,channel,args):
        error=True
        if len(args[0])==22:
            try:
                id=int(args[0][3:-1])
                ids=set()
                self.self2.guilds[0].fetch_member(id)
                if not id==authorID:
                    if not id==self.self2.user.id:
                        if not id in self.duelsDict:
                            if not authorID in self.duelsDict:
                                error=False
                            else:
                                if self.duelsDict[authorID]["status"]=="sended":
                                    await channel.send(self.self2.config._replics["duels1PAlreadyRequest"].format(
                                        user=f"<@!{self.duelsDict[authorID]['opponent']}>",
                                    ))
                                    # вам уже послали запрос на дуэль
                                elif self.duelsDict[authorID]["status"]=="wait":
                                    await channel.send(self.self2.config._replics["duels1PAlreadySendRequest"].format(
                                        user=f"<@!{self.duelsDict[authorID]['opponent']}>",
                                    ))
                                    # вы уже послали запрос на дуэль
                                else:
                                    await channel.send(self.self2.config._replics["duels1PAlreadyIn"].format(
                                        user=f"<@!{authorID}>",
                                        user2=f"<@!{self.duelsDict[authorID]['opponent']}>",
                                    ))
                                    # вы уже в дуэли
                        else:
                            if self.duelsDict[id]["status"]=="sended":
                                await channel.send(self.self2.config._replics["duels2PAlreadyRequest"].format(
                                    user=f"<@!{id}>",
                                    user2=f"<@!{self.duelsDict[id]['opponent']}>",
                                ))
                                # пользователю уже послали запрос на дуэль
                            elif self.duelsDict[id]["status"]=="wait":
                                await channel.send(self.self2.config._replics["duels2PAlreadySendRequest"].format(
                                    user=f"<@!{id}>",
                                ))
                                # пользователь уже послал запрос на дуэль другому игроку
                            else:
                                await channel.send(self.self2.config._replics["duels2PAlreadyIn"].format(
                                    user=f"<@!{id}>",
                                ))
                                # пользователь уже в дуэли
                    else:
                        await channel.send(self.self2.config._replics["duelsSendBot"])
                        # бот не может быть соперником
                else:
                    await channel.send(self.self2.config._replics["duelsSendMyself"])
                    # вы не можете начать дуэль с собой
            except:
                await channel.send(self.self2.config._replics["duelsUserNotFound"])
                # пользователь не найден
        else:
            await channel.send(self.self2.config._replics["duelsUserNotFound"])
            # пользователь не найден
        if not error:
            name=await self.self2.iGlobalTimer.random()
            await self._append(authorID,id,name)
            await self.self2.iGlobalTimer.add(self.self2.config.duels_timeConsent,self._remove(id,channel,True),name)
            await channel.send(self.self2.config._replics["duelsInvite"].format(
                user=f"<@!{authorID}>",
                user2=f"<@!{self.duelsDict[authorID]['opponent']}>",
                consentTime=self.self2.config.duels_timeConsent,
            ))
            log.info(f"{authorID} послал запрос пользователю {id}.",extra=extra)
