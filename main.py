import time
from agents.fundamental_agent import FundamentalAnalysingAgent
from settings import *

print(users['coordinator']['username'])

if __name__ == "__main__":
    fa_agent = FundamentalAnalysingAgent("admin@127.0.0.1", "dewmal", news_read_frequency=5)
    fa_agent.start()
    fa_agent.web.start(hostname="127.0.0.1", port="10000")

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    fa_agent.stop()
