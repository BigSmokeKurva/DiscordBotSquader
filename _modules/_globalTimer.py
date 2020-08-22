#               Импорт не служебных модулей
import logging
import asyncio
import sys
import warnings
from random import shuffle
#
log=logging.getLogger("main")
extra={"moduleName":"Timer"}
#

class GlobalTimer:
    def __init__(self):
        self.timerDict={"time":0}
        if not sys.warnoptions:
            warnings.simplefilter("ignore")
    async def timer(self):
        while True:
            if self.timerDict["time"] in self.timerDict:
                asyncio.gather(*self.timerDict[self.timerDict["time"]].values())
                await self.remove(time=self.timerDict["time"])
            await asyncio.sleep(1)
            self.timerDict["time"]+=1
            #if self.timerDict["time"]%10==0:
            #    log.debug(self.timerDict,extra=extra)
    async def add(self,time,func,name=None):
        if not name:
            name=await self.random()
        time+=self.timerDict["time"]
        if time in self.timerDict:
            self.timerDict[time].setdefault(name,func)
        else:
            self.timerDict.setdefault(time,{name:func})
    async def remove(self,name=None,time=None):
        if time:
            del self.timerDict[self.timerDict["time"]]
        else:
            async def removeName(name):
                for key in self.timerDict:
                    if key!="time":
                        for keys in self.timerDict[key]:
                            if name in keys:
                                del self.timerDict[key][name]
                                return
            await removeName(name)
    async def random(self):
        abc=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9"]
        shuffle(abc)
        abc="".join(abc)
        return abc