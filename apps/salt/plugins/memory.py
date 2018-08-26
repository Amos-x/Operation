from salt import utils


class Memory(object):
    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt

    def process(self):
        result = utils.shell_exec_command(self.token, self.tgt, 'dmidecode  -q -t 17 2>/dev/null')
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
        ram_dict = {}
        key_map = {
            'Size': 'capacity',
            'Locator': 'slot',
            'Type': 'model',
            'Speed': 'speed',
            'Manufacturer': 'manufacturer',
            'Serial Number': 'sn',
        }
        devices = content.split('Memory Device')
        for item in devices:
            item = item.strip()
            if not item:
                continue
            if item.startswith('#'):
                continue
            segment = {}
            lines = item.split('\n\t')
            for line in lines:
                if not line.strip():
                    continue
                if len(line.split(':')):
                    key, value = line.split(':')
                else:
                    key = line.split(':')[0]
                    value = ""
                if key in key_map:
                    segment[key_map[key.strip()]] = value.strip()
            if segment['capacity'] != 'No Module Installed':
                segment['capacity'] = segment['capacity'][:-3]
                segment['slot'] = segment['slot'][10:]
                ram_dict[segment['slot']] = segment

        return ram_dict

if __name__ == '__main__':
    token = 'a7a8b2b7acca5d2bc7536dc305bec08237d7db74'
    a = Memory(token,['files-server']).process()
    print(a)