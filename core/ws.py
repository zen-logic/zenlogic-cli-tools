import asyncio, json, uuid
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed


class MessageServer(object):

    
    def __init__(self):
        self.connected = {}
        asyncio.run(self.main())
        

    async def handler(self, websocket):
        uid = str(uuid.uuid4())
        print(f'new connection: {uid}')
        self.connected[uid] = websocket
        data = json.dumps({'id': uid})
        message = await websocket.send(data)

        try:
            while True:
                try:
                    message = await websocket.recv()
                    print(uid, json.loads(message))
                except ConnectionClosed as e:
                    print(e)
                    print(f'removing connection: {uid}')
                    del self.connected[uid]
                    break
        finally:
            if uid in self.connected:
                print(f'removing connection: {uid}')
                del self.connected[uid]
            

    async def main(self):
        async with serve(self.handler, "", 8001):
            await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    MessageServer()
    
