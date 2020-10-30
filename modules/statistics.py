#               Импорт не служебных модулей
import logging
from discord import Embed
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"Statistics"}
#

class Statistics:
    def __init__(self,self2):
        self.self2=self2
        self.fields=[]
        if len(self.self2.config._replics["statisticsFields"])!=0:
            for field in self.self2.config._replics["statisticsFields"].split("\,/"):
                self.fields.append(field)
        self.statuses={
            "offline"       :   "Оффлайн",
            "online"        :   "Онлайн",
            "idle"          :   "Не активен",
            "dnd"           :   "Не беспокоить",
            "invisible"     :   "Невидимый",
        }
        self.months={
            1   :   "января",
            2   :   "февраля",
            3   :   "марта",
            4   :   "апреля",
            5   :   "мая",
            6   :   "июня",
            7   :   "июля",
            8   :   "августа",
            9   :   "сентября",
            10  :   "октября",
            11  :   "ноября",
            12  :   "декабря",
        }
    async def statistic(self,authorID,channel,colour,args):
        if not len(args):
            id=authorID
            error=False
        else:
            id,error=await self.self2.iChecks.validArgsCheck(authorID,channel,args)
        if not error:
            member=await self.self2.guilds[0].fetch_member(id)
            embed=Embed(colour=colour,title=self.self2.config._replics["statisticsTitle"].format(
                user=member,
            ))
            # status
            print(member.status)
            status=self.statuses[str(member.status)]
            # duel
            duelStat=await self.self2.iDuels.csv(id,item=["wins","loses"])
            # level
            levelStat=await self.self2.iLevels.csv(id,item="level")
            # timevoice
            voiceStat=await self.self2.iTimeVoice.csv(id)
            # format
            if voiceStat//60!=0:
                timeFormat="Часов"
                voiceStat//=60
            else:
                timeFormat="Минут"
            # months
            if len(self.months[member.created_at.month])>3: # created
                cmonth=self.months[member.created_at.month][:3]+"." 
            else:
                cmonth=self.months[member.created_at.month]
            if len(self.months[member.joined_at.month])>3: # joined
                jmonth=self.months[member.joined_at.month][:3]+"." 
            else:
                jmonth=self.months[member.joined_at.month]
            # placeholders
            placeholders={
                "created"   :   str(member.created_at.day)+" "+cmonth+" "+str(member.created_at.year),
                "status"    :   status,
                "duelsWins" :   duelStat["wins"],
                "joined"    :   str(member.joined_at.day)+" "+jmonth+" "+str(member.joined_at.year),
                "level"     :   levelStat,
                "duelsLoses":   duelStat["loses"],
                "role"      :   member.roles[-1].mention,
                "format"    :   timeFormat,
                "voiceTime" :   voiceStat,
                "count"     :   int(await self.self2.iEconomy.csv(id)),
                "user"      :   member,
            }
            # title
            if self.self2.config._replics["statisticsTitle"]!="":
                embed.title=self.self2.config._replics["statisticsTitle"].format(**placeholders)
            # description
            if self.self2.config._replics["statisticsDescription"]!="":
                embed.description=self.self2.config._replics["statisticsDescription"].format(**placeholders)
            # field
            if self.fields!=[]:
                for field in self.fields:
                    field=field.format(**placeholders).split("\:/")
                    embed.add_field(name=field[0],value=field[1])
            # thumbnail
            embed.set_thumbnail(url=member.avatar_url)
            # send
            await channel.send(embed=embed)