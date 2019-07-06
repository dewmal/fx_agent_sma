import datetime

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour


class ReadNewsBehaviour(PeriodicBehaviour):
    async def run(self):
        print(f"ReadNewsBehaviour  Run at {datetime.datetime.now().time()}")


class FundamentalAnalysingAgent(Agent):

    def __init__(self, jid, password, verify_security=False, news_read_frequency=60 * 60 * 60):
        super().__init__(jid, password, verify_security)
        self.news_read_frequency = news_read_frequency

    async def setup(self):
        print(f"PeriodicSenderAgent started at {datetime.datetime.now().time()}")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=5)
        b = ReadNewsBehaviour(period=self.news_read_frequency, start_at=start_at)
        self.add_behaviour(b)
