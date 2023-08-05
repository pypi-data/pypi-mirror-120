from __future__ import annotations

import asyncio
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Union,
    Optional,
    List,
    Dict,
    Any
)

import discord

from .Base import DatabaseChecker
from .Punishments import Punisher

if TYPE_CHECKING:
    from .Punishments import Punishment
    from discord.ext import commands


__all__ = ("UnbanFailure", "BanManager")


class UnbanFailure(Exception):
    """Raises an exception when the user tries to unban a discord.User without passing the guild."""


class BanManager(DatabaseChecker, Punisher):
    """
    A BanManager that manages guild bans.
    """

    __slots__ = ("bot",)

    def __init__(self, bot: commands.Bot):
        super().__init__([{'guild': "snowflake", 'member': "snowflake", 'reason': "string", 'timestamp': "snowflake"}],
                         ['bans'])
        self.bot = bot

        self.add_event(self.on_database_connect)

    async def on_database_connect(self):
        self.bot.loop.create_task(self.__check_bans())

    async def get_banned_members(self) -> List[Dict[str, Any]]:
        """
        |coro|

        This function returns all the members that are supposed to be unbanned but are banned.

        :return: The list of unbanned members.
        :rtype: List[Dict[str, Any]]
        """

        return [x for x in await self.database.select(self.tables['bans'], [], fetchall=True)
                if x["timestamp"] <= datetime.utcnow().timestamp()]

    async def __check_bans(self) -> None:
        """
        |coro|

        A loop that ensures that members are unbanned when they need to.

        :return: None
        :rtype: None
        """

        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            for banned_member in await self.get_banned_members():
                guild = self.bot.get_guild(banned_member['guild'])

                if guild is None:
                    continue

                user = await self.bot.fetch_user(banned_member['member'])

                if await self.unban(user, guild):
                    await self.call_event("on_unban", user, banned_member['reason'])

            await asyncio.sleep(300)

    async def punish(self, ctx: commands.Context, member: discord.Member, punishment: Punishment) -> None:
        try:
            self.bot.loop.create_task(
                self.ban(member, punishment.punishment_reason, punishment.punishment_time.total_seconds())
            )
        except discord.errors.Forbidden as e:
            raise e
        else:
            await self.call_event("on_punishment", ctx, member, punishment)

    @staticmethod
    async def get_ban(member: Union[discord.Member, discord.User], guild: discord.Guild) -> Optional[discord.User]:
        """
        |coro|

        This function returns the user object of the member if he is banned from the guild.

        :param member: The banned member.
        :type member: discord.Member
        :param guild: The guild.
        :type guild: discord.Guild
        :return: The user object if found.
        :rtype: Optional[discord.User]
        """

        banned = await guild.bans()
        for x in banned:
            if x.user.id == member.id:
                return x.user

    async def unban(self, member: Union[discord.Member, discord.User], guild: discord.Guild = None) -> bool:
        self._check_database()

        if isinstance(member, discord.User) and not guild:
            raise UnbanFailure("Cannot unban a discord.User without a guild.")

        guild = guild if guild is not None else member.guild
        await self.database.delete(self.tables['bans'], {'guild': guild.id, 'member': member.id})

        if user := await self.get_ban(member, guild):
            await guild.unban(user)
            return True

    async def ban(self,
                  member: discord.Member,
                  reason: str = "No reason provided.",
                  time_of_ban: Union[int, float] = 0) -> None:
        """
        |coro|

        Bans the member from the guild.

        :param member: The member to ban.
        :type member: discord.Member
        :param reason: The reason of the ban.
        :type reason: str
        :param time_of_ban: The time of ban.
        :type time_of_ban: Union[int, float]
        :return: None
        :rtype: None
        """

        self._check_database()

        await member.ban(reason=reason)

        if time_of_ban <= 0:
            return

        await self.database.insert(self.tables['bans'], {'guild': member.guild.id,
                                                         'member': member.id,
                                                         'reason': reason,
                                                         'timestamp': datetime.utcnow().timestamp() + time_of_ban})

        await asyncio.sleep(time_of_ban)

        if await self.unban(member):
            await self.call_event("on_unban", member, reason)
