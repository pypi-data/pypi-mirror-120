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
"""
non-subscription event sent immediately after connecting,
contains server information
"""

from pincer.commands import ChatCommandHandler
from pincer.core.dispatch import GatewayDispatch
from pincer.objects import User
from pincer.utils import Coro


async def on_ready_middleware(self, payload: GatewayDispatch):
    """
    Middleware for ``on_ready`` event.

    :param self:
        The current client.

    :param payload:
        The data received from the ready event.
    """
    self.bot = User.from_dict(payload.data.get("user"))
    await ChatCommandHandler(self).initialize()
    return "on_ready",


def export() -> Coro:
    return on_ready_middleware
