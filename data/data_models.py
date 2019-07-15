from datetime import datetime


class TickStream:
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
    open = 0
    high = 0
    low = 0
    close = 0
    epoch = 0
    symbol: str

    def __init__(self, open, high, low, close, epoch, symbol, tick_list=[]) -> None:
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.epoch = epoch
        self.symbol = symbol
        self.tick_list = tick_list

    @staticmethod
    def from_tick_list(tick_list: [TickStream]):
        if len(tick_list) > 0:
            open_tick = tick_list[0]
            high_tick = max(tick_list, key=lambda tick: tick.value)
            low_tick = min(tick_list, key=lambda tick: tick.value)
            close_tick = tick_list[-1]
            return TickWindow(open_tick.value, high_tick.value, low_tick.value, close_tick.value, open_tick.epoch,
                              open_tick.symbol,
                              tick_list)
        else:
            return None

    def __str__(self) -> str:
        return f"{self.symbol} OLHC - {self.open},{self.high},{self.low},{self.close},{self.epoch}"


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
