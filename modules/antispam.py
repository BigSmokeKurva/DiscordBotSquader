#               Импорт не служебных модулей
import logging
#
log=logging.getLogger("main")
extra={"moduleName":"AntiSpam"}
#

class AntiSpam:
    def __init__(self,self2):
        self.spamDict={}
        self.self2=self2
    async def check(self,msg):
        async def delete():
            await msg.delete()
            log.info(f"Сообщение \"{msg.author}: {content}\" удалено!",extra=extra)
            return True
        error=False
        id=msg.author.id
        content=msg.content.lower()
        contentItem,*argsTemp=content.split(" ")
        if not contentItem[len(self.self2.config.main_commandPrefix):] in self.self2.config.antispam_spamBypass:
            if id in self.spamDict:
                if content in self.spamDict[id]:
                    error=await delete()
                else:
                    self.spamDict[id].append(content)
            else:
                self.spamDict.setdefault(id,[content])
            for keyword in self.self2.config.antispam_keywords:
                if content.count(keyword):
                    error=await delete()
            await self.self2.iGlobalTimer.add(self.self2.config.antispam_spamCooldown,self.remove(id,content))
        if not error:
            return True
    async def remove(self,id,content):
        self.spamDict[id].remove(content)