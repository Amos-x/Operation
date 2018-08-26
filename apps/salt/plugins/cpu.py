from salt import utils

class Cpu(object):
    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt

    def process(self):
        result = utils.get_info(self.token, self.tgt, 'grains')
        cpu_physical = utils.shell_exec_command(self.token, self.tgt, "cat /proc/cpuinfo | grep 'physical id' | sort | uniq | wc -l")
        response = {}
        for key in self.tgt:
            grains_items = result['return'][0].get(key)
            cpu_physical_num = cpu_physical['return'][0].get(key)
            if not grains_items and not cpu_physical_num:
                cpu_info = {'status': False, 'message':'salt-minion数据返回错误，可能是salt-key错误或salt-minon无法连接'}
            else:
                cpu_info = {
                    'status': True,
                    'cpu_arch': grains_items.get('cpuarch'),
                    'cpu_model': grains_items.get('cpu_model'),
                    'cpu_flags': grains_items.get('cpu_flags'),
                    'cpu_core_count': grains_items.get('num_cpus'),
                    'cpu_physical_num': cpu_physical_num,
                }
            response[key] = cpu_info

        return response

if __name__ == '__main__':
    token = '0378211d367f6e6abb6957265dbdd9299b2fbfe3'
    a = Cpu(token,['192.168.9.54','192.168.9.55']).process()
    print(a)