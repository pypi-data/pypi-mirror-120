import asyncio
import json

class Db(object):
    def __init__(self, nw, table):
        self.nw = nw
        self.table = table

    async def get(self, query, projection=None, options=None):
        """ahmad = await db.get({'age', 20})"""
        queue = asyncio.Queue()
        '''if projection is None:
            projection = {}'''
        if options is None:
            options = {}

        def db_result(msg):
            queue.put_nowait(msg.value)

        if projection == None and options == None:
            self.nw.send('db','get', self.table, json.dumps(query))
        else:
            self.nw.send('db','get', self.table, json.dumps(query), json.dumps(projection), json.dumps(options))
        self.nw.when('db.'+ self.table, db_result)
        return await queue.get()

    async def first(self, query, projection=None, options=None):
        result = await self.get(self.table, query, projection, options if options else {'$limit':1})
        if result:
            return result[0]
        else:
            return None

    async def last(self, query, projection=None, options=None):
        result = await self.get(self.table, query, projection, options if options else {'$limit':1, '$sort':{'$natural':-1}})
        if result:
            return result[-1]
        else:
            return None

    def index(self, keys, options = None):
        if options:
            self.nw.send('db', 'set', self.table, 'index', keys, options)
        else:
            self.nw.send('db', 'set', self.table, 'index', keys)

    def drop(self):
        """db.drop()"""
        self.nw.send('db','set', self.table, 'drop')

    def remove(self, query):
        """db.remove({'age',40})"""
        self.nw.send('db', 'set', self.table, 'remove', json.dumps(query))

    '''def set(self, value, value2=None):
        """db.set({'name':'ahmad', 'age': 40})"""
        if value2:
            return self.nw.send('db', 'set', self.table, json.dumps(value), json.dumps(value2))
        return self.nw.send('db', 'set', self.table, json.dumps(value))'''

    def update(self, query, value):
        """db.set({'name':'ahmad', 'age': 40}, {'$set':{'age':41}})"""
        return self.nw.send('db', 'set', self.table, json.dumps(query), json.dumps(value))

    async def set(self, value, value2=None):
        """db.set({'name':'ahmad', 'age': 40})"""
        queue = asyncio.Queue()

        def db_result(msg):
            queue.put_nowait(msg.value)

        if value2:
            self.nw.send('db', 'set', self.table, json.dumps(value), json.dumps(value))
        else:
            self.nw.send('db', 'set', self.table, json.dumps(value))
        self.nw.when('db.' + self.table + '_id', db_result)
        return await queue.get()

if __name__ == '__main__':
    from . import Node
    async def myloop():
        await asyncio.sleep(10)
        test_db = Db(ctrl.nw, 'test')
        ahmad = await test_db.get({})
        print(ahmad)

    async def connected():
        await asyncio.sleep(10)
        test_db = Db(node.nw)
        #id = await test_db.set_wait({'name':'ahmad sadiq', 'age': 43})
        #print(id)
        r = await test_db.first({}, 'test')
        print(r)


    node = Node()
    node.nw.on_connected = connected
    node.nw.debug = True
    node.nw.run(myloop())