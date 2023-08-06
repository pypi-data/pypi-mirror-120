import asyncio
import inspect

class Client():
    def __init__(self):
        self.reader = None
        self.writer = None
        self.received = None
        self.managed = True

    async def connect(self, serverHost='s2.nodewire.org', failed=None):
        while True:
            try:
                print('connecting to {} ...'.format(serverHost))
                self.reader, self.writer = await asyncio.open_connection(serverHost, 10001)
                while True:
                    try:
                        data = await self.reader.readline()
                        if len(data)==0:
                            await self.send_to_subscriber('disconnected')
                            break
                        else:
                            try:
                                await self.send_to_subscriber(data.decode().strip())
                            except Exception as ex1:
                                print(str(ex1))
                                if not self.managed: raise
                    except (ConnectionError, TimeoutError) as ex:
                        print(str(ex))
                        await self.send_to_subscriber('disconnected')
                        break
                print('Close the socket')
                if not failed is None:
                    failed(serverHost)
                self.close_connection()
                await asyncio.sleep(10)
                print('trying to reconnect...')
            except TimeoutError as Ex: # todo get the relevant exceptions: TimeoutError
                print(f'failed to connect:{Ex}')
                if not failed is None:
                    failed(serverHost)
                    # break
                await asyncio.sleep(30)
                print('trying to reconnect...')
        print('loop ended')

    def close_connection(self):
        if not self.writer is None:
            self.writer.close()
            self.writer = None

    async def send_to_subscriber(self, data):
        if self.received:
            if inspect.iscoroutinefunction(self.received):
                await self.received(data)
            else:
                self.received(data)

    async def sendasync(self, message):
        while(self.writer==None): 
            await asyncio.sleep(10)
            print('waiting for reconnect...')
        self.writer.write(message.encode())

    def send(self, message):
        self.writer.write(message.encode())

if __name__ == '__main__':
    c = Client()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(c.connect())
    except KeyboardInterrupt:
        pass
    loop.close()