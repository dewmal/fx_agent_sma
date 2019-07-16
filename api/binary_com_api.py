import asyncio
import json
import sys
import traceback

import settings
from data.data_models import TickStream, TickWindow


def get_symbol(symbol):
    for stock_index in settings.stock_indexes:
        if stock_index['api_name'] == symbol:
            symbol = stock_index['symbol']
            return symbol


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

            prices = fact["history"]["prices"]
            times = fact["history"]["times"]

            for idx, time in enumerate(times):
                price = prices[idx]
                # print(time)
                # print(datetime.datetime.fromtimestamp(time))

                tick = TickStream(tickId=time, symbol=get_symbol(symbol), ask=price, bid=price, quote=price,
                                  epoch=time)
                await _callback_fn(tick)

                await asyncio.sleep(delay=settings.sleep_delay)

        elif message_type == 'candles':

            symbol = fact["echo_req"]["ticks_history"]

            candles = fact['candles']
            for candle in candles:
                open, close, low, high, epoch = float(candle['open']), float(candle['close']), float(
                    candle['low']), float(candle['high']), int(candle['epoch'])
                t_window = TickWindow(open=open, close=close, low=low, high=high, epoch=epoch,
                                      symbol=get_symbol(symbol))
                await _callback_fn(t_window)

                await asyncio.sleep(delay=settings.sleep_delay)

            pass
        elif message_type == 'ohlc':
            candle = fact['ohlc']
            open, close, low, high, epoch, symbol, last_epoch_time = float(candle['open']), float(
                candle['close']), float(
                candle['low']), float(candle['high']), int(candle['open_time']), candle['symbol'], int(candle['epoch'])

            t_window = TickWindow(open=open, close=close, low=low, high=high, epoch=epoch, symbol=get_symbol(symbol),
                                  last_epoch_time=last_epoch_time)
            await _callback_fn(t_window)
            await asyncio.sleep(delay=settings.sleep_delay)

            # tick = TickStream(tickId=last_epoch_time, symbol=get_symbol(symbol), ask=close, bid=close, quote=close,
            #                   epoch=last_epoch_time)
            # await _callback_fn(tick)
            # await asyncio.sleep(delay=settings.sleep_delay)


    except Exception as e:
        ex, val, tb = sys.exc_info()
        traceback.print_exception(ex, val, tb)


''' Candle OLHC Response
    {
      "echo_req": {
        "adjust_start_time": 1,
        "count": 10,
        "end": "latest",
        "granularity": 60,
        "start": 1,
        "style": "candles",
        "subscribe": 1,
        "ticks_history": "R_50"
      },
      "msg_type": "ohlc",
      "ohlc": {
        "close": "303.9150",
        "epoch": 1563262054,
        "granularity": 60,
        "high": "304.1961",
        "id": "9f1a0311-f3bb-05e0-ce78-11baf6a0aa6d",
        "low": "303.9065",
        "open": "304.1676",
        "open_time": 1563262020,
        "symbol": "R_50"
      }
'''

''' Candle History
            {
  "candles": [
    {
      "close": 304.0483,
      "epoch": 1563262020,
      "high": 304.1961,
      "low": 303.9065,
      "open": 304.1676
    },
    {
      "close": 304.2153,
      "epoch": 1563262080,
      "high": 304.2153,
      "low": 303.952,
      "open": 304.0676
    }
  ],
  "echo_req": {
    "adjust_start_time": 1,
    "count": 2,
    "end": "latest",
    "start": 1,
    "style": "candles",
    "ticks_history": "R_50"
  },
  "msg_type": "candles"
}       '''
