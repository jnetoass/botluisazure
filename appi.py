# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime
from botbuilder.core.bot import Bot

app = Flask(__name__)
from flask import Flask,request,Response
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
    ConversationState,
    MemoryStorage
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes
import asyncio

from bot import LuisBot
from config import DefaultConfig

loop = asyncio.get_event_loop()




# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.

botsettings = BotFrameworkAdapterSettings("a896b57b-d97c-414f-8b1d-0dd0780e3492","9yRpUW=vZ$RU(Si1fmJho_>=pE>")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
# Create the Bot
BOT = LuisBot()
@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await Bot.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)


if __name__ == "__main__":
    app.run(host="localhost", port=3978) #localhost -> 0.0.0.0
