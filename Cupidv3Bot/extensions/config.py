from discord import TextChannel
from discord.ext.commands import Bot, Cog, Context, command, Group

from CupidV3Database.guildconfiguration import GuildConfig

configure = Group(name="config")

class GuildConfig(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @configure.command(name="channels", description="Configurations for the guild")
    async def channels(self, ctx: Context, channel: TextChannel, setting: str):
        guild_config = GuildConfig({"guild_id": ctx.guild.id})
        if setting == "level_up":
            subscribed_events = guild_config.subscribed_events.level_up

            subscribed_events.append({"channel_id": channel.id})

            await guild_config.update(
                data={
                    "$set": {
                        "subscribed_events": {
                            "level_up": subscribed_events
                        }
                    }
                }
            )
        elif setting == "case_logging":
            subscribed_events = guild_config.subscribed_events.cases

            subscribed_events.append({"channel_id": channel.id})
            await GuildConfig.update(
                data={
                    "$set": {
                        "subscribed_events": {
                            "cases_": subscribed_events
                        }
                    }
                }
            )
        else:
            return await ctx.reply(
                f"There is no such thing as {setting}"
            )
        await ctx.reply(f"Successfully set `{setting}` to `{channel.mention}`")

def setup(bot: Bot):
    bot.add_cog(GuildConfig(bot))