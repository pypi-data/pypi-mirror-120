from . import setting

settings = setting.load()

if settings['tcp_port'] != '':
    from .client_tcp import Command
elif settings['udp_port'] != '':
    from .client_udp import Command
else:
    raise ValueError(f'Cybos server setting error: {settings}')
