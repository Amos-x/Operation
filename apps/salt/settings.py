import os

# BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SALT_API_URL = 'https://192.168.9.89:8000'
SALT_USER = 'Amos'
SALT_PASSWD = 'FzMm945'

INSERT_ASSET_API = 'http://localhost:8000/api/asset/'

PLUGINS_DICT = {
    'basic': "salt.plugins.basic.Basic",
    'board': "salt.plugins.board.Board",
    'cpu': "salt.plugins.cpu.Cpu",
    'disk': "salt.plugins.disk.Disk",
    'memory': "salt.plugins.memory.Memory",
    'nic': "salt.plugins.nic.Nic",
}


ACCEPT_DICT = {
    'basic': "salt.accept.basic.Basic",
    'board': "salt.accept.board.Board",
    'cpu': "salt.accept.cpu.Cpu",
    'disk': "salt.accept.disk.Disk",
    'memory': "salt.accept.memory.Memory",
    'nic': "salt.accept.nic.Nic",
}
