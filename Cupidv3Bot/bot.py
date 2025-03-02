from discord.ext.commands import Bot, Context, is_owner
from discord import Intents, utils
import logging

from extensions.dispatcher import dispatcher

from settings import TOKEN

class Cupidv3(Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=Intents.all())
        utils.setup_logging()
        self.logger = logging.getLogger('CupidV3')
        self.extns = ["extensions.moderation", "extensions.testing", "extensions.dispatchlistener", "extensions.levels"]
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


bot = Cupidv3()

@bot.command()
@is_owner()
async def reload(context:Context):
    await bot.reload_all()
    await context.send("Done reloading all extensions!")

bot.run(TOKEN)