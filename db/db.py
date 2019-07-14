from bson import ObjectId
from pymongo import MongoClient

from data.data_models import TickStream

client = MongoClient('mongodb://localhost:27017')

db = client.fx_mas_app


class FxDataBase:
    async def insert_fx_tick(self, fx_tick: TickStream):
        fx_ticks = db.fx_ticks
        result = fx_ticks.insert_one(fx_tick.as_dict())
        return result.inserted_id

    async def get_fx_tick(self, fx_tick_id):
        fx_ticks = db.fx_ticks
        # print(fx_tick_id)
        fx_tick_id = ObjectId(fx_tick_id)
        tick_data = fx_ticks.find_one({"_id": fx_tick_id})
        return TickStream.from_dict(tick_data)
