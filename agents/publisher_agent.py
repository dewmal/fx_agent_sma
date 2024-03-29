import asyncio

import websockets
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.template import Template

from settings import sleep_delay


class PublisherBehaviour(OneShotBehaviour):

    async def server(self, websocket, path):
        while True:
            msg = await self.receive(timeout=1)
            if msg:
                data_key = msg.get_metadata("data_key")
                print(data_key, path, data_key == path)
                if f"/{data_key}" == path:
                    data_value = msg.get_metadata("data_value")
                    await websocket.send(data_value)
            await asyncio.sleep(delay=sleep_delay)

    def __init__(self):
        super().__init__()

    async def run(self):
        start_server = websockets.serve(self.server, '127.0.0.1', 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


class PublisherAgent(Agent):

    async def setup(self):
        temp = Template()
        temp.set_metadata("stream", "publish_stream")

        ba = PublisherBehaviour()
        self.add_behaviour(ba)
