import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template


class PublisherBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            print(f"Publisher  {msg}")

        await asyncio.sleep(delay=1)


class PublisherAgent(Agent):

    async def setup(self):
        temp = Template()
        temp.set_metadata("stream", "publish_stream")

        ba = PublisherBehaviour()
        self.add_behaviour(ba)
