#               Импорт не служебных модулей
import logging
import pandas
import discord.utils as utils
#
log=logging.getLogger("main")
extra={"moduleName":"TimeVoice"}
#

class TimeVoice:
    def __init__(self,self2):
        self.self2=self2
        self.money_rewards={}
        for items in self.self2.config.timevoice_moneyRewards.split(","):
            items=items.split(":")
            self.money_rewards[int(items[0])]=int(items[1])
        self.roles={}
        for item in self.self2.config.timevoice_rolesRewards.split(","):
            item=item.split(":")
            self.roles[int(item[0])]=float(item[1])
    async def voice(self,add=None):
        if add:
            channels=self.self2.guilds[0].voice_channels
            inVoice=set()
            for channel in channels:
                for member in channel.members:
                    inVoice.add(member.id)
            if self.self2.user.id in inVoice:
                inVoice.remove(self.self2.user.id)
            voiceCSV=await self.csv(inVoice=inVoice)
            if not voiceCSV is None:
                for id in inVoice:
                    member=utils.get(self.self2.guilds[0].members,id=id)
                    for role in member.roles:
                        if role.id in self.roles:
                            await self.self2.iEconomy.add(member.id,self.roles[role.id])
                    voiceCSV.loc[id,"time"]+=1
                    if voiceCSV.loc[id,"time"]%60==0:
                            await self.self2.iLaV.check(id)
                    if voiceCSV.loc[id,"time"]/60 in self.money_rewards:
                        count=voiceCSV.loc[id,"time"]//60
                        await self.self2.iEconomy.add(id,self.money_rewards[count])
                log.debug(voiceCSV,extra=extra)
                voiceCSV.to_csv("db/voice.csv",sep=",")
            log.debug(f"\n---\n{inVoice}\n---\n",extra=extra)
            log.debug(voiceCSV,extra=extra)
        await self.self2.iGlobalTimer.add(60,self.voice(True))
    async def csv(self,id=None,inVoice=None):
        #voiceCSV=pandas.read_csv("db/voice.csv",sep=",")
        #voiceCSV.set_index("id",inplace=True)
        #if inVoice:
        #    notInVoiceCSV=[]
        #    for id in inVoice:
        #        if not id in voiceCSV.index:
        #            notInVoiceCSV.append([id,0])
        #    if len(notInVoiceCSV):
        #        notInVoiceCSV=pandas.DataFrame(notInVoiceCSV,columns=["id","time"])
        #        notInVoiceCSV.set_index("id",inplace=True)
        #        voiceCSV=voiceCSV.append(notInVoiceCSV)
        #    return voiceCSV
        #else:
        #    if not id in voiceCSV.index:
        #        notInVoiceCSV=pandas.DataFrame([[id,0]],columns=["id","time"])
        #        notInVoiceCSV.set_index("id",inplace=True)
        #        voiceCSV=voiceCSV.append(notInVoiceCSV)
        #        voiceCSV.to_csv("db/voice.csv",sep=",")
        #    return voiceCSV.loc[id,"time"]
        ####
        voiceCSV=pandas.read_csv("db/voice.csv",sep=",")
        voiceCSV.set_index("id",inplace=True)
        notInVoiceCSV=[]
        if not inVoice is None:
            if len(inVoice)==0:
                return
            use=None
            for id in inVoice:
                if not id in voiceCSV.index:
                    notInVoiceCSV.append([id,0])
                    if not use:
                        use=True
            if use:
                notInVoiceCSV=pandas.DataFrame(notInVoiceCSV,columns=["id","time"])
                notInVoiceCSV.set_index("id",inplace=True)
                voiceCSV=voiceCSV.append(notInVoiceCSV)
            return voiceCSV
        else:
            if not id in voiceCSV.index:
                notInVoiceCSV=pandas.DataFrame([[id,0]],columns=["id","time"])
                notInVoiceCSV.set_index("id",inplace=True)
                voiceCSV=voiceCSV.append(notInVoiceCSV)
                voiceCSV.to_csv("db/voice.csv",sep=",")
            return voiceCSV.loc[id,"time"]