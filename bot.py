# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.core import ActivityHandler, TurnContext,RecognizerResult,MessageFactory
from botbuilder.schema import ChannelAccount
from botbuilder.ai.luis import LuisApplication,LuisPredictionOptions,LuisRecognizer


class LuisBot(ActivityHandler):
    def __init__(self):
        luis_app = LuisApplication("52a3853b-ca6f-48a9-b5b2-ca5a31db3710","1a5e19cdf4444808989503e0ee2dd5a0","https://westus.api.cognitive.microsoft.com/")
        luis_option = LuisPredictionOptions(include_all_intents=True,include_instance_data=True)
        self.LuisReg = LuisRecognizer(luis_app,luis_option,True)

    async def on_message_activity(self, turn_context: TurnContext):
        luis_result = await self.LuisReg.recognize(turn_context)
        intent = LuisRecognizer.top_intent(luis_result)
        if (intent == 'quem'):
            await turn_context.send_activity("Olá eu sou seu assistente virtual, estou na versão beta")
        if (intent == 'ligarLuz'):
            await turn_context.send_activity("Ok estou ligando a luz")
        if (intent == 'desligarLuz'):
            await turn_context.send_activity("Ok estou apagando a luz")
        if (intent == 'temperaturaStatus'):
            await turn_context.send_activity("A temperatura é de:")
        if (intent == 'umidadeStatus'):
            await turn_context.send_activity("A umidade é de:")
        if (intent == 'aumentarTemperatura'):
            await turn_context.send_activity("Estou aumentando a temperatura")
        if (intent == 'baixarTemperatura'):
            await turn_context.send_activity("Estou abaixando a temperatura")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Olá seja bem vindo!")
