from tortoise import Tortoise
from config import DATABASE_CONFIG

async def init():
    await Tortoise.init(config=DATABASE_CONFIG)
    await Tortoise.generate_schemas()

async def close():
    await Tortoise.close_connections()