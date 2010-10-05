import os
import time

LOCKDIR = os.path.join(os.getcwd(), '.lock/')
if not os.path.exists(LOCKDIR):
    os.mkdir(LOCKDIR)

    
class SimpleLockError(Exception): pass
class LockAlreadyActive(SimpleLockError): pass
class LockNotActive(SimpleLockError): pass
    
    
class SimpleLock(object):
    """
    mylock = SimpleLock('mylock')
    @mylock.decorate
    def myfunc():
        do_something()
        
    myfunc() only calls the function if no other thread/process is running it at
    the moment.
    """
    def __init__(self, lockname):
        self.lockname = lockname
        self.filename = os.path.join(LOCKDIR, self.lockname)
        
    @property
    def active(self):
        return os.path.exists(self.filename)
    
    @property
    def age(self):
        if self.active:
            f = open(self.filename, 'r')
            timestamp = f.read()
            f.close()
            return float(timestamp)
        return -1
    
    def aquire(self):
        if not self.active:
            f = open(self.filename, 'w')
            f.write(str(time.time()))
            f.close()
        else:
            raise LockAlreadyActive(self.lockname)
        
    def release(self):
        if self.active:
            os.remove(self.filename)
        else:
            raise LockNotActive(self.lockname)
        
    def decorate(self, function):
        def _wrapped(*args, **kwargs):
            if self.active:
                return
            self.aquire()
            try:
                return function(*args, **kwargs)
            finally:
                self.release()
        _wrapped.__name__ = function.__name__
        return _wrapped