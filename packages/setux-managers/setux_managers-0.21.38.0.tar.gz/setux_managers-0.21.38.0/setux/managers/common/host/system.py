from pybrary.net import get_ip_adr
from pybrary.func import memo

from setux.core.manage import Manager


class Distro(Manager):
    manager = 'system'

    @property
    def hostname(self):
        attr = '_hostname_'
        try:
            val = getattr(self, attr)
        except AttributeError:
            ret, out, err = self.run('hostname')
            val = out[0]
            setattr(self, attr,  val)
        return val

    @hostname.setter
    def hostname(self, val):
        attr = '_hostname_'
        delattr(self, attr)
        ret, out, err = self.run(
            'hostname', val.replace('_', '')
        )
        return ret

    @memo
    def fqdn(self):
        ret, out, err = self.run('hostname -f')
        return out[0]
