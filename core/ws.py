import asyncio, json, uuid, sys, signal
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
import core.util


class MessageServer(object):

    
    def __init__(self, port=None):
        self.port = port
        self.connected = {}
        self.subscribed = []
        asyncio.run(self.main())


    async def process_message(self, uid, message):
        if 'action' in message:
            message_handler = getattr(self, message['action'], None)
            if message_handler:
                await message_handler(uid, message)


    async def subscribe(self, uid, message):
        self.subscribed.append(uid)
        await self.send_data(uid, {'status': 'OK'})


    async def send_data(self, uid, data):
        await self.connected[uid].send(json.dumps(data))


    async def broadcast(self, uid, data):
        for uid in self.subscribed:
            await self.send_data(uid, data)
        

    async def cleanup(self):
        print('message server shutting down...')
        

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
                    del self.connected[uid]
                    break
        finally:
            if uid in self.connected:
                print(f'removing connection: {uid}')
                del self.connected[uid]
            

    async def main(self):
        if self.port:
            port = self.port
        else:
            port = 8090

        print(f'Message server starting on port {port}...')
            
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

        async with serve(self.handler, "", port):
            await stop
            await self.cleanup()

            
if __name__ == "__main__":

    port = None
    
    if len(sys.argv) > 1:
        port = sys.argv[1]

    MessageServer(port=port)
    


    
