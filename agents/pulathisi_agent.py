import json

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from app import fx_db
from settings import get_xmpp_username, users


class PredictionPresentBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            tick_id = msg.get_metadata("fx_tick_id")
            tick = await fx_db.get_fx_tick(tick_id)

            tick.epoch += 60
            tick.quote = tick.quote % 105 / 100

            msg = Message(to=get_xmpp_username(users['publisher']['username']))
            msg.set_metadata("stream", "publish_stream")
            msg.set_metadata("data_key", "prediction")
            msg.set_metadata("data_value", json.dumps({'prediction': {"epoch": tick.epoch, "quote": tick.quote}}))
            await  self.send(msg)


class PulathisiRishi(Agent):

    async def setup(self):
        ba = PredictionPresentBehaviour()
        self.add_behaviour(ba)
