from pymongo import MongoClient

from data.data_models import TickStream

client = MongoClient('mongodb://localhost:27017')

db = client.fx_mas_app


class FxDataBase:
    async def insert_fx_tick(self, fx_tick: TickStream):
        fx_ticks = db.fx_ticks
        result = fx_ticks.insert_one(fx_tick.as_dict())
        return result.inserted_id
