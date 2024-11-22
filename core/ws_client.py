import asyncio, signal
from websockets.asyncio.client import connect


async def send(message, port=None):
    if not port:
        port = 8090

    uri = f'ws://127.0.0.1:{port}'
    async with connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response



