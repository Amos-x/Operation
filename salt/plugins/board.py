from salt import utils


class Board(object):
    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt

    def process(self):
        result = utils.shell_exec_command(self.token, self.tgt, 'dmidecode -t2')
        response = {}
        for key in self.tgt:
            content = result['return'][0].get(key)
            if not content:
                info = {'status':False,'message':'salt-minion数据返回错误，可能是salt-key错误或salt-minon无法连接'}
            else:
                info = self.parse(content)
                info['status'] = True
            response[key] = info

        return response


    def parse(self, content):
        result = {}
        key_map = {
            'Manufacturer': 'board_factory',
            'Product Name': 'board_model',
            'Serial Number': 'board_sn',
        }

        for item in content.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]

        return result

if __name__ == '__main__':
    token = 'a7a8b2b7acca5d2bc7536dc305bec08237d7db74'
    a = Board(token,['test']).process()
    print(a)
