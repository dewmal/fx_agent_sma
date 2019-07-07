class TickStream:
    symbol: str
    ask: float
    bid: float
    quote: float
    epoch: int

    def __init__(self, tickId, symbol, ask, bid, quote, epoch, version="1.0") -> None:
        super().__init__()
        self.tickId = tickId
        self.bid = bid
        self.ask = ask
        self.symbol = symbol
        self.quote = quote
        self.epoch = epoch
        self.version = version

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
