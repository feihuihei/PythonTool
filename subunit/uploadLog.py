import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options
import os
import urllib.parse
import time

define("port", default=8098, help="run on 11000 port", type=int)

class LogHandler(tornado.web.RequestHandler):
    path = "/home/homework/log/loggrove/"
    def get(self):
       pass

    def post(self):
        host = self.request.remote_ip
        param = self.request.body
        if not param:
            self.write("param is none...")
        param = param.decode(encoding='utf-8')
        paramArr = param.split('\n')
        path = self.path + host
        if not os.path.exists(path):
            os.makedirs(path)
        path = path + '/point.log'
        for log in paramArr:
            if not log:
                continue
            logcontent = urllib.parse.unquote(urllib.parse.unquote(log))
            content = logcontent.split('&')
            dic = {}
            for ss in content:
                arr = ss.split('=')
                if len(arr) == 2:
                    dic.setdefault(arr[0],arr[1])
            self.write(str(dic))
            content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ": " + dic.__str__() + '\n\n'
            with open(path, 'a+') as f:
                f.write(content)
#iosyike
class IosYkLogHandler(tornado.web.RequestHandler):
    path = "/home/homework/log/loggrove/"
    def get(self):
       pass

    def post(self):
        host = self.request.remote_ip
        param = self.request.body
        if not param:
            self.write("param is none...")
        param = param.decode(encoding='utf-8')
        paramArr = param.split('\n')
        path = self.path + host
        if not os.path.exists(path):
            os.makedirs(path)
        path = path + '/point.log'
        for log in paramArr:
            if not log:
                continue
            logcontent = urllib.parse.unquote(urllib.parse.unquote(log))
            content = logcontent.split('&')
            dic = {}
            for ss in content:
                arr = ss.split('=')
                if len(arr) == 2:
                    dic.setdefault(arr[0],arr[1])
            self.write(str(dic))
            content = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ": " + dic.__str__() + '\n\n'
            with open(path, 'a+') as f:
                f.write(content)

class LogRuleHandler(tornado.web.RequestHandler):
    def get(self):
       pass

    def post(self):
        dic = {
	        "sessionTimeout": 30,
            "storageExpires": 10,
            "sendMaxLength": 100,
            "sendInterval": 1,
            "sendIntervalWifi": 30,
            "onlywifi": False,
            "sampleRate": {
                "default": 1
            }
        }
        self.write(dic.__str__())

application = tornado.web.Application(handlers=[
    (r'^/nlogtj/ctj/zuoye.*', LogHandler),
    (r'^/nlogtj/yike.*', IosYkLogHandler),
    (r'^/nlogtj/rule.*', LogRuleHandler),
    ],
    settings = dict(
        compress_response = True,
    ),
    autoreload = True)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application,
                                                decompress_request=True,
                                                )
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()