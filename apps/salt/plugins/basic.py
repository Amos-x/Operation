from salt import utils

class Basic(object):
    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt

    def process(self):
        grains_items = utils.get_info(self.token, self.tgt, 'grains')
        response = {}
        for key in self.tgt:
            items = grains_items['return'][0].get(key)
            if not items:
                info = {'status':False, 'message': 'salt-minion数据返回错误，可能是salt-key错误或salt-minon无法连接'}
            else:
                info = {
                    'name': items.get('host'),
                    'sn': items.get('serialnumber'),
                    'os_type': items.get('osfullname'),
                    'os_release': items.get('osrelease'),
                    'kernel_release': items.get('kernelrelease'),
                    'status': 'online',
                    'sub_asset_type': 'Vps',
                }
            response[key] = info

        return response

if __name__ == '__main__':
    token = 'fc78bdd1c8ed37c85be8b69c52debe89802674df'
    a = Basic(token,['192.168.9.54','192.168.9.55']).process()
    print(a)