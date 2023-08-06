import ujson
import usocket

class URL:
    def __init__(self, protocol: str, host: str, port: int, *resources):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.resources = resources

    def __call__(self, *resources):
        return '{}://{}:{}{}'.format(self.protocol, self.host, self.port, self.path(*resources))

    def __repr__(self):
        return self()

    def path(self, *resources):
        resources = self.resources + resources
        return '/' + '/'.join(resources) if len(resources) > 0 else ''

class Response:
    def __init__(self, file = None, status: int = 0, headers: dict = {}, encoding: str = 'utf-8'):
        self.file = file
        self.status = status
        self.headers = headers
        self.encoding = encoding
        self._cache = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
        self._cache = None

    @property
    def content(self):
        if self._cache is None:
            try:
                self._cache = self.file.read().decode(self.encoding)
            finally:
                self.file.close()
                self.file = None
        return self._cache

    @property
    def text(self):
        return str(self.content, self.encoding)

    @property
    def json(self):
        return ujson.loads(self.content)

def request(url: URL, data = None, method: str = 'GET', headers: dict = {}):
    response = Response()
    try:
        addr = usocket.getaddrinfo(url.host, url.port, 0, usocket.SOCK_STREAM)[0]
        sock = usocket.socket(addr[0], addr[1], addr[2])
        sock.connect(addr[-1])
        sock.write(b"%s /%s HTTP/1.0\r\n" % (method, url.path()))

        if not "Host" in headers:
            sock.write(b"Host: %s\r\n" % url.host)

        for key in headers:
            sock.write(key)
            sock.write(b": ")
            sock.write(headers[key])
            sock.write(b"\r\n")

        if data:
            sock.write(b"Content-Length: %d\r\n" % len(data))

        sock.write(b"\r\n")

        if data:
            sock.write(data)

        header = sock.readline()
        status = int(header.split(b' ')[1])

        headers = {}
        line = sock.readline()
        while line != b'\r\n':
            header, value = line.rstrip().split(b': ', 1)
            headers[header] = value
            line = sock.readline()
        response = Response(sock, status, headers)
    except:
        if sock:
            sock.close()
    finally:
        return response

def head(url: URL, **kwargs):
    return request(url, method='HEAD', **kwargs)

def get(url: URL, **kwargs):
    return request(url, method='GET', **kwargs)

def post(url: URL, **kwargs):
    return request(url, method='POST', **kwargs)

def put(url: URL, **kwargs):
    return request(url, method='PUT', **kwargs)

def patch(url: URL, **kwargs):
    return request(url, method='PATCH', **kwargs)

def delete(url: URL, **kwargs):
    return request(url, method='DELETE', **kwargs)
