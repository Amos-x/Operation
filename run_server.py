# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019/2/22 8:24 PM
#   FileName = run_server

import sys
import subprocess


if __name__ == '__main__':
    subprocess.call('python3 operation.py start all', shell=True,
                    stdin=sys.stdin, stdout=sys.stdout)
