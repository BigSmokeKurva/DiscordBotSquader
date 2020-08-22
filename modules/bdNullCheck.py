import logging
import pandas
import datetime
#
log=logging.getLogger("main")
extra={"moduleName":"bdNullCheck"}
#

class NullCheck:
    def __init__(self,self2):
        self.self2=self2
    async def check(self):
        async def removeChannel(id,channel):
            if await self.self2.iPVC._check(channel):
                channelsRemoved.add(channel)
                channel=self.self2.get_channel(channel)
                await channel.delete()
        duelsCSV=pandas.read_csv("db/duels.csv",sep=",")
        voiceCSV=pandas.read_csv("db/voice.csv",sep=",")
        levelsCSV=pandas.read_csv("db/levels.csv",sep=",")
        economyCSV=pandas.read_csv("db/economy.csv",sep=",")
        pvcCSV=pandas.read_csv("db/pvc.csv",sep=",")
        duelsCSV.set_index("id",inplace=True)
        voiceCSV.set_index("id",inplace=True)
        levelsCSV.set_index("id",inplace=True)
        economyCSV.set_index("id",inplace=True)
        pvcCSV.set_index("id",inplace=True)
        ids=set()
        notInServer=set()
        channelsRemoved=set()
        today=datetime.date.today()
        today=datetime.datetime(today.year,today.month,today.day)
        for member in self.self2.guilds[0].members:
            ids.add(member.id)
        for id in duelsCSV.index: # проверка duels.csv
            if not id in ids:
                duelsCSV=duelsCSV.drop(id)
                notInServer.add(id)
        for id in voiceCSV.index: # проверка voice.csv
            if not id in ids:
                voiceCSV=voiceCSV.drop(id)
                notInServer.add(id)
        for id in levelsCSV.index: # проверка levels.csv
            if not id in ids:
                levelsCSV=levelsCSV.drop(id)
                notInServer.add(id)
        for id in economyCSV.index: # проверка economy.csv
            if not id in ids:
                economyCSV=economyCSV.drop(id)
                notInServer.add(id)
        for id in pvcCSV.index: # проверка pvc.csv
            channel=pvcCSV.loc[id,"channel"]
            if not id in ids:
                await removeChannel(id,channel)
                pvcCSV=pvcCSV.drop(id)
                notInServer.add(id)
            else:
                dayremove=datetime.datetime.strptime(pvcCSV.loc[id,"dayremove"],'%Y-%m-%d')
                if dayremove<=today:
                    await removeChannel(id,channel)
        duelsCSV.to_csv("db/duels.csv",sep=",")
        voiceCSV.to_csv("db/voice.csv",sep=",")
        levelsCSV.to_csv("db/levels.csv",sep=",")
        economyCSV.to_csv("db/economy.csv",sep=",")
        pvcCSV.to_csv("db/pvc.csv",sep=",")
        log.info(f"С сервера удалены каналы - {', '.join(str(i) for i in channelsRemoved)}.",extra=extra)
        log.info(f"Из всех баз данных были удалены - {', '.join(str(i) for i in notInServer)}.",extra=extra)
        await self.self2.iGlobalTimer.add(self.self2.config.nullcheck_time,self.check())