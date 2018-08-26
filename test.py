import subprocess
import os,sys

base_dir = os.path.dirname(os.path.abspath(__file__))
a_dir = os.path.join(base_dir,'apps')

print(a_dir)
subprocess.run('python3 manage.py runserver',shell=True,cwd=a_dir,stdout=sys.stdout)
