from salt import utils

class Disk(object):
    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt

    def process(self):
        result = utils.shell_exec_command(self.token, self.tgt, "fdisk -l |sed -n '2p' |awk '{print$3}'")
        response = {}
        for key in self.tgt:
            content = result['return'][0].get(key)
            if not content:
                disk_info = {'status': False, 'message':'salt-minion数据返回错误，可能是salt-key错误或salt-minon无法连接'}
            else:
                disk_info = {
                    'status': True,
                    'iface_type': 'SCSI',
                    'capacity': content
                }
            response[key] = disk_info

        return response

if __name__ == '__main__':
    token = 'a7a8b2b7acca5d2bc7536dc305bec08237d7db74'
    a = Disk(token,['test']).process()
    print(a)