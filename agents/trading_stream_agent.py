import asyncio
import json

import websockets
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

import settings
from api.binary_com_api import process_message
from app import fx_db
from communicate.message import MessageBuilder, AgentType


class TradingStreamReceivingAgent(OneShotBehaviour):

    async def notify_coordinator(self, fx_tick_id):
        msg = MessageBuilder(sender_agent=AgentType.STREAM_AGENT,
                             to_agent=AgentType.COORDINATOR) \
            .meta_data("fx_tick_id", f"{fx_tick_id}") \
            .body("FX_TICK") \
            .message
        await  self.send(msg)

    def __init__(self, pair_name):
        super().__init__()
        self.pair_name = pair_name

    async def fx_tick_reader(self):
        async with websockets.connect(
                f'{settings.binary_api_end_point}') as websocket:
            json_data = json.dumps({'ticks': f'{self.pair_name}'})
            await websocket.send(json_data)

            tick_stream = self
            async for message in websocket:
                async def tick_value(fx_tick):
                    res_id = await fx_db.insert_fx_tick(fx_tick)
                    await tick_stream.notify_coordinator(res_id)

                await process_message(message, _callback_fn=tick_value)

    async def run(self):
        asyncio.get_event_loop().run_until_complete(self.fx_tick_reader())


class TradingStreamAgent(Agent):

    def __init__(self, jid, password, verify_security=False, stock_indexes=[]):
        super().__init__(jid, password, verify_security)
        self.stock_indexes = stock_indexes

    async def setup(self):
        print("start trading stream agent")

        for index_val in self.stock_indexes:
            print(index_val)
            b = TradingStreamReceivingAgent(pair_name=f"{index_val['api_name']}")
            self.add_behaviour(b)
