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

            print(fx_tick)

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
