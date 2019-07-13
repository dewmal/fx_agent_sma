import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from communicate.message import MessageBuilder, AgentType, get_template
from settings import get_xmpp_username, users
import communicate.message as me


class CoordinatorTickStreamReadingBehavior(CyclicBehaviour):

    async def notify_pulathisi(self, tick_id):
        msg = Message(to=get_xmpp_username(users['oracle']['username']))
        msg.set_metadata("fx_tick_id", tick_id)
        await self.send(msg)

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            MessageBuilder(AgentType.TECHNICAL)
            ta_msg = Message(to=get_xmpp_username(users['technical']['username']))
            ta_msg.set_metadata("fx_tick_id", msg.get_metadata("fx_tick_id"))
            ta_msg.set_metadata("stream", me.AgentType.COORDINATOR.value)
            await self.send(ta_msg)

            await self.notify_pulathisi(msg.get_metadata("fx_tick_id"))

        await asyncio.sleep(delay=1)


class CoordinatorAgent(Agent):

    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        print(f"{jid}")

    async def setup(self):
        print("Coordinator Agent Created...")
        template = get_template(AgentType.COORDINATOR)

        b = CoordinatorTickStreamReadingBehavior()
        self.add_behaviour(b, template=template)
