import asyncio, json, uuid, sys, signal
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
import core.util


class MessageServer(object):

    
    def __init__(self, port=None):
        self.loop = None
        self.stop = None
        self.port = port
        self.connected = {}
        self.subscribed = set()
        asyncio.run(self.main())


    async def process_message(self, uid, message):
        if 'action' in message:
            message_handler = getattr(self, message['action'], None)
            if message_handler:
                await message_handler(uid, message)


    async def subscribe(self, uid, message):
        self.subscribed.add(uid)
        await self.send_data(uid, {'status': 'OK'})


    async def send_data(self, uid, data):
        await self.connected[uid].send(json.dumps(data))


    async def broadcast(self, uid, data):
        for uid in self.subscribed:
            del data['action']
            await self.send_data(uid, data)
        

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
                    data = json.loads(message)
                    print(uid, data)
                    await self.process_message(uid, data)
                except ConnectionClosed as e:
                    print(e)
                    print(f'removing connection: {uid}')
                    if uid in self.subscribed:
                        self.subscribed.remove(uid)
                    del self.connected[uid]
                    break
        finally:
            if uid in self.connected:
                print(f'removing connection: {uid}')
                if uid in self.subscribed:
                    self.subscribed.remove(uid)
                del self.connected[uid]


    def cleanup(self, *args):
        print('message server shutting down...')
        if self.stop and not self.stop.done():
            self.stop.set_result(0)


    async def main(self):
        if self.port:
            port = self.port
        else:
            port = 8090

        print(f'Message server starting on port {port}...')
            
        self.loop = asyncio.get_running_loop()
        self.stop = self.loop.create_future()
        self.loop.add_signal_handler(signal.SIGTERM, self.cleanup, None)
        async with serve(self.handler, "", port):
            await self.stop

        # async with serve(self.handler, "", port):
        #     await asyncio.get_running_loop().create_future()
        #     await self.cleanup()
            

def run(port):
    MessageServer(port=port)
    
