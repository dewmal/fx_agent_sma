import datetime

from utils import round_time


class TickStream:
    __type__ = "tick_stream"
    symbol: str
    ask: float
    bid: float
    quote: float
    epoch: int
    value: float

    def __init__(self, tickId, symbol, ask, bid, quote, epoch, version="1.0") -> None:
        super().__init__()
        self.tickId = tickId
        self.bid = bid
        self.ask = ask
        self.symbol = symbol
        self.quote = quote
        self.epoch = epoch
        self.version = version
        self.value = (self.ask + self.bid) / 2

    def as_dict(self):
        return {
            "tickId": self.tickId,
            "symbol": self.symbol,
            "ask": self.ask,
            "bid": self.bid,
            "quote": self.quote,
            "epoch": self.epoch,
        }

    @classmethod
    def from_dict(cls, tick_data):
        # print(tick_data['pair'])
        return TickStream(
            tick_data['tickId'],
            tick_data['symbol'],
            tick_data['ask'],
            tick_data['bid'],
            tick_data['quote'],
            tick_data['epoch']
        )

    def __str__(self) -> str:
        return f"{self.as_dict()}"


class TickWindow:
    __type__ = "window_stream"
    open = 0
    high = 0
    low = 0
    close = 0
    epoch = 0
    symbol: str
    last_epoch_time = 0

    def __init__(self, open, high, low, close, epoch, symbol, last_epoch_time=0, tick_list=[], id=None) -> None:
        self.id = id
        self.last_epoch_time = last_epoch_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.epoch = epoch
        self.symbol = symbol
        self.tick_list = tick_list

    def as_dict(self):
        return {
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "epoch": self.epoch,
            "symbol": self.symbol,
            "last_epoch_time": self.last_epoch_time,
        }

    @classmethod
    def from_dict(cls, _data):
        return TickWindow(
            _data['open'],
            _data['high'],
            _data['low'],
            _data['close'],
            _data['epoch'],
            _data['symbol'],
            _data['last_epoch_time'],
            [],
            _data['_id'],
        )

    @staticmethod
    def from_tick_list(tick_list: [TickStream]):
        if len(tick_list) > 0:
            open_tick = tick_list[0]
            high_tick = max(tick_list, key=lambda tick: tick.value)
            low_tick = min(tick_list, key=lambda tick: tick.value)
            close_tick = tick_list[-1]

            return TickWindow(open_tick.value, high_tick.value, low_tick.value, close_tick.value,
                              round_time(datetime.datetime.fromtimestamp(open_tick.epoch)).timestamp(),
                              open_tick.symbol,
                              tick_list)
        else:
            return None

    def __str__(self) -> str:
        return f"{self.symbol} OLHC - {self.open},{self.high},{self.low},{self.close},{self.epoch},{self.last_epoch_time},{self.id}"


class TIData:

    def __init__(self, name, time_interval, epoch, data, symbol) -> None:
        super().__init__()
        self.time_interval = time_interval
        self.symbol = symbol
        self.data = data
        self.epoch = epoch
        self.name = name

    def __str__(self):
        return f"{self.name}-{self.time_interval},{self.data},{self.epoch},{self.symbol}"
