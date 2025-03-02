from discord.ext.commands import Context, Bot, Cog, command
from discord import Member

from CupidV3Database.moderationdb import Case, CaseType


class Moderation(Cog):

    @command("warn")
    async def warn(self, context:Context, member:Member, *reason:str):
        guild = context.guild
        moderator = context.author
        target = member
        reason = ' '.join(word for word in reason)
        case_type = CaseType.warn
        case = await Case.create_record(guild.id, moderator.id, moderator.name, moderator.avatar.url, target.id, target.name, target.avatar.url, case_type, reason)
        await context.send(embed=case.embed)



async def setup(bot:Bot):
    await bot.add_cog(Moderation())