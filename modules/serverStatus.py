#               Импорт не служебных модулей
import logging
#
log=logging.getLogger("main")
extra={"moduleName":"ServerStatus"}
#

class ServerStatus:
    def __init__(self,self2):
        self.self2=self2
        self.use=True
    async def update(self):
        #log.debug("Start.",extra=extra)
        if self.use:
            self.use=False
            self.guild=self.self2.guilds[0]
            self.inVoiceChannel=self.guild.get_channel(self.self2.config.serverstatus_statusInVoice)
            self.inServerChannel=self.guild.get_channel(self.self2.config.serverstatus_statusInServer)
        try:
            inVoiceCount=0
            inServerCount=self.guild.member_count
            for channel in self.guild.voice_channels:
                inVoiceCount+=len(channel.members)
            await self.inVoiceChannel.edit(name=self.self2.config._replics["serverstatusInVoiceChannelName"].format(count=inVoiceCount))
            await self.inServerChannel.edit(name=self.self2.config._replics["serverstatusInServerChannelName"].format(count=inServerCount))
        except:
            self.use=True
            log.debug("Ошибка!",extra=extra)
        await self.self2.iGlobalTimer.add(self.self2.config.serverstatus_statusUpdate,self.update())
        #log.debug("Finish.",extra=extra)