from salt import utils
import re

class Nic(object):
    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt

    def process(self):
        result = utils.shell_exec_command(self.token,self.tgt,'ifconfig')
        response = {}
        for key in self.tgt:
            content = result['return'][0].get(key)
            if not content:
                info = {'status': False, 'message':'salt-minion数据返回错误，可能是salt-key错误或salt-minon无法连接'}
            else:
                info = self.parse(content)
                info['status'] = True
            response[key] = info

        return response

    def parse(self,content):
        nic = {}
        ipterfaces_list =content.split('\n\n')
        for ipterface in ipterfaces_list:
            ipterface_info = ipterface.split(':',1)
            ipterface_name = ipterface_info[0]
            if ipterface_name == 'lo':
                continue
            info_list = ipterface_info[1].split('\n')
            info = [x for x in info_list[1].strip().split(' ') if x]
            nic_info = {
                'ip': info[1],
                'netmask': info[3],
                'broadcast': info[5],
                'mac_addr': info_list[2].strip().split(' ')[1],
            }
            nic[ipterface_name] = nic_info

        return nic

if __name__ == '__main__':
    token = 'a7a8b2b7acca5d2bc7536dc305bec08237d7db74'
    a = Nic(token,['test']).process()
    print(a)