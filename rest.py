import tornado.httpserver
import tornado.ioloop
import tornado.web
import sqlite3

_db = sqlite3.connect('shop.db')
_cursor = _db.cursor()


class SensorRequestHandler(tornado.web.RequestHandler):
    def get(self, arg):
        price = self.get_argument("price", None)
        quantity = self.get_argument("quantity", None)
        value = self.get_argument("value", None)
        if price:
            _cursor.execute("SELECT price FROM data WHERE ID = '" + arg + "'")
            data = _cursor.fetchone()
            self.write(arg + " unit price: " + str(format(data[0], '.2f')))
        elif quantity:
            _cursor.execute("SELECT quantity FROM data WHERE ID = '" + arg + "'")
            data = _cursor.fetchone()
            self.write(arg + " stock level: " + str(data[0]))
        elif value:
            _cursor.execute("SELECT price FROM data WHERE ID = '" + arg + "'")
            cost = _cursor.fetchone()
            _cursor.execute("SELECT quantity FROM data WHERE ID = '" + arg + "'")
            amount = _cursor.fetchone()
            self.write(arg + " total stock value:" + str(format(cost[0]*amount[0], ".2f")))

    def put(self, item):
        self.write(item)
        price = self.get_argument("price", None)
        quantity = self.get_argument("quantity", None)
        if item == "milk" or item == "flower":
            if price:
                value = float(self.get_argument("price"))
                record = (item, float(self.get_argument("price"), ))
                _cursor.execute("UPDATE data SET price = " + str(value) + " WHERE ID = '" + item + "'")
                _db.commit()
                self.write('OK')
            elif quantity:
                value = int(self.get_argument("quantity"))
                record = (item, int(self.get_argument("quantity"), ))
                _cursor.execute("UPDATE data SET quantity = " + str(value) + " WHERE ID = '" + item + "'")
                _db.commit()
                self.write('OK')
        else:
            self.write(item)


class DatabaseHandler(tornado.web.RequestHandler):
    def get(self):
        for line in _db.iterdump():
            self.write('%s\n' % line)