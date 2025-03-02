from discord.ext.commands import Bot, Context, is_owner
from discord import Intents, utils
import logging

from Cupidv3Bot.extensions.dispatcher import dispatcher

class Cupidv3(Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=Intents.all())
        utils.setup_logging()
        self.logger = logging.getLogger('CupidV3')
        self.extns = ["Cupidv3Bot.extensions.moderation", "Cupidv3Bot.extensions.testing", "Cupidv3Bot.extensions.dispatchlistener", "Cupidv3Bot.extensions.levels"]
        dispatcher.set_bot(self)
    
    async def setup_hook(self):
        self.logger.info("Running setup_hook")
        for ext in self.extns:
            self.logger.info(f"loading extension: \"{ext}\"")
            await self.load_extension(ext)
    
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