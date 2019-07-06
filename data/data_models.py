class TickStream:
    pair: str
    ask: float
    bid: float
    quote: float
    timestamp: int

    def __init__(self, pair, ask, bid, quote, timestamp) -> None:
        super().__init__()
        self.bid = bid
        self.ask = ask
        self.pair = pair
        self.quote = quote
        self.timestamp = timestamp

    def as_dict(self):
        return {
            "pair": self.pair,
            "ask": self.ask,
            "bid": self.bid,
            "quote": self.quote,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, tick_data):
        # print(tick_data['pair'])
        return TickStream(
            tick_data['pair'],
            tick_data['ask'],
            tick_data['bid'],
            tick_data['quote'],
            tick_data['timestamp']
        )
