#               Импорт не служебных модулей
import logging
import asyncio
#
log=logging.getLogger("main")
extra={"moduleName":"Events"}
#

class Events:
    async def on_message(self,message):
        extra={"moduleName":"Chat"}
        if self.user.id!=message.author.id:
            if str(message.channel.type)!="private":
                if await self.iChecks.admCheck(message.author) or await self.iAntiSpam.check(message):
                    if await self.iLevels.levels(message):
                        if await self.iCommands.run_command(message):
                            log.info(f"{message.author.id}: {message.content}",extra=extra)
                            await self.iTimeRoles.check(message.author) # проверка TimeRoles
            else: # личное сообщение боту
                await message.channel.send(self.config._replics["messagePrivate"])
    async def on_ready(self):
        log.info(f"Подключенно - {self.user}",extra=extra)
        if self.oneUse:
            self.oneUse=False
            await asyncio.gather(
                self.iGlobalTimer.timer(),
                self.iServerStatus.update(),
                self.iTimeVoice.voice(),
                self.iNullCheck.check(),
                #self.iMusic.startup(),
                )
    async def on_raw_reaction_add(self,payload):
        if payload.message_id==self.config.giveroles_messageID and payload.user_id!=self.user.id:
            await self.iGiveRoles.add(payload)
    async def on_raw_reaction_remove(self,payload):
        if payload.message_id==self.config.giveroles_messageID and payload.user_id!=self.user.id:
            await self.iGiveRoles.remove(payload)
    async def on_voice_state_update(self,member,before,after):
        await self.iPVC.run(member,before,after)
    async def on_member_join(self,member):
        await member.send(self.config._replics["messageOnJoinPrivate"])
