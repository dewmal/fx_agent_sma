import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from app import fx_db
from communicate.message import get_template, AgentType
from data.data_models import TIData
from settings import sleep_delay
from ta_lib.ta_analyser import TAnalyser


class FxTechnicalBehaviour(CyclicBehaviour):
    tick_analyser = TAnalyser(60)

    def read_analysing_report(self, report: TIData):
        print("----")
        print(report.epoch)
        print("----")

    def __init__(self):
        super().__init__()
        self.tick_analyser.ta_result.subscribe_(self.read_analysing_report)

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            # print(msg)
            tick_id = msg.get_metadata("fx_tick_id")
            tick = await fx_db.get_fx_tick(tick_id)
            self.tick_analyser.on_next(tick)
            # print(fx_tick)

        await asyncio.sleep(delay=sleep_delay)


class TechnicalAnalysingAgent(Agent):

    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        print("TA Agent Start")

    async def setup(self):
        template = get_template(AgentType.TECHNICAL)
        b = FxTechnicalBehaviour()
        self.add_behaviour(b, template=template)
        print("TA Agent setup done...")
