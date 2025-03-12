from discord.ext.commands import Bot, Context, is_owner
from discord import Intents, utils
import logging
import redis
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
        r = redis.Redis(host='localhost', port=6379)
        self.pubsub = r.pubsub()
        self.pubsub.subscribe("bot_channel")
    
    async def setup_hook(self):
        self.logger.info("Running setup_hook")
        for ext in self.extns:
            self.logger.info(f"loading extension: \"{ext}\"")
            await self.load_extension(ext)
        t = Thread(target=self.receive_messages, daemon=True)
        t.start()
        self.logger.info("Done setting up!")


    def receive_messages(self):
        for message in self.pubsub.listen():
            if message["type"] != "message": continue
            asyncio.run(self.proccess_event(message))

    async def proccess_event(self, message:dict):
        data:dict = json.loads(message.get('data'))
        event_name = data.get('event')
        match (event_name):
            case 'profile_update':
                print(data)
                profile_id = data.get('profile_id')
                profile, _ = await Profile.get_profile(profile_id)
                



    
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