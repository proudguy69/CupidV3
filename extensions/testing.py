from discord.ext.commands import Context, Bot, Cog, command
from discord import Member, TextChannel

from database.guildconfiguration import GuildConfig, ChannelPostingConfig, Posting


# just commands to test

class Testing(Cog):

    @command("setup_channel")
    async def setup_channel(self, ctx:Context, channel:TextChannel, action:str, type:str): # ?setup_channel #channel add cases
        guild = ctx.guild
        guild_config = await GuildConfig.get_record(guild.id)
        
        if not channel.id in guild_config.channel_configurations:
            # create a new config for this channel
            new_config = ChannelPostingConfig(channel.id)
            if action == "add":
                if type == "cases":
                    new_config.add_posting(Posting.cases)
                    await guild_config.update({"$set":{f"channels":new_config.data}})
                    await ctx.send(f"Added \"posting_cases\" rule to {channel.mention}\n(this means any case that gets updated or made will be posted here)")
                


        




async def setup(bot:Bot):
    await bot.add_cog(Testing())