import asyncio, signal
from websockets.asyncio.client import connect


async def send(message, host=None, port=None):

    if not port:
        port = 8090

    if not host:
        host = '127.0.0.1'

    uri = f'ws://{host}:{port}'
    
    async with connect(uri) as websocket:
        await websocket.send(message)



