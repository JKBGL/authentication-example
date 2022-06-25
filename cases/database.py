import databases
from objects import settings

conn = databases.Database(settings.SQL_URI)

async def init_pool():
    await conn.connect()
    
async def close_pool():
    await conn.disconnect()
