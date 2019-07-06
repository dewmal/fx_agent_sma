import json
import sys
import traceback

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
            # print(pair_name,date,data)
            # await context.publish(index=date, data=data)

            tick_val = TickStream(pair=symbol, ask=ask, bid=bid, quote=quote,
                                  timestamp=date)
            await _callback_fn(tick_val)

        elif message_type == 'proposal':
            # self.buy_contact(ws, fact)
            pass
        elif message_type == 'authorize':
            # self.is_logged_in = True
            # self.account_balance = float(fact['authorize']['balance'])
            pass
        elif message_type == 'buy':
            # self.account_balance = float(fact['buy']['balance_after'])
            pass
        elif message_type == 'sell':
            # self.account_balance = float(fact['sell']['balance_after'])
            pass
        else:
            # logging.info(fact)
            pass

    except Exception as e:
        ex, val, tb = sys.exc_info()
        traceback.print_exception(ex, val, tb)
