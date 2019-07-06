import asyncio
import json

import websockets
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

from api.binary_com_api import process_message
from app import fx_db
from settings import get_xmpp_username, users


class TradingStreamReceivingAgent(OneShotBehaviour):

    async def notify_publisher(self, fx_tick_id):
        to_sender = get_xmpp_username(users['publisher']['username'])  # Instantiate the message
        msg = Message(to=to_sender)  # Instantiate the message
        msg.set_metadata("stream", "publish_stream")  # Instantiate the message
        msg.set_metadata("fx_tick_id", f"{fx_tick_id}")  # Instantiate the message
        msg.body = "Tick Data"  # Set the message content

        await  self.send(msg)

    async def notify_coordinator(self, fx_tick_id):
        to_sender = get_xmpp_username(users['coordinator']['username'])  # Instantiate the message
        msg = Message(to=to_sender)  # Instantiate the message
        msg.set_metadata("stream", "fx_tick")  # Instantiate the message
        msg.set_metadata("fx_tick_id", f"{fx_tick_id}")  # Instantiate the message
        msg.body = "Tick Data"  # Set the message content

        await  self.send(msg)

    def __init__(self, pair_name):
        super().__init__()
        self.pair_name = pair_name

    async def fx_hello(self):
        async with websockets.connect(
                'wss://ws.binaryws.com/websockets/v3?app_id=1089') as websocket:
            json_data = json.dumps({'ticks': f'{self.pair_name}'})
            print(f"sending stream {json_data}")
            await websocket.send(json_data)
            print(f"> {json_data}")

            tick_stream = self
            async for message in websocket:
                async def tick_value(fx_tick):
                    res_id = await fx_db.insert_fx_tick(fx_tick)
                    await tick_stream.notify_coordinator(res_id)
                    await tick_stream.notify_publisher(res_id)

                await process_message(message, _callback_fn=tick_value)

    async def run(self):
        asyncio.get_event_loop().run_until_complete(self.fx_hello())


class TradingStreamAgent(Agent):

    def __init__(self, jid, password, verify_security=False, stock_indexes=[]):
        super().__init__(jid, password, verify_security)
        self.stock_indexes = stock_indexes

    async def setup(self):
        print("start trading stream agent")

        for index_val in self.stock_indexes:
            print(index_val)
            b = TradingStreamReceivingAgent(pair_name=f"{index_val}")
            self.add_behaviour(b)
