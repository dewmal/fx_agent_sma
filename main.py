import time

from agents.coordinator_agent import CoordinatorAgent
from agents.decision_agent import DecisionAgent
from agents.fundamental_agent import FundamentalAnalysingAgent
from agents.technical_agent import TechnicalAnalysingAgent
from agents.trading_stream_agent import TradingStreamAgent
from settings import *

if __name__ == "__main__":

    agents = []

    fa_di_agent = DecisionAgent(get_xmpp_username(
        users['decision']['username']),
        users['decision']['password'])
    agents.append([fa_di_agent, users['decision']['port']])

    fa_co_agent = CoordinatorAgent(get_xmpp_username(
        users['coordinator']['username']),
        users['coordinator']['password'])
    agents.append([fa_co_agent, users['coordinator']['port']])

    fa_ta_agent = TechnicalAnalysingAgent(get_xmpp_username(
        users['technical']['username']),
        users['technical']['password'])
    agents.append([fa_ta_agent, users['technical']['port']])

    fa_agent = FundamentalAnalysingAgent(get_xmpp_username(
        users['fundamental']['username']),
        users['fundamental']['password'],
        news_read_frequency=60 * 60 * 2)
    agents.append([fa_agent, users['fundamental']['port']])

    fa_trading_stream_agent = TradingStreamAgent(get_xmpp_username(
        users['stream_agent']['username']),
        users['stream_agent']['password'],
        stock_indexes=stock_indexes)

    agents.append([fa_trading_stream_agent, users['stream_agent']['port']])

    for agent, port in agents:
        agent.start()
        agent.web.start(hostname="127.0.0.1", port=port)

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    fa_agent.stop()
