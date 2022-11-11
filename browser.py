from utils import *

def load(url):
    headers, body = request(url)
    show(body)


if __name__ == "__main__":
    import sys
    load(sys.argv[1])