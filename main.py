import time
from agents.fundamental_agent import FundamentalAnalysingAgent
from agents.trading_stream_agent import TradingStreamAgent
from settings import *

print(users['coordinator']['username'])

if __name__ == "__main__":
    fa_agent = FundamentalAnalysingAgent(get_xmpp_username(users['fundamental']['username']),
                                         users['fundamental']['password'], news_read_frequency=5)
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
