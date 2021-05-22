import sys
if sys.version_info < (3, 7):
    raise ImportError('Your Python version {0} is not supported by aiogram, please install '
                      'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))


from .call import Wallet, P2P, Terminals


__all__ = ('Wallet', 'P2P', 'Terminals')

__version__ = '1.0.2'
