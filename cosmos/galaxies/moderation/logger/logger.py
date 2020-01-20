import discord
import typing

from .events import LoggerEvents
from discord.ext import commands


class NameConvertor(commands.Converter):

    async def convert(self, ctx, argument):
        if not argument.lower().startswith("on"):
            raise commands.BadArgument("Logger name doesn't starts with 'on'.")
        if " " in argument:
            return argument.lower().replace(" ", "_")
        return argument


class Logger(LoggerEvents):
    """Logger plugin provides option to log various discord and moderation events in desired channel.

    Available Logger Events:
        - on_message_delete -- Logs content and other attributes of message which was just deleted.
        - on_bulk_message_delete -- Logs channel from which messages was deleted in bulk.
        - on_message_edit -- Logs old and new content along wth other attributes of message which was just edited.
        - on_guild_channel_pins_update -- Logs several attributes when a message is pinned in channel.
        - on_member_join -- Logs useful attributes of member who just joined the server.
        - on_member_remove -- Logs attributes of member who just left the server.
        - on_moderation -- Logs several attributes of member, type of moderation, moderator and reason if it was
        provided when moderator or auto-moderator performs any moderation action on this member.

    """

    @staticmethod
    async def __logger_entry_parser(_, entry, __):
        return entry.replace("_", " ").title()

    @LoggerEvents.group(name="logger", aliases=["log", "logging", "loggers"], invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def logger(self, ctx):
        """Displays list of loggers enabled in different channels."""
        guild_profile = await ctx.fetch_guild_profile()
        if not guild_profile.loggers:
            return await ctx.send_line(f"❌    {ctx.guild.name} doesn't has any loggers enabled.")
        embed = ctx.embeds.one_line.primary(f"{ctx.guild.name} Loggers", ctx.guild.icon_url)
        for logger in guild_profile.loggers:
            embed.add_field(name=logger.name, value=logger.channel.mention)
        await ctx.send(embed=embed)

    async def __get_logger_name_from_menu(self, ctx, loggers):
        menu = ctx.get_menu(loggers, entry_parser=self.__logger_entry_parser)
        response = await menu.wait_for_response()
        return response.entry

    @logger.command(name="enable", aliases=["create"])
    async def enable_logger(self, ctx, channel: typing.Optional[discord.TextChannel], *, name: NameConvertor = None):
        """Enables logger in specified channel. Logger name should always start with `on_`."""
        channel = channel or ctx.channel
        guild_profile = await ctx.fetch_guild_profile()
        loggers = [name for name in self.loggers if not guild_profile.get_logger(name)]
        name = name or await self.__get_logger_name_from_menu(ctx, loggers)
        if name not in self.loggers:
            return await ctx.send_line(f"❌    Sorry but logging for event '{name}' isn't supported yet.")
        logger = guild_profile.get_logger(name)
        if logger:
            return await ctx.send_line(f"❌    Logs for event '{logger.name}' is already enabled in #{logger.channel}")

        await guild_profile.enable_logger(name, channel)
        await ctx.send_line(f"✅    Logs for event '{name}' has been enabled in #{channel.name} channel.")

    @logger.command(name="disable", aliases=["remove"])
    async def disable_logger(self, ctx, *, name: NameConvertor = None):
        """Disables specified logger. Logger name should always start with `on_`."""
        guild_profile = await ctx.fetch_guild_profile()
        loggers = [logger.name for logger in guild_profile.loggers]
        name = name or await self.__get_logger_name_from_menu(ctx, loggers)
        if name not in self.loggers:
            return await ctx.send_line(f"❌    Sorry but logging for event '{name}' isn't supported yet.")
        logger = guild_profile.get_logger(name)
        if not logger:
            return await ctx.send_line(f"❌    Logs for event '{name}' isn't' enabled yet.")

        await guild_profile.remove_logger(name)
        await ctx.send_line(f"✅    Logs for event '{name}' has been removed.")
