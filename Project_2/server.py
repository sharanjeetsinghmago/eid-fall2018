import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

import MySQLdb

'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes.
'''

db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="pythonspot")
cur = db.cursor()

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print ('new connection')

    def on_message(self, message):
        print ('message received:  %s' % message)
        # Reverse Message and send it back
        # print 'sending back message: %s' % message[::-1]
        # self.write_message(message[::-1])
        if message == "get_temp_last":
            cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                temp_last = row[1]
                ts = row[3]
            self.write_message("Latest Temp :" + temp_last +" Time : " +ts)

        if message == "get_humid_last":
            cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                humid_last = row[1]
                ts = row[3]
            self.write_message("Latest Humid :" + temp_last +" Time : " +ts)

        if message == "get_temp_avg":
            cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                temp_avg = row[2]
                ts = row[3]
            self.write_message("Average Temp :" + temp_last +" Time : " +ts)

        if message == "get_humid_avg":
            cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                hummid_avg = row[2]
                ts = row[3]
            self.write_message("Average Humid :" + temp_last +" Time : " +ts)

        if message == "get_temp_max":
            cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                temp_max = row[5]
                ts = row[3]
            self.write_message("Max Temp :" + temp_last +" Time : " +ts)

        if message == "get_humid_max":
            cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                humid_max = row[5]
                ts = row[3]
            self.write_message("Max Humid :" + temp_last +" Time : " +ts)

        if message == "get_temp_min":
            cur.execute("SELECT * FROM temp2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                temp_min = row[4]
                ts = row[3]
            self.write_message("Min Temp :" + temp_last +" Time : " +ts)

        if message == "get_humid_min":
            cur.execute("SELECT * FROM hum2 ORDER by id DESC LIMIT 1")
            for row in cur.fetchall():
                humid_min = row[4]
                ts = row[3]
            self.write_message("Min Humid :" + temp_last +" Time : " +ts)

    def on_close(self):
        print ("connection closed")

    def check_origin(self, origin):
        return True

application = tornado.web.Application([
    (r'/ws', WSHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
