import time
from .message import Message
import asyncio
from .client2 import Client
import json
import uuid
import inspect
import requests

debug = False # False for deployment

class Nodewire:
    def __init__(self, name='node', server='s2.nodewire.org', process=None):
        self.name = name
        self.type = name
        self.server_address = server
        self.gateway = ''
        self.id = 'None'
        self.callbacks = {}
        self.terminated = False
        self.client = Client()
        self.called_connected =  False
        self.connected = False

        self.ack = False
        self.waiting_config = False

        try:
            self.readconfig()
            # print(self.uuid)
        except Exception as ex:
            print('Failed to read configuration file. Creating new config...')
            self.uuid = str(uuid.uuid4())
            print(f'New UUID is {self.uuid}')
            self.register()
            self.token = 'None'
            self.name = name
            self.id = 'None'
            self.saveconfig()

        if self.process_command:
            self.client.received = self.process_command

        self.process = process
        self.on_connected = None
        self.debug = False

    def saveconfig(self):
        file = open('nw.cfg', 'w')
        file.write(json.dumps({
            'uuid': self.uuid,
            'token': self.token,
            'name': self.name,
            'id': self.id,
            'gateway': self.gateway
        }))
        file.close()

    def readconfig(self):
        file = open('nw.cfg', 'r')
        config = json.loads(file.read())
        self.uuid = config['uuid']
        self.token = config['token']
        if config['name']:
            self.name = config['name']
        self.id = config['id']
        self.gateway = config['gateway']
        file.close()

    async def start(self, loop):
        if self.token == 'None':
            await self.client.sendasync('cp Gateway id={}\n'.format(self.uuid))
            self.waiting_config = True
        else:
            await self.client.sendasync('cp Gateway key={} {}\n'.format(self.token, self.uuid))
        self.connected = True

    def send(self, Node, Command, *Params):
        if self.connected:
            try:
                cmd = Node + ' ' + Command + ' ' + ' '.join(param for param in Params) + (' ' + self.name if len(Params) != 0 else self.name)
                if self.debug:print(cmd)
                self.client.send(cmd+'\n')
                return True
            except Exception as ex:
                if self.debug:print(f'failed to send command over LAN, {ex}')
                asyncio.Task(self.disconnected())
                return False

    async def pinger(self):
        if self.debug: print('pinging...')
        while not self.ack:
            self.send('cp', 'ThisIs', self.id)
            await asyncio.sleep(5)

    async def keepalive(self):
        await asyncio.sleep(60)
        while True:
            self.ack = False
            try:
                self.send('cp', 'keepalive')
            except:
                await self.start(asyncio.get_event_loop())
            await asyncio.sleep(5)
            if not self.ack:
                if self.debug: print('didn\'t recieve ack')
                await self.disconnected()
            await asyncio.sleep(300)

    async def disconnected(self):
        self.client.close_connection()
        self.connected = False
        await self.start(asyncio.get_event_loop())

    def when(self, cmd, func):
        self.callbacks[cmd] = func

    async def process_command(self, cmd):
        self.last = time.time()
        if cmd == 'disconnected':
            await self.disconnected()
            return
        msg = Message(cmd)

        if self.debug: print(cmd)

        if msg.command == 'ack':
            self.ack = True
        elif msg.command == 'gack' and not self.called_connected:
            if self.waiting_config:
                self.waiting_config = False
                self.gateway = msg.address_instance
                self.token = msg.address
                self.saveconfig()
                await self.disconnected()
            if self.on_connected:
                self.called_connected = True
                if inspect.iscoroutinefunction(self.on_connected):
                    asyncio.create_task(self.on_connected())
                else:
                    self.on_connected()
        elif msg.command == 'authfail':
            if self.token != 'None':
                if self.debug: print('we have been deleted')
                self.token = 'None'
                self.saveconfig()
            else:
                self.register()
        elif msg.command == 'autherror':
            self.register()
        elif msg.command == 'ping':
            self.ack = False
            asyncio.Task(self.pinger())
        elif msg.command == 'get' and msg.port == 'id':
            self.send(msg.sender_full, 'id', self.id)
        elif msg.command == 'get' and msg.port == 'type':
            self.send(msg.sender_full, 'type', self.type)
        elif msg.command == 'set' and msg.port == 'id':
            self.id = msg.params[1]
            self.saveconfig()
        elif msg.command == 'set' and msg.port == 'name':
            self.name = msg.params[1]
            self.saveconfig()
            self.send(msg.sender_full, 'ThisIs')
        else:
            if self.process:
                self.process(msg)
        if msg.command == 'val':
            signal = (msg.sender_full if msg.sender_instance!=msg.address_instance else msg.sender) + '.' + msg.port
            if signal in self.callbacks:
                self.callbacks[signal](msg)
        elif msg.command in self.callbacks:
                self.callbacks[msg.command](msg)

    def register(self):
        print('Please present the account credentials to authorize this node\n(This will be used to create a token but your username and passwords are never stored)')
        email =  input('Enter account name: ')
        pwd = input('Enter password: ')
        try:
            server = self.server_address
            if server == 'localhost': server+=':5001'
            print('https://'+server+'/login')
            token = requests.post('https://'+server+'/login', json={'email': email, 'pwd': pwd})
            result = requests.post('https://'+server+'/add_gateway', json={'gateway': self.uuid}, headers={"Authorization": f"Bearer {token.text}"})
            print(result.text)
            if result.text == 'success':
                asyncio.Task(self.disconnected())
        except Exception as ex:
            print(ex)

    async def run_async(self):
        loop = asyncio.get_event_loop()
        await asyncio.gather(
            asyncio.create_task(self.client.connect(serverHost=self.server_address)),
            asyncio.create_task(self.start(loop)),
            asyncio.create_task(self.keepalive())
        )

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(self.client.connect(serverHost=self.server_address)),
            loop.create_task(self.start(loop)),
            loop.create_task(self.keepalive())
        ]
        wait_tasks = asyncio.wait(tasks)
        try:
            loop.run_until_complete(wait_tasks)
        except KeyboardInterrupt:
            loop.stop()
            loop.run_until_complete(loop.shutdown_asyncgens())
        except SystemExit:
            loop.stop()
            loop.run_until_complete(loop.shutdown_asyncgens())

if __name__ == '__main__':
    nw = Nodewire('pyNode')
    nw.debug = True
    nw.run()

