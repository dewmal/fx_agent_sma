import asyncio

import rx
from rx import operators as ops, Observable
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from app import fx_db
from communicate.message import get_template, AgentType
from data.data_models import TIData, TickStream, TickWindow
from settings import sleep_delay
from ta_lib.ta_analyser import TAnalyser
from ta_lib.ta_analyser_window import TAnalyserWidow


class FxTechnicalWindowReadBehaviour(CyclicBehaviour):

    def __init__(self, stock_indexes):
        super().__init__()
        self.stock_indexes = stock_indexes

        for stock_index in stock_indexes:
            tick_analyser = TAnalyserWidow(20, stock_index['symbol'])
            tick_analyser.ta_result.subscribe_(self.read_analysing_report)
            self.analysers.append(tick_analyser)
            print(tick_analyser)

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            # print("Window Tick  Stream")
            db_id = msg.get_metadata("db_id")
            window = await fx_db.get_fx_window(db_id)
            # print(window)
            rx.from_iterable(self.analysers).pipe(ops.filter(lambda a: a.symbol == window.symbol)).subscribe_(
                lambda tick_analyser: tick_analyser.on_next(window))

    analysers = []

    def read_analysing_report(self, report: TIData):
        print("--window--")
        print(report.name, report.symbol, report.epoch)
        print(report.data)
        print("--window--")


class FxTechnicalTickReadBehaviour(CyclicBehaviour):
    analysers = []

    def read_analysing_report(self, report: TIData):
        print("----")
        print(report.name, report.symbol, report.epoch)
        print("----")

    def __init__(self, stock_indexes):
        super().__init__()
        for stock_index in stock_indexes:
            tick_analyser = TAnalyser(60, stock_index['symbol'])
            tick_analyser.ta_result.subscribe_(self.read_analysing_report)
            self.analysers.append(tick_analyser)
            print(tick_analyser)

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            # print(msg)
            tick_id = msg.get_metadata("fx_tick_id")
            tick = await fx_db.get_fx_tick(tick_id)
            # print(tick.symbol)
            # rx.from_iterable(self.analysers).subscribe_(print)
            rx.from_iterable(self.analysers).pipe(ops.filter(lambda a: a.symbol == tick.symbol)).subscribe_(
                lambda tick_analyser: tick_analyser.on_next(tick))
            # print(fx_tick)

        await asyncio.sleep(delay=sleep_delay)


class TechnicalAnalysingAgent(Agent):

    def __init__(self, jid, password, verify_security=False, stock_indexes=None):
        super().__init__(jid, password, verify_security)
        self.stock_indexes = stock_indexes
        print("TA Agent Start")

    async def setup(self):
        # template = get_template(AgentType.TECHNICAL)
        # template.set_metadata("db_type", f"{TickStream.__type__}")
        # b = FxTechnicalTickReadBehaviour(self.stock_indexes)
        # self.add_behaviour(b, template=template)

        template = get_template(AgentType.TECHNICAL)
        template.set_metadata("db_type", f"{TickWindow.__type__}")
        b = FxTechnicalWindowReadBehaviour(self.stock_indexes)
        self.add_behaviour(b, template=template)

        print("TA Agent setup done...")
