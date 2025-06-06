# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import socket


class Response:
    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson

        return ujson.loads(self.content)


def _request(
    modem,
    method,
    url,
    data=None,
    json=None,
    headers={},
    stream=None,
    auth=None,
    timeout=None,
    parse_headers=True,
):
    redirect = None  # redirection url, None means no redirection
    chunked_data = data and getattr(data, "__next__", None) and not getattr(data, "__len__", None)

    if auth is not None:
        import binascii

        username, password = auth
        formated = b"{}:{}".format(username, password)
        formated = str(binascii.b2a_base64(formated)[:-1], "ascii")
        headers["Authorization"] = "Basic {}".format(formated)

    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ssl

        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = modem.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
    ai = ai[0]

    resp_d = None
    if parse_headers is not False:
        resp_d = {}

    s = modem.socket(ai[0], socket.SOCK_STREAM, ai[2])
    if timeout is not None:
        # Note: settimeout is not supported on all platforms, will raise
        # an AttributeError if not available.
        s.settimeout(timeout)

    try:
        s.connect(ai[-1])
        if proto == "https:":
            s = modem.wrap_socket(s, server_hostname=host)
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if "Host" not in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if json is not None:
            assert data is None
            import ujson

            data = ujson.dumps(json)
            s.write(b"Content-Type: application/json\r\n")
        if data:
            if chunked_data:
                s.write(b"Transfer-Encoding: chunked\r\n")
            else:
                if getattr(data, "readinto", None):
                    s.write(b"Content-Length: %d\r\n" % len(data.seek(0, 2)))
                else:
                    s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"Connection: close\r\n\r\n")
        if data:
            if chunked_data:
                for chunk in data:
                    s.write(b"%x\r\n" % len(chunk))
                    s.write(chunk)
                    s.write(b"\r\n")
                s.write("0\r\n\r\n")
            else:
                if getattr(data, "readinto", None):
                    l = data.seek(0, 2)
                    to_read = data.seek(0, 0)
                    buf = bytearray(1024)
                    while to_read < l:
                        r = data.readinto(buf)
                        if r == 1024:
                            s.write(buf)
                        else:
                            s.write(buf[:r])
                        to_read += r
                    data.close()
                else:
                    s.write(data)

        l = s.readline()
        print(f"request2 l: {repr(l)}")
        l = l.split(None, 2)
        if len(l) < 2:
            # Invalid response
            raise ValueError("HTTP error: BadStatusLine:\n%s" % l)
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            # print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + str(l, "utf-8"))
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                if status in [301, 302, 303, 307, 308]:
                    redirect = str(l[10:-2], "utf-8")
                else:
                    raise NotImplementedError("Redirect %d not yet supported" % status)
            if parse_headers is False:
                pass
            elif parse_headers is True:
                l = str(l, "utf-8").strip()
                if ":" in l:
                    k, v = l.split(":", 1)
                    resp_d[k.strip()] = v.strip()
                else:
                    pass
            else:
                parse_headers(l, resp_d)
    except OSError:
        s.close()
        raise

    if redirect:
        s.close()
        if status in [301, 302, 303]:
            return _request("GET", redirect, None, None, headers, stream)
        else:
            return _request(method, redirect, data, json, headers, stream)
    else:
        resp = Response(s)
        resp.status_code = status
        resp.reason = reason
        if resp_d is not None:
            resp.headers = resp_d
        return resp


def urlencode(query):
    if not isinstance(query, dict):
        raise TypeError

    l = []
    for k, v in query.items():
        if isinstance(k, bytes) or isinstance(k, bytearray):
            k = k.decode("utf-8")
        else:
            k = str(k)

        if isinstance(v, bytes) or isinstance(v, bytearray):
            v = v.decode("utf-8")
        else:
            v = str(v)
        l.append(k + "=" + v)

    return "&".join(l)
