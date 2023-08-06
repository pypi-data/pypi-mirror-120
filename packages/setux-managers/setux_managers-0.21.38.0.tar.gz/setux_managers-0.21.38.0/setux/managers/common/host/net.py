from pybrary.net import get_ip_adr
from pybrary.func import memo

from setux.core.manage import Manager


class Distro(Manager):
    manager = 'net'

    @memo
    def addr(self):
        ok, adr = get_ip_adr()
        if ok:
            return adr
        else:
            debug(adr)
            return '!'

