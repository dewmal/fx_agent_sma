import socketio

from db.db import FxDataBase

fx_db = FxDataBase()

sio = socketio.AsyncServer(async_mode='aiohttp')

