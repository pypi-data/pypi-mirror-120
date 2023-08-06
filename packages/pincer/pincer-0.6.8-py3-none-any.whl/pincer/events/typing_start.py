# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2021 Pincer
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from dataclasses import dataclass

from ..objects.guild_member import GuildMember
from ..utils.api_object import APIObject
from ..utils.types import APINullable, MISSING
from ..utils.snowflake import Snowflake


@dataclass
class TypingStartEvent(APIObject):
    """
    Sent when a user starts typing in a channel.

    :param channel_id:
        id of the channel

    :param guild_id:
        id of the guild

    :param user_id:
        id of the user

    :param timestamp:
        unix time (in seconds) of when the user started typing

    :param member:
        the member who started typing if this happened in a guild
    """
    channel_id: Snowflake
    user_id: Snowflake
    timestamp: int

    guild_id: APINullable[Snowflake] = MISSING
    member: APINullable[GuildMember] = MISSING
