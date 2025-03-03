from discord import TextChannel
from discord.ext.commands import Bot, Cog, Context, command, Group, group

from CupidV3Database.guildconfiguration import GuildConfig


from enum import Enum

class Set(Enum):
    add = "add"
    remove = "remove"



class Config(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @group(name="configure", invoke_without_command = True)
    async def configure(self, ctx:Context):
        await ctx.reply("test!")


    @configure.command(name="channel", description="configures events for channels")
    async def channel(self, ctx:Context, set:str, channel:TextChannel, event:str):
        """adds / removes channels to events 
        Args:
            channel (TextChannel): the channel to configure
            set (Set): add or remove
            event (str): the event to add / remove from the channe
        """

        guild_config = await GuildConfig.get_record(ctx.guild.id)
        set = set.lower()
        event = event.lower()
        
        match (set):
            case 'add':
                success, msg = await guild_config.subscribe(event, channel.id)
            case 'remove':
                success, msg = await guild_config.unsubscribe(event, channel.id)
            case _:
                return await ctx.reply("set can only be \"add\" or \"remove\"")
        
        
        await ctx.reply(msg)
        

    @channel.error
    async def channel_err(self, ctx:Context, err):
        await ctx.send(f"```{err}```")


        

async def setup(bot:Bot):
    await bot.add_cog(Config(bot))