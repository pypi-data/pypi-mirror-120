from . import setting

s = setting.load()

if s.active_port == 'TCP':
    from .client_tcp import Command
elif s.active_port == 'UDP':
    from .client_udp import Command
else:
    raise ValueError(f'Cybos server setting error: {s}')
