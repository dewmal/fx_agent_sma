import time

from agents.coordinator_agent import CoordinatorAgent
from agents.fundamental_agent import FundamentalAnalysingAgent
from agents.technical_agent import TechnicalAnalysingAgent
from agents.trading_stream_agent import TradingStreamAgent
from settings import *

print(users['coordinator']['username'])

if __name__ == "__main__":

    fa_co_agent = CoordinatorAgent(get_xmpp_username(users['coordinator']['username']),
                                   users['coordinator']['password'])
    fa_co_agent.start()
    fa_co_agent.web.start(hostname="127.0.0.1", port=users['coordinator']['port'])

    fa_ta_agent = TechnicalAnalysingAgent(get_xmpp_username(users['technical']['username']),
                                          users['technical']['password'])
    fa_ta_agent.start()
    fa_ta_agent.web.start(hostname="127.0.0.1", port=users['technical']['port'])

    fa_agent = FundamentalAnalysingAgent(get_xmpp_username(users['fundamental']['username']),
                                         users['fundamental']['password'], news_read_frequency=60 * 60 * 2)
    fa_agent.start()
    fa_agent.web.start(hostname="127.0.0.1", port=users['fundamental']['port'])

    fa_trading_stream_agent = TradingStreamAgent(get_xmpp_username(users['stream_agent']['username']),
                                                 users['stream_agent']['password'], stock_indexes=stock_indexes)

    fa_trading_stream_agent.start()
    fa_trading_stream_agent.web.start(hostname="127.0.0.1", port=users['stream_agent']['port'])

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    fa_agent.stop()
