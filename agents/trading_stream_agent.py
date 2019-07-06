import asyncio
import json

import websockets
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

from api.binary_com_api import process_message
from app import fx_db


class TradingStreamReceivingAgent(OneShotBehaviour):

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

            async for message in websocket:
                async def tick_value(fx_tick):
                    res_id = await fx_db.insert_fx_tick(fx_tick)
                    print(res_id)

                # print(message)
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
