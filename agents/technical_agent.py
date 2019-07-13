import asyncio
import sys
import traceback
from queue import Queue

import rx
from rx import operators as ops
from rx.subject import Subject
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from app import fx_db
from communicate.message import get_template, AgentType
from data.data_models import TickWindow


def create_window(tick_list):
    return TickWindow.from_tick_list(tick_list)


class FxTechnicalBehaviour(CyclicBehaviour):
    window_que = Queue(maxsize=10)

    tick_subscriber = rx.subject.Subject()

    def __init__(self):
        super().__init__()
        try:

            self.tick_subscriber.pipe(
                ops.map(lambda fx_id: fx_db.get_fx_tick(fx_id)),
                ops.buffer_with_time(60),
                ops.map(create_window),
                ops.filter(lambda w: w is not None)
            ).subscribe(
                on_next=lambda op: print(op),
                on_error=lambda e: print(e),
                on_completed=lambda: print("on_completed")
            )

        except Exception:
            print(traceback.format_exc())
            # or
            print(sys.exc_info()[0])

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            # print(msg)

            tick_id = msg.get_metadata("fx_tick_id")

            self.tick_subscriber.on_next(tick_id)

            # print(fx_tick)

        await asyncio.sleep(delay=1)


class TechnicalAnalysingAgent(Agent):

    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        print("TA Agent Start")

    async def setup(self):
        template = get_template(AgentType.TECHNICAL)
        b = FxTechnicalBehaviour()
        self.add_behaviour(b, template=template)
        print("TA Agent setup done...")
