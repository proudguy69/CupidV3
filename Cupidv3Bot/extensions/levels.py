from discord.ext.commands import Cog, Bot, Context, command
from discord import Message

from random import randint

from database.levelsdb import Level


class Levels(Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @Cog.listener(name="on_message")
    async def on_message(self, message:Message):
        author = message.author
        guild = message.guild
        if author.bot: return
        user_level = await Level.get_level(guild.id, author.id)
        ## we do calculateion, we will say 0 -> 50 for now
        random_xp = randint(1,50)
        await user_level.increase_xp(random_xp)
    

    @command(name='level', description='views your current level')
    async def level(self, ctx:Context):
        user_level = await Level.get_level(ctx.guild.id, ctx.author.id)
        embed, file = await user_level.get_rank_card(ctx.author.name, ctx.author.avatar.url)
        await ctx.send(file=file, embed=embed)
    


async def setup(bot:Bot):
    await bot.add_cog(Levels(bot))