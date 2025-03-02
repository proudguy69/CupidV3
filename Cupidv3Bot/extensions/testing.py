from discord.ext.commands import Context, Bot, Cog, command
from discord import Member, TextChannel

from CupidV3Database.guildconfiguration import GuildConfig


# just commands to test

class Testing(Cog):

    def __init__(self):
        super().__init__()
    
    @command()
    async def subscribe(self, ctx:Context, channel:TextChannel, event:str):
        config = await GuildConfig.get_record(ctx.guild.id)
        state = await config.subscribe(channel.id, event)
        if not state:
            return await ctx.send(f"event \"{event}\" does not exists")
        await ctx.send(f"Subscribed {channel.mention} to {event}")

                


        




async def setup(bot:Bot):
    await bot.add_cog(Testing())