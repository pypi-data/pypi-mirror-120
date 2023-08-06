from .nodewire import Nodewire
import json
import inspect
import asyncio

from .message import Message

will_get = {}

class _Node():
    def __init__(self, nw, name, gateway):
        self.name = name
        self.nw = nw
        self.gateway = gateway
        self.ports = {}

    def __iter__(self):
        self.iterobj = iter(self.ports)
        return self.iterobj

    def __next__(self):
        next(self.iterobj)

    def __unicode__(self):
        return self.name + str(self.ports)

    def __repr__(self):
        return self.name + str(self.ports)

    def __str__(self):
        return self.name + str(self.ports)

    def __contains__(self, item):
        return item in self.ports

    def __getitem__(self, item):
        if item in self.ports:
            return self.ports[item]
        elif item == 'name':
            return self.name
        else:
            return None

    def __setitem__(self, key, value):
        self.nw.send(self.gateway+':'+self.name, 'set', key, json.dumps(value))

    def set(self, key,value):
        self.ports[key] = value

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        if key in ['nw', 'name', 'gateway', 'ports']:
            super(_Node, self).__setattr__(key, value)
        else:
            if key.startswith('on_'):
                self.__dict__[key] = value
                #super(_Node, self).__setattr__(key, value) # todo: check if this is a method
            else:
                self.__setitem__(key, value)

class Node:
    def __init__(self, nodename='pynode', inputs='', outputs='', server = 's2.nodewire.org'):
        self.nw = Nodewire(nodename, process=self.process, server = server)
        self.nw.debug = False
        self.nodes = []
        self.sender = None
        self.inputs =  [{'port': i, 'value':0} for i in  inputs.split()]
        self.outputs = [{'port': o, 'value':0} for o in outputs.split()]
        self.queue = None

        for method in inspect.getmembers(self, predicate=inspect.ismethod):
            if method[0].startswith('get_'):
                port = method[0][4:]
                ports = [p for p in self.outputs if p['port'] == port]
                if ports != []: ports[0]['get'] = method[1]
            elif method[0].startswith('on_'):
                port = method[0][3:]
                ports = [p for p in self.inputs if p['port'] == port]
                if ports != []: ports[0]['on'] = method[1]
            elif method[0] == 'loop': 
                self.nw.on_connected = method[1]

    def get(self, item):
        ports = [p for p in self.outputs if p['port'] == item]
        if ports != []:
            port = ports[0]
            if 'get' in port:
                return port['get'](sender=self.sender)
            elif 'value' in port:
                return port['value']
            else:
                return 0
        else:
            ports = [p for p in self.inputs if p['port']==item]
            if ports != []:
                port = ports[0]
                return port['value']
            else:
                print('invalid port or attribute: {}'.format(item))
                return None
            # raise Exception('invalid port or attribute: {}'.format(item))

    def set(self, key, value):
        ports = [p for p in self.inputs if p['port'] == key]
        if ports != []:
            ports[0]['value'] = value
            if 'on' in ports[0]:
                if inspect.iscoroutinefunction(ports[0]['on']):
                    asyncio.create_task(ports[0]['on'](sender=self.sender, value=value))
                else:
                    ports[0]['on'](sender=self.sender, value=value)
        else:
            ports = [p for p in self.outputs if p['port'] == key]
            if ports != []:
                ports[0]['value'] = value
                self.nw.send('ee', 'val', key, json.dumps(value))

    def __getattr__(self, item):
        if item in ['nw', 'nodes', 'sender', 'inputs', 'outputs', 'queue'] or item.startswith('__'):
            return super(Node, self).__getattr__(item)
        ports = [p for p in self.inputs if p['port']==item]
        if ports != []:
            port = ports[0]
            return port['value']
        else:
            return self.get(item)

    def __setattr__(self, key, value):
        if key in ['nw', 'nodes', 'sender', 'inputs', 'outputs', 'queue'] or key.startswith('__'):
            super(Node, self).__setattr__(key, value)
        else:
            if key.startswith('on_'):
                port = key[3:]
                ports = [p for p in self.inputs if p['port'] == port]
                if ports!=[]: ports[0]['on']=value
            elif key.startswith('get_'):
                port = key[4:]
                ports = [p for p in self.outputs if p['port'] == port]
                if ports != []: ports[0]['get'] = value
            else:
                self.set(key, value)

    async def get_node(self, nodename, instance=None):
        if instance==None: instance = self.nw.gateway
        nodes = [n for n in self.nodes if n.name==nodename]
        if len(nodes) == 0:
            self.queue = asyncio.Queue()
            self.nw.send('cp','subscribe', nodename if instance==None else instance +':'+nodename, 'val')
            self.nw.send('cp', 'getnode', nodename)
            return await self.queue.get()
        else:
            return nodes[0]

    def process(self, msg:Message):
        if msg.command == 'get':
            if msg.port == 'ports':
                ports = ' '.join([o['port'] for o in self.outputs]) + ' ' + ' '.join([i['port'] for i in self.inputs])
                self.nw.send(msg.sender_full, 'ports', ports)
            else:
                self.sender = msg.sender_full
                result = getattr(self, msg.port, None)
                if inspect.iscoroutine(result):
                    def done(t):
                        self.nw.send(msg.sender, 'val', msg.port, json.dumps(task.result()))
                        self.sender = None
                    task = asyncio.create_task(result)
                    task.add_done_callback(done)
                else:
                    self.nw.send(msg.sender, 'val', msg.port, json.dumps(result))
                    self.sender = None
        elif msg.command == 'set':
            if msg.port in [p ['port'] for p in self.inputs]:
                self.sender = msg.sender
                setattr(self, msg.port, msg.value)
                self.sender = None
                self.nw.send(msg.sender, 'val', msg.port, json.dumps(getattr(self, msg.port, None)))
        elif msg.command == 'val':
            senders = [s for s in self.nodes if s.name==msg.sender and s.gateway==msg.sender_instance]
            if senders!=[]:
                senders[0].set(msg.port, msg.value)
                if 'on_' + msg.port in senders[0].__dict__:
                    senders[0].__dict__['on_' + msg.port](msg.sender_full)
        elif msg.command == 'node':
            msg.params[0] = msg.params[0].replace("'", '"')
            msg.params[0] = msg.params[0].replace('None', 'null')
            msg.params[0] = msg.params[0].replace('True', 'true')
            msg.params[0] = msg.params[0].replace('False', 'false')
            nodevalue = json.loads(msg.params[0])
            nodename = msg.params[1]
            gateway = msg.params[2]
            n = _Node(self.nw, nodename, gateway)
            if n not in self.nodes:
                for key in nodevalue:
                    n.set(key, nodevalue[key])
                self.nodes.append(n)
            if nodename in will_get:
                will_get[nodename](n)
                del will_get[nodename]
            if self.queue: self.queue.put_nowait(n)


if __name__ == '__main__':
    class MyNode(Node):
        def __init__(self):
            self.auto = False
            self.times = 0

        def lost_power(self, node):
            if sco.mains == 0 and self.auto: sco.ignition = 1
            self.times+=1

        def on_auto_switched(self, sender, value):
            self.auto = value

        def get_service_required(self, sender):
            return self.times>10

        async def loop(self):
            global sco
            sco = await self.get_node('sco')
            sco.on_mains = self.lost_power

    ## MAIN PROGRAM
    mynode = MyNode(inputs = 'auto_switch', outputs = 'service_required')
    mynode.nw.debug = True
    mynode.nw.run()