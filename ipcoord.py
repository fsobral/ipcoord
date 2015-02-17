import web
import json
import random

db = web.database(dbn='mysql', user='fsobral', db='ipcoord')

urls = (
    '/ipcoord', 'Coordenator',
    '/ipcoord/keygen', 'KeyGenerator'
)

app = web.application(urls, globals())


class KeyGenerator:

    def __init__(self):

        self._tablename = 'users'
        
        self._rchars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'

    def GET(self):

        inp = web.input()

        user = db.select(self._tablename,where='email = ' + web.sqlquote(inp.email))

        if len(user) == 0:

            _skey = ''.join(random.sample(self._rchars,30))

            db.insert(self._tablename,email=inp.email,skey=_skey)

        else:

            _skey = user[0].skey

        return _skey


class Coordenator:

    def __init__(self):

        self._tablename = 'mach_map'

    def DELETE(self):

        inp = web.input()

        r = db.delete(self._tablename,where='name = ' + \
                      web.sqlquote(inp.name) + ' and skey = ' + \
                      web.sqlquote(inp.skey))

        return r

    def PUT(self):

        inp = web.input()

        r = db.insert(self._tablename,name=inp.name, \
                      ip=inp.ip,skey=inp.skey, \
                      updated=web.SQLLiteral('NOW()'))

        return r

    def POST(self):

        inp = web.input()

        r = db.query('INSERT INTO ' + self._tablename + \
                     ' (name, ip, skey, updated) VALUES (\'' + inp.name + \
                     '\', \'' + inp.ip + '\', \'' + inp.skey + \
                     '\', NOW()) ON DUPLICATE KEY UPDATE ip = \'' + \
                     inp.ip + '\', updated = NOW()')

        return r

    def GET(self):
        
        jsonformat = False

        delay = 5

        inp = web.input()

        if inp.has_key('json'): jsonformat = True

        if inp.has_key('delay'):

            delay = int(inp.delay)

        machines = db.query('SELECT name,ip FROM ' + \
                            self._tablename + \
                            ' WHERE TIMESTAMPDIFF(MINUTE,updated,now()) <= ' + \
                            str(delay) + ' and skey = ' + \
                            web.sqlquote(inp.skey));

        s = ''

        if jsonformat:

            obj = list(machines)

            s = json.dumps(obj)

        else:

            for m in machines:

                s += m['name'] + '\t' + m['ip'] + '\n'

        return s;

if __name__ == "__main__":
    app.run()
