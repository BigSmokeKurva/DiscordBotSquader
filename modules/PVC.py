import logging
import pandas
import datetime
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"PVC"}
#

class PersonalVoiceChannels:
    def __init__(self,self2):
        self.self2=self2
        self.inProcess=set()
    async def run(self,member,before,after): # запуск
        error=True
        try:
            if after.channel.category_id==self.self2.config.pvc_category:
                error=False
        except:pass
        if not error:
            await self.connect(member,after)
    async def connect(self,member,voiceState): # коннект
        id=member.id
        if id in self.inProcess:
            return
        pvcCSV  =   await self.csv(id)
        channel =   int(pvcCSV.loc[id,"channel"])
        if voiceState.channel.id==self.self2.config.pvc_runChannel:
            self.inProcess.add(id)
            if not await self._check(channel,voiceState.channel.category):
                channel=await self.self2.guilds[0].create_voice_channel(
                    self.self2.config._replics["pvcNameChannel"].format(
                        user=member.display_name,
                    ),
                    category=voiceState.channel.category,
                    user_limit=self.self2.config.pvc_slots,
                    ) 
                await channel.set_permissions(member,manage_channels=True)
                log.info(f"Канал {channel.id} создан.",extra=extra)
            else:
                channel=self.self2.get_channel(channel)
            await member.move_to(channel)
            self.inProcess.remove(id)
            channel=channel.id
        if voiceState.channel.id==channel:
            today=datetime.date.today()
            today=datetime.datetime(today.year,today.month,today.day)
            dayremove=today+datetime.timedelta(self.self2.config.pvc_days) ###
            pvcCSV.loc[id,"channel"]    =       channel
            pvcCSV.loc[id,"dayremove"]  =       f"{dayremove.year}-{dayremove.month}-{dayremove.day}"
            pvcCSV.to_csv("db/pvc.csv",sep=",")
    async def _check(self,channel,category=None):
        if category is None:
            category=utils.get(self.self2.guilds[0].categories,id=self.self2.config.pvc_category)
        if channel:
            channel=self.self2.get_channel(channel)
            if channel in category.channels:
                return True # канал есть
            else:
                return False # канал удален
        else:
            return False # канал не создан
    async def kick(self,authorID,channelB,args): # кик
        id,error=await self.self2.iChecks.validArgsCheck(authorID,channelB,args)
        if not error:
            pvcCSV=await self.csv(authorID)
            channel=pvcCSV.loc[authorID,"channel"]
            lenChannel=len(str(channel))
            if lenChannel!=1:
                channel=self.self2.get_channel(channel)
                member=await self.self2.guilds[0].fetch_member(id)
                if member in channel.members:
                    await member.move_to(self.self2.get_channel(self.self2.config.pvc_runChannel))
                    await channelB.send(self.self2.config._replics["pvcKickSuccessfully"].format(
                        user=f"<@!{id}>",
                    ))
                    log.info(f"{authorID} кикнул {id} сщ своего канала.",extra=extra)
                else:
                    await channelB.send(self.self2.config._replics["pvcUserNoInChannel"])
                    # пользователь не в вашем канале
            else:
                await channelB.send(self.self2.config._replics["pvcNoChannel"])
                # у вас нет канала
    async def csv(self,id=None,index="id"):
        pvcCSV=pandas.read_csv("db/pvc.csv",sep=",")
        if index=="channel":
            drop=False
        else:
            drop=True
        pvcCSV.set_index(index,inplace=True,drop=drop)
        notInPVCCSV=[]
        if index=="id" and not id in pvcCSV.index:
            stub=str(datetime.datetime(2020,1,1)) ###
            notInPVCCSV.append([id,0,stub])
            notInPVCCSV=pandas.DataFrame(notInPVCCSV,columns=["id","channel","dayremove"])
            notInPVCCSV.set_index("id",inplace=True)
            pvcCSV=pvcCSV.append(notInPVCCSV)
        return pvcCSV