from discord.ext.commands import Bot, Cog

from Cupidv3Bot.extensions.dispatcher import dispatcher
from CupidV3Database.matchingdb import Profile
from CupidV3Database.moderationdb import Case
from CupidV3Database.guildconfiguration import GuildConfig
from CupidV3Database.levelsdb import Level




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

    @dispatcher.listen(event_name='level_up')
    async def case_create(level:Level):
        config = await GuildConfig.get_record(level.guild_id)
        if config.subscribed_events.level_up:
            channels = [dispatcher.bot.get_channel(cid) for cid in config.subscribed_events.level_up]
            for channel in channels:
                await channel.send(content=f'<@{level.user_id}>',embed=level.level_up_embed)
    
    @dispatcher.listen(event_name="profile_update")
    async def profile_update(profile_id:int):
        profile, _ = await Profile.get_profile(profile_id)
        channel = dispatcher.bot.get_channel(1307474634559459360)
        await channel.send(embed=profile.embed)



    @dispatcher.listen(event_name='config_guild_create')
    async def case_create(new_config:GuildConfig):
        print("new config created")
        

    
    



async def setup(bot:Bot):
    await bot.add_cog(DispatchListener(bot))