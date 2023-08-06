#!/usr/bin/python3
from urllib.parse import urlsplit, urlencode
import asyncio
import zlib
import gzip
import chardet
import ssl
import json as sjson
import h11

__all__ = ["get", "post", "head", "put", "delete", "options", "patch", "Session", "ConnectionError", "ConnectionTimeout"]

__version__ = "v0.2.0"


async def get(url, **kwargs):

    return await Session().get(url, **kwargs)

async def post(url, **kwargs):

    return await Session().post(url, **kwargs)

async def head(url, **kwargs):

    return await Session().head(url, **kwargs)

async def put(url, **kwargs):

    return await Session().put(url, **kwargs)

async def delete(url, **kwargs):

    return await Session().delete(url, **kwargs)

async def options(url, **kwargs):

    return await Session().options(url, **kwargs)

async def patch(url, **kwargs):

    return await Session().patch(url, **kwargs)


class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key.title(), value)

    def __getitem__(self, key):
        return super().__getitem__(key.title())

    def __delitem__(self, key):
        super().__delitem__(key.title())

    def copy(self):
        return CaseInsensitiveDict(**self._data)


class Response:
    def __init__(self):
        self.status_code = None
        self.headers = None
        self.content = None
        self.url = None
        self.encoding = None
        self.cookies = None
        self._sock = None

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    @property
    def text(self):
        return self.content.decode(self.encoding, "replace") if self.content else ""

    def json(self):
        if n:=self.text:
            return sjson.loads(n)

    def _setHeaders(self, headers):
        self.headers = CaseInsensitiveDict()
        for key, value in headers:
            self.headers[key.decode()] = value.decode()


class Session:
    def  __init__(self):
        self.netloc = ""
        self.writer = None
        self.keepAlive = False

    async def __aenter__(self):
        self.keepAlive = True
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None

    def __del__(self):
        if self.writer:
            self.writer.close()

    async def get(self, url, **kwargs):

        return await self.request("get", url, **kwargs)

    async def post(self, url, **kwargs):

        return await self.request("post", url,  **kwargs)

    async def head(self, url, **kwargs):

        return await self.request("head", url, **kwargs)

    async def put(self, url, **kwargs):

        return await self.request("put", url, **kwargs)

    async def delete(self, url, **kwargs):

        return await self.request("delete", url, **kwargs)

    async def options(self, url, **kwargs):

        return await self.request("options", url, **kwargs)

    async def patch(self, url, **kwargs):

        return await self.request("patch", url, **kwargs)

    async def request(self, method, url, retries=0, timeout=30, **kwargs):
        retries = int(retries)
        if not 0 <= retries: raise ValueError("retries must be positive integer")
        error = None
        for i in range(retries + 1):
            try:
                return await asyncio.wait_for(self._request(method, url, **kwargs), timeout=timeout)
            except Exception as e:
                error = e
                await self.close()

        if error:
            raise error from None

    async def _request(self, method, url, params=None, data=None, headers=None,
                     sslTimeout=20, cookies=None, verify=True, json=None, file=None):

        if method.lower() not in ("get", "post", "head", "put", "delete", "options", "patch"):
            raise ValueError(f"Unsupported method '{method}'")

        url = urlsplit(url)
        if self.keepAlive:
            if self.netloc:
                if self.netloc != url.netloc:
                    if self.writer:
                        await self.close()
                    self.netloc = url.netloc
            else:
                self.netloc = url.netloc
        method = method.upper()

        _headers = dict()
        _headers["Host"] = url.netloc
        _headers["User-Agent"] = f"arequest"
        _headers["Accept-Encoding"] = "gzip, deflate"
        _headers["Accept-Language"] = "*"
        _headers["Accept"] = "*/*"
        _headers["Connection"] = "keep-alive" if self.keepAlive else "close"

        if params:
            if isinstance(params, dict):
                query = urlencode(params)
            else:
                raise TypeError("params must be dict.")

            if url.query:
                query = f"?{url.query}&{params}"
            else:
                query = f"?{params}"
        else:
            query = f"?{url.query}" if url.query else None

        if headers:
            if isinstance(headers, dict):
                for i in headers:
                     _headers[str(i).title()] = headers[i]
            else:
                raise TypeError("headers argument must be a dict.")

        if cookies:
            if isinstance(cookies, dict):
                cookies = urlencode(cookies)
            elif not isinstance(cookies, str):
                raise TypeError("cookies argument must be a dict or a str.")

            _headers["Cookie"] = cookies

        elif data:
            if isinstance(data, dict):
                data = urlencode(data)
            elif not isinstance(data, str):
                raise TypeError("data argument must be a dict or a str.")

            _headers["Content-Length"] = str(len(data))
            _headers["Content-Type"] = "application/x-www-form-urlencoded"

        if json:
            if isinstance(json, dict):
                data = sjson.dumps(json, default=str)
                _headers["Content-Length"] = str(len(data))
                _headers["Content-Type"] = "application/json"
            else:
                raise TypeError("json argument must be a dict.")

        elif file:
            pass


        headers = []
        for key, value in _headers.items(): 
            headers.append((key, value))

        headers.sort()
        conn = h11.Connection(our_role=h11.CLIENT)
        sendData = conn.send(h11.Request(method=method, target=f"{url.path or '/'}{query or ''}", headers=headers))

        if self.keepAlive and self.writer:
            writer = self.writer
            reader = self.reader
        else:
            if url.scheme == "https":
                if not verify:
                    sslTimeout = None
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                reader, writer = await asyncio.open_connection(
                    url.hostname, url.port or 443, ssl=verify or context, ssl_handshake_timeout=sslTimeout)
            elif url.scheme == "http":
                reader, writer = await asyncio.open_connection(
                    url.hostname, url.port or 80)
            else:
                raise ValueError("Unknown scheme '{url.scheme}'")

        writer.write(sendData)
        if data:
            writer.write(conn.send(h11.Data(data=data.encode())))
        writer.write(conn.send(h11.EndOfMessage()))


        r = Response()
        content = []
        while True:
            try:
                event = conn.next_event()
            except h11.ProtocolError:
                raise ConnectionError("connection close.")
            if event is h11.NEED_DATA:
                conn.receive_data(await reader.read(2048))
                continue
            elif isinstance(event, h11.Response):
                r._setHeaders(event.headers)
                r.status_code = event.status_code
            elif isinstance(event, h11.Data):
                content.append(event.data)
            elif isinstance(event, h11.ConnectionClosed):
                raise ConnectionError("h11 ConnectionClosed event.")
            elif type(event) is h11.EndOfMessage:
                break

        content = b"".join(content)
        if self.keepAlive and r.headers.get("Connection").lower() == "keep-alive":
            conn.start_next_cycle()
            self.reader = reader
            self.writer = writer
        else:
            if self.writer:
                await self.close()
            else:
                writer.close()
                await writer.wait_closed()

        r.url = url.geturl()

        if not content:
            return r

        # r.cookies = {}
        # while line := await reader.readline():
        #     line = line.decode().rstrip()
        #     if line:
        #         k, v = line.split(": ", 1)
        #         if k == "Set-Cookie":
        #             c = v.split(";", 1)[0].strip().split("=")
        #             if len(c) == 2:
        #                 r.cookies[c[0]] = c[1].strip("\"")
        #         else:
        #             r.headers[k] = v
        #     else:
        #         content = await reader.read()
        #         writer.close()
        #         break

        if (t := r.headers.get("Content-Encoding")):
            if t == "gzip":
                content = gzip.decompress(content)

            elif t == "deflate":
                content = zlib.decompress(content)

            else:
                raise TypeError(f"Unsupported Content-Encoding '{t}'")

        if r.headers.get("Content-Type") and r.headers["Content-Type"].find("charset") != -1:
            r.encoding = r.headers["Content-Type"].split("charset=")[1]
        else:
            r.encoding = chardet.detect(content)["encoding"]

        r.content = content
        return r


class ConnectionError(Exception):
    pass


class ConnectionTimeout(ConnectionError):
    pass


async def main():
    r = await get("https://10.30.1.11/get", timeout=0.1)
    print(r.headers)
    print(r.status_code)
    print(r.encoding)
    print(r.text)
    # print(r.json())


if __name__ == '__main__':
    asyncio.run(main())




