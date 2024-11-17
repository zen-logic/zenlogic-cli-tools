import asyncio
from websockets.asyncio.client import connect


async def send(message, port=None):
    if not port:
        port = 8090

    uri = f'ws://localhost:{port}'
    async with connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response
    
        
if __name__ == "__main__":
    response = asyncio.run(send('{"message": "Hello World!"}'))
    print(f"{response}")
