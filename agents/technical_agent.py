from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class FxStreamReadingBehaviour(CyclicBehaviour):

    async def run(self):
        pass


class TechnicalAnalysingAgent(Agent):

    async def setup(self):
        b = FxStreamReadingBehaviour()
        self.add_behaviour(b)
