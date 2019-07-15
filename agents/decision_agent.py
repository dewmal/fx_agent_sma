import asyncio

from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template

from settings import sleep_delay


class HighAlertNewsRecBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            print("Do not attend for any transaction")

        await asyncio.sleep(delay=sleep_delay)


class DecisionAgentBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=1)
        if msg:
            ta_value = float(msg.get_metadata("ta"))
            ta_symbol = msg.get_metadata("symbol")
            ta_signal = msg.get_metadata("signal")

            if ta_value > 0.9:
                print(f"You can  {ta_signal} {ta_symbol} and you can profit more than {90.0}%")
            elif ta_value > 0.6:
                print(f"You can  {ta_signal} {ta_symbol} and you can profit more than {60.0}%")
            elif ta_value > 0.4:
                print(f"You can  {ta_signal} {ta_symbol} and you can profit more than {50.0}%")
            else:
                print("Do nothing...")

        await asyncio.sleep(delay=sleep_delay)


class DecisionAgent(Agent):

    def setup(self):
        tmp = Template()
        tmp.set_metadata("stream", "ta_result")
        ba = DecisionAgentBehaviour()
        self.add_behaviour(ba, template=tmp)

        tmp = Template()
        tmp.set_metadata("stream", "high_alert_result")
        ba = HighAlertNewsRecBehaviour()
        self.add_behaviour(ba, template=tmp)
