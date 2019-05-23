# coding: utf-8
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler
import os,json
import web.dao
define("port", default=8000, type=int, help="run server on the given port.")


class IndexHandler(RequestHandler):
    def get(self):
        pass


class UploadHandler(RequestHandler):
    url = 'git@afpai.com'
    path = '/home/node6/webroot'
    def post(self):
        result = {}
        result['flag'] = 0
        result['msg'] = ''
        abs_path = self.path + '/' + self.url
        try:
            meta = self.request.files['file'][0]
            data = self.request.body_arguments
            fileName = data.get('fileName')[0].decode('utf-8')
            group = data.get('group')[0].decode('utf-8')
            module = data.get('module')[0].decode('utf-8')
            branch = data.get('branch')[0].decode('utf-8')
            node = data.get('node')[0].decode('utf-8')
            if not group or not module or not branch or not node:
                result['flag'] = -2
                result['msg'] = 'group, module, branch or node was wrong.'
                self.write(json.dumps(result))
            #拼接文件存储的绝对路径
            abs_path = abs_path + '/' + group + '/' + module + '/' + branch
            if not os.path.exists(abs_path):
                os.makedirs(abs_path)
            abs_path = abs_path + '/'+ fileName
            while os.path.exists(abs_path):
                print('文件已存在.......正在删除文件.......')
                os.remove(abs_path)
            f = open(abs_path, 'wb')
            f.write(meta['body'])
            f.close()
            result['flag'] = 1
            result['msg'] = 'success'
        except Exception:
            result['flag'] = 0
            result['msg'] = 'failed in upload file....'
            return result
        # 将redis中的ext字段中的文件路径替换为url
        redis = web.dao.PreviousCompileDao(node, self.url, group, module, branch)
        value = redis.get()
        if value:
            opssite_path = abs_path.replace(self.path,'')
            value['ext']['filename'] = "http://192.168.32.194:8090"+opssite_path
            redis.setex(value)
        else:
            result['flag'] = -1
            result['msg'] = '暂无已编译的文件'
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(result))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/upload", UploadHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()