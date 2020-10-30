import logging
import discord.utils as utils
from discord import FFmpegPCMAudio
import youtube_dl
#
log=logging.getLogger("main")
extra={"moduleName":"Music"}
#

class Music:
    def __init__(self,self2):
        self.self2=self2
        ytdl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'default_search': "auto",
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            self.ytdl=ytdl
    async def run(self,msg):
        command,*args=msg.content.split(" ")
        command=command[len(self.self2.config.main_commandPrefix):].lower()

        channel =   msg.channel
        id      =   msg.author.id

        if command in self.self2.config.music_playAliases:
            await self.play(id,channel,args)
    async def startup(self): # При запуске
        channel=self.self2.get_channel(726396951792320593) ###
        self.voice=await channel.connect()
    async def play(self,id,channel,args): # !play
        if self.voice.is_playing():
            self.voice.stop()
        print(args)
        args="".join(args)
        video=await self.download(args)
        await channel.send(video["webpage_url"])




    async def download(self,args):
        print(type(args))
        if args.count("youtube.com"):
            ytInfo=self.ytdl.extract_info(args,download=False)
        else:
            #args=self.ytdl.extract_info(args,download=False)["id"]
            #print(self.ytdl.extract_info(args,download=False))
            ytInfo=self.ytdl.extract_info(args,download=False)["entries"][0]
        return ytInfo



    async def genEmbed(self):
        pass