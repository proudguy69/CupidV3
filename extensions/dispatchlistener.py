from discord.ext.commands import Bot, Cog

from extensions.dispatcher import dispatcher
from database.moderationdb import Case
from database.guildconfiguration import GuildConfig




class DispatchListener(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
    
    ## need an easier way to handle dispatched events and posting logs
    
    @dispatcher.listen(event_name='cases_create')
    async def case_create(new_case:Case):
        config = await GuildConfig.get_record(new_case.guild_id)
        if config.subscribed_events.cases_create:
            channels = [dispatcher.bot.get_channel(cid) for cid in config.subscribed_events.cases_create]
            for channel in channels:
                await channel.send(embed=new_case.embed)



    @dispatcher.listen(event_name='config_guild_create')
    async def case_create(new_config:GuildConfig):
        print("new config created")
        

    
    



async def setup(bot:Bot):
    await bot.add_cog(DispatchListener(bot))