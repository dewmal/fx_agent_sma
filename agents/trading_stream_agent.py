import asyncio
import json

import websockets
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

from api.binary_com_api import process_message


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
                    print(fx_tick)

                # print(message)
                await process_message(message, _callback_fn=tick_value)

    async def run(self):
        asyncio.get_event_loop().run_until_complete(self.fx_hello())


class TradingStreamAgent(Agent):
    async def setup(self):
        print("start trading stream agent")
        b = TradingStreamReceivingAgent(pair_name="R_100")
        self.add_behaviour(b)

        b = TradingStreamReceivingAgent(pair_name="R_50")
        self.add_behaviour(b)
