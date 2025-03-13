from discord.ext.commands import Bot, Context, is_owner
from discord import Intents, utils
import logging
import redis.asyncio as redis
from redis.asyncio.client import PubSub
import asyncio
import json
from threading import Thread

from Cupidv3Bot.extensions.dispatcher import dispatcher
from CupidV3Database.matchingdb import Profile

class Cupidv3(Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=Intents.all())
        utils.setup_logging()
        self.logger = logging.getLogger('CupidV3Bot.bot')
        self.extns = ["Cupidv3Bot.extensions.moderation", "Cupidv3Bot.extensions.testing", "Cupidv3Bot.extensions.dispatchlistener", "Cupidv3Bot.extensions.levels", "Cupidv3Bot.extensions.config"]
        dispatcher.set_bot(self)
    
    async def setup_hook(self):
        self.logger.info("Running setup_hook")
        for ext in self.extns:
            self.logger.info(f"loading extension: \"{ext}\"")
            await self.load_extension(ext)
        asyncio.create_task(self.start_redis())
        self.logger.info("Done Running setup_hook")
        

    
    async def reader(self, channel: PubSub):
        STOPWORD = "STOP"
        while True:
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message is None: continue
            if message.get('type') != 'message': continue
            if message.get('data', '') == STOPWORD: break
            await self.proccess_event(message)
    

    async def start_redis(self):
        r = redis.Redis(decode_responses=True)
        async with r.pubsub() as pubsub:
            await pubsub.subscribe("bot_channel")
            future = asyncio.create_task(self.reader(pubsub))
            await future
            await pubsub.close()


    async def proccess_event(self, message:dict):
        data:dict = json.loads(message.get('data'))
        event_name = data.get('event')
        match (event_name):
            case 'profile_update': await self.profile_update(data)
    
    async def profile_update(self, data:dict):
        submissions_channel = self.get_channel(1307474634559459360)
        profile, _ = await Profile.get_profile(data.get('profile_id'))
        profile_embed = profile.embed
        profile_embed.color = 0xFDFD96
        #return
        await submissions_channel.send(embed=profile_embed)

                



    
    async def reload_all(self):
        self.logger.info("Running reload_all")
        for ext in self.extns:
            self.logger.info(f"reloading extension: \"{ext}\"")
            await self.reload_extension(ext)


cupidbot = Cupidv3()

@cupidbot.command()
@is_owner()
async def reload(context:Context):
    await cupidbot.reload_all()
    await context.send("Done reloading all extensions!")



