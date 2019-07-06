import asyncio
from queue import Queue

import numpy as np
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from app import fx_db
from settings import get_xmpp_username, users
from ta_lib.ta_rules import ta_rule_ge_value


class FxTechnicalBehaviour(CyclicBehaviour):
    window_que = Queue(maxsize=10)

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            # print(msg)
            tick_id = msg.get_metadata("fx_tick_id")
            # print(tick_id)
            fx_tick = await fx_db.get_fx_tick(tick_id)

            self.window_que.put(fx_tick)
            # print("put done")

            if self.window_que.qsize() == 5:
                sma_value = np.random.uniform(0, 1)  # sma([x.ask for x in list(self.window_que.queue)], 5)
                ema_value = np.random.uniform(0, 1)  # ema([x.ask for x in list(self.window_que.queue)], 5)
                wma_value = np.random.uniform(0, 1)  # wma([x.ask for x in list(self.window_que.queue)], 5)
                rsi_value = np.random.uniform(0, 1)  # rsi([x.ask for x in list(self.window_que.queue)], 5)

                ta_value = ta_rule_ge_value(sma_value, ema_value, wma_value, rsi_value)

                # direction = ta_rule_ge_direction([x.ask for x in list(self.window_que.queue)])

                msg = Message(to=get_xmpp_username(username=users['decision']['username']))
                msg.set_metadata("stream", "ta_result")
                msg.set_metadata("symbol", fx_tick.pair)
                msg.set_metadata("signal", "BUY")

                msg.set_metadata("ta_value", f"{ta_value}")

                await self.send(msg)

                self.window_que.get()

        await asyncio.sleep(delay=1)


class TechnicalAnalysingAgent(Agent):

    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        print("TA Agent Start")

    async def setup(self):
        temp = Template()
        temp.set_metadata("stream", "technical_tick")
        b = FxTechnicalBehaviour()
        self.add_behaviour(b, template=temp)
