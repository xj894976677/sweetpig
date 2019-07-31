from wgsiServer.wgsi_server import WSGIServer
from app import app
import atexit
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9003
    print('running http://{}:{}'.format(host, port))
    server = WSGIServer(host, port, app)
    atexit.register(server.server_close)
    server.serve_forever()
