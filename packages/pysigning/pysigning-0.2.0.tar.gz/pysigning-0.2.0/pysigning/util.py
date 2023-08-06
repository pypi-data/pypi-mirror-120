import sys

def tobytes(x, raw=False):
    if isinstance(x, str):
        if not raw:
            if x == '-':
                return sys.stdin.buffer.read()
            if x.startswith('@'):
                filename = x[1:]
                if filename == '-':
                    return sys.stdin.buffer.read()
                with open(filename, 'rb') as f:
                    return f.read()
        x = x.encode('utf8')
    return x