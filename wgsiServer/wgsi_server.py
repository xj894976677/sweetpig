import selectors
import socket
from wgsiServer.http_parsed import BaseRequest
import time


class WSGIServer(object):

    def __init__(self, host, port, application):
        self.app = application
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.address = (host, port)
        self.request_queue_size = 5
        self.open_socket()

    def accept(self, sock, mask):
        sel = self.selector
        conn, addr = sock.accept()  # Should be ready
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def write(self, sock, mask):

        print('write')
        sel = self.selector

        # # 组织相应 头信息(header)
        # response_headers = "HTTP/1.1 200 OK\r\n"  # 200表示找到这个资源
        # response_headers += "\r\n"  # 用一个空的行与body进行隔开
        # # 组织 内容(body)
        # response_body = "hello world"
        #
        # response = response_headers + response_body
        # sock.send(response.encode("utf-8"))
        body = self.app(self.req.getenv(), self.start_response)
        for data in body:
            self.response += data
        resp = self.response
        sock.send(resp)
        sel.unregister(sock)
        sock.close()

    def read(self, conn, mask):
        sel = self.selector

        data = conn.recv(1000)  # Should be ready
        if data:
            conn.setblocking(False)
            sel.unregister(conn)

            # print('echoing', repr(data))

            s = data.decode('utf-8')
            self.req = BaseRequest(s)
            # print(self.req.headers)

            sel.register(conn, selectors.EVENT_WRITE, self.write)
        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

    def server_close(self):

        self.sock.close()
        self.selector.close()

    def server_bind(self):
        """
        绑定
        """
        sock = self.sock

        sock.bind(self.address)
        self.server_address = sock.getsockname()

    def server_listen(self):
        """
        监听
        """
        self.sock.listen(self.request_queue_size)

    def open_socket(self):
        sock = self.sock

        self.server_bind()
        self.server_listen()
        sock.setblocking(False)

    def serve_forever(self):
        sock = self.sock
        sel = self.selector

        sel.register(sock, selectors.EVENT_READ, self.accept)
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        finally:
            print('close')
            self.server_close()

    def start_response(self, status, headers_list):
        """
        :return:
        """

        r = 'HTTP/1.1 {}\r\n'.format(status)
        for h in headers_list:
            k = h[0]
            v = h[1]
            r += '{}: {}\r\n'.format(k, v)
        # r += "Server: sweetpig-wsgi\r\n"
        r += '\r\n'
        # r += "Date: %s\r\n" % format_date_time(time.time())
        r += "Server: sweetpig-wsgi\r\n"
        self.response = r.encode()


_weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_monthname = [None, # Dummy so we can use 1-based month numbers
              "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def format_date_time(timestamp):
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    return "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
        _weekdayname[wd], day, _monthname[month], year, hh, mm, ss
    )
