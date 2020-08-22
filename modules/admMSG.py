#               Импорт не служебных модулей
import logging
from discord import Embed
#
log=logging.getLogger("main")
extra={"moduleName":"AdmMSG"}
#

class AdmMSG:
    def __init__(self,self2):
        self.self2=self2
        self.custom={}
        for item in self.self2.config.admmsg_custom.split("\,/"):
            item=item.split("\:/")
            self.custom[item[0]]=item[1]
    async def sendMSG(self,channel,args):
        if args[0]=="rolesmsg":
            msg=await channel.send(self.self2.config._replics["admmsgRolesMSG"])
            for emoji in self.self2.iGiveRoles.roles:
                await msg.add_reaction(emoji=emoji)
            self.self2.config=await self.self2.iConfigParser.edit("GiveRoles","message_id",str(msg.id))
        elif args[0]=="cmdduelsmsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgRulesDuelMSG"]))
        elif args[0]=="ruleschatmsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgRulesChatMSG"]))
        elif args[0]=="rulesvoicemsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgRulesVoiceMSG"]))
        elif args[0]=="welcomemsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgWelcomeMSG"]))
        elif args[0]=="cmdglobalmsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgCmdGlobalMSG"]))
        elif args[0]=="cmdmusicmsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgCmdMusicMSG"]))
        elif args[0]=="cmdmusicmsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgCmdMusicMSG"]))
        elif args[0]=="cmdhelpmsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgCmdHelpMSG"]))
        elif args[0]=="cmdbuyrolemsg":
            await channel.send(embed=await self.genEmbed(self.self2.config._replics["admmsgCmdBuyRoleMSG"],self.self2.config.admmsg_cmdBuyRoleImage))
        elif args[0] in self.custom:
            await channel.send(embed=await self.genEmbed(self.custom[args[0]]))
    async def genEmbed(self,msg,image=None):
        embed=Embed(title=None,description=msg,colour=0x363940)
        if not image is None:
            embed.set_image(url=image)
        return embed




