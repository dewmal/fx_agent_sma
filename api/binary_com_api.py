import asyncio
import datetime
import json
import sys
import traceback

import settings
from data.data_models import TickStream


async def process_message(message, _callback_fn):
    fact = json.loads(message)
    # print(message)
    message_type = fact['msg_type']

    if 'error' in fact and fact['error']['code'] == 'AuthorizationRequired':
        # self.login(ws)
        pass

    try:
        # print(fact)
        if message_type == 'tick':
            _id = fact['tick']['id']
            date = int(fact['tick']['epoch'])
            ask = float(fact['tick']['ask'])
            bid = float(fact['tick']['bid'])
            quote = float(fact['tick']['quote'])
            symbol = str(fact['tick']['symbol'])

            for stock_index in settings.stock_indexes:
                if stock_index['api_name'] == symbol:
                    tick = TickStream(tickId=_id, symbol=stock_index['symbol'], ask=ask, bid=bid, quote=quote,
                                      epoch=date)
                    await _callback_fn(tick)
                    break

        elif message_type == 'history':

            symbol = fact["echo_req"]["ticks_history"]

            for stock_index in settings.stock_indexes:
                if stock_index['api_name'] == symbol:
                    symbol = stock_index['symbol']
                    break

            prices = fact["history"]["prices"]
            times = fact["history"]["times"]

            for idx, time in enumerate(times):
                price = prices[idx]
                # print(time)
                # print(datetime.datetime.fromtimestamp(time))

                tick = TickStream(tickId=time, symbol=symbol, ask=price, bid=price, quote=price,
                                  epoch=time)
                await _callback_fn(tick)

                await asyncio.sleep(delay=settings.sleep_delay)


    except Exception as e:
        ex, val, tb = sys.exc_info()
        traceback.print_exception(ex, val, tb)
