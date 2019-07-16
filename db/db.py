from bson import ObjectId
from pymongo import MongoClient
import pymongo.results
import settings
from data.data_models import TickStream, TickWindow

client = MongoClient(f'mongodb://{settings.db_host()}')

db = client.fx_mas_app


class FxDataBase:

    async def insert_fx_window(self, fx_window: TickWindow):
        fx_windows = db.fx_window
        search_q = {"epoch": fx_window.epoch, "symbol": fx_window.symbol}
        fx_window_data = fx_windows.find_one(search_q)
        if fx_window_data:
            result = fx_windows.update_one(search_q, {"$set": fx_window.as_dict()})
            # print("Update ", )
            return str(fx_window_data['_id'])
        else:
            result = fx_windows.insert_one(fx_window.as_dict())
            return result.inserted_id

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

    async def get_fx_window(self, window_id):
        fx_windows = db.fx_window
        # print(fx_window_id)
        fx_window_id = ObjectId(window_id)
        tick_data = fx_windows.find_one({"_id": fx_window_id})
        return TickWindow.from_dict(tick_data)
