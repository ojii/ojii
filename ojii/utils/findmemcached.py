import os
import socket


class IP(object):
    def __init__(self):
        self.base = None
        
    def get(self, end):
        if not self.base:
            self.base = self._get_base()
        return '%s.%s' % (self.base, end)
    
    def _get_base(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        return s.getsockname()[0].rsplit('.', 1)[0]
ip_getter = IP()

def check(ip, port, timeout):
    try:
        socket.create_connection((ip, port), timeout)
        return ip
    except socket.error:
        return False

def find_local_memcachd(timeout=1, startip=1, endip=127, port=11211, cachefile=None):
    if cachefile and os.path.exists(cachefile):
        f = open(cachefile, 'r')
        first = f.read()
        f.close()
        if check(first, port, timeout):
            return first
    for end in xrange(startip, endip + 1):
        ip = ip_getter.get(end)
        if check(ip, port, timeout):
            if cachefile:
                f = open(cachefile, 'w')
                f.write(ip)
                f.close()
            return ip
    return None