import ssl
import socket

def request(url):
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP
    )
    scheme, url = url.split("://", 1)
    assert scheme in ["http", "https"], \
        "Unknown scheme {}".format(scheme)
    host, path = url.split("/", 1)
    path = "/" + path
    
    # Wrap the socket to use SSL (HTTPS)
    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    port = 80 if scheme == "http" else 443

    # You can set a custom port in the host
    if ":" in host:
        host, port = host.split(":", 1)
    port = int(port)
    
    s.connect((host, port))

    s.send("GET {} HTTP/1.0\r\n".format(path).encode("utf8") +
        "Host: {}\r\n\r\n".format(host).encode("utf 8"))

    # The \r\n\r\n at the end are essential, so it sends that blank line at the end of the request
    # If you forget that, the other computer will keep waiting on you to send that newline, 
    # and you'll keep waiting on its response.

    response = s.makefile("r", encoding="utf8", newline="\r\n")

    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    headers={}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip() #strip function removes any empty spaces

    assert "transfer-encoding" not in headers
    assert "content-encoding" not in headers

    body = response.read()
    s.close()

    return headers, body


def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")