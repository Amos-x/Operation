#! /usr/local/bin/python3
# __author__: Amos,Chinese
# Email：379833553@qq.com

from apps import __version__
import os
import sys
import subprocess
import threading
import time
import argparse
import platform
import signal


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    from config import config as CONFIG
except ImportError:
    print('Could not find config file, Please check the integrity of the project.')
    sys.exit(1)

OS_TYPE = platform.system()
APPS_DIR = os.path.join(BASE_DIR, 'apps')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
HTTP_HOST = CONFIG.HTTP_BIND_HOST or '127.0.0.1'
HTTP_PORT = CONFIG.HTTP_LISTEN_PORT or 8080

WORKERS = CONFIG.WORKERS or 4
DEBUG = CONFIG.DEBUG or True
all_services = ['gunicorn', 'celery', 'beat']
TIMEOUT = 10
DAEMON = False


def make_migrations():
    print('\nCheck database structure change ...')
    os.chdir(APPS_DIR)
    subprocess.call('python3 manage.py makemigrations', shell=True)
    subprocess.call('python3 manage.py migrate', shell=True)


def collect_static():
    print("Collect static files")
    os.chdir(APPS_DIR)
    subprocess.call('python3 manage.py collectstatic --no-input', shell=True)


def prepare():
    make_migrations()
    collect_static()


def get_pid_file_path(service):
    return os.path.join(TMP_DIR, '{}.pid'.format(service))


def get_log_file_path(service):
    return os.path.join(LOG_DIR, '{}.log'.format(service))


def parse_service(service):
    if service == 'all':
        return all_services
    elif ',' in service:
        return [i.strip() for i in service.split(',')]
    else:
        return [service]


def get_pid(service):
    pid_file = get_pid_file_path(service)
    if os.path.isfile(pid_file):
        with open(pid_file) as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0


def is_running(service):
    pid_file = get_pid_file_path(service)
    if os.path.isfile(pid_file):
        pid = get_pid(service)
        if pid:
            try:
                os.kill(pid, 0)
            except OSError:
                return False
            else:
                return True
        else:
            os.remove(pid_file)
            return False
    else:
        return False


def start_gunicorn():
    print("\n- Start Gunicorn WSGI HTTP Server")
    prepare()
    service = 'gunicorn'
    bind = '{}:{}'.format(HTTP_HOST, HTTP_PORT)
    log_format = '%(h)s %(t)s "%(r)s" %(s)s %(b)s '
    pid_file = get_pid_file_path(service)
    log_file = get_log_file_path(service)

    cmd = [
        'gunicorn', 'Operation.wsgi',
        '-b', bind,
        '-w', str(WORKERS),
        '-k', 'eventlet',
        '--access-logformat', log_format,
        '-p', pid_file,
        '--access-logfile', log_file,
    ]
    if DAEMON:
        cmd.append('--daemon')
    if DEBUG:
        cmd.append('--reload')
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, cwd=APPS_DIR)
    return p


def start_celery():
    print("\n- Start Celery as Distributed Task Queue")
    # Todo: Must set this environment, otherwise not no ansible result return
    # os.environ.setdefault('PYTHONOPTIMIZE', '1')

    # 解决celery无法使用root启动问题
    if os.getuid() == 0:
        os.environ.setdefault('C_FORCE_ROOT', '1')

    service = 'celery'
    pid_file = get_pid_file_path(service)
    log_file = get_log_file_path(service)
    cmd = [
        'celery', 'worker',
        '-A', 'Operation',
        '-l', CONFIG.LOG_LEVEL.lower(),
        '--pidfile', pid_file,
        '-c', str(WORKERS),
    ]
    if DAEMON:
        cmd.extend([
            '--logfile', log_file,
            '--detach',
        ])
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, cwd=APPS_DIR)
    return p


def start_beat():
    print("\n- Start Beat as Periodic Task Scheduler")

    service = 'beat'
    pid_file = get_pid_file_path(service)
    log_file = get_log_file_path(service)

    # os.environ.setdefault('PYTHONOPTIMIZE', '1')
    if os.getuid() == 0:
        os.environ.setdefault('C_FORCE_ROOT', '1')

    scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
    cmd = [
        'celery', 'beat',
        '-A', 'Operation',
        '--pidfile', pid_file,
        '-l', CONFIG.LOG_LEVEL.lower(),
        '--scheduler', scheduler,
        '--max-interval', '60',
    ]
    if DAEMON:
        cmd.extend([
            '--logfile', log_file,
            '--detach',
        ])
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, cwd=APPS_DIR)
    return p


def start_service(service):
    print(time.ctime())
    print('\nOperation version {}, by Amos'.format(__version__))

    services_handler = {
        'gunicorn': start_gunicorn,
        'celery': start_celery,
        'beat': start_beat
    }

    services_set = parse_service(service)
    process = []
    for i in services_set:
        if is_running(i):
            show_service_status(i)
            continue
        func = services_handler.get(i)
        p = func()
        process.append(p)

    now = time.time()
    for i in services_set:
        while not is_running(i):
            if int(time.time() - now) < TIMEOUT:
                time.sleep(1)
                continue
            else:
                print("\n - Error: {} start error, timeout".format(i))
                stop_service(service, sig=9)
                return

    stop_event = threading.Event()

    if not DAEMON:
        signal.signal(signal.SIGTERM, lambda x, y: stop_event.set())
        while not stop_event.is_set():
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                stop_event.set()
                break

        print("Stop services")
        for p in process:
            p.terminate()

        for i in services_set:
            stop_service(i)
    else:
        print()
        show_service_status(service)


def stop_service(service,sig=15):
    services_set = parse_service(service)
    for i in services_set:
        print("\nStopping {} service...".format(i))
        pid = get_pid(i)
        if pid:
            os.kill(pid, sig)
        now = time.time()
        while is_running(i):
            if int(time.time() - now) < TIMEOUT:
                time.sleep(1)
                continue
            else:
                print("\n - Error: {} stop error, timeout".format(i))
                return
        print("{} is stopped".format(i))


def show_service_status(service):
    services_set = parse_service(service)
    for i in services_set:
        if is_running(i):
            pid = get_pid(i)
            print("\n{} is running: {}".format(i, pid))
        else:
            print("\n{} is stopped".format(i))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Operation service control tools;

    \r\n Usage:
    \r\n%(prog)s sction service
    
    \r\nExample:
    
    \r\n%(prog)s start all

    """)

    parser.add_argument(
        'action', type=str,
        choices=('start', 'stop', 'status', 'restart'),
        help='Action to run')

    parser.add_argument(
        "service", type=str, default="all", nargs="?",
        choices=['all', 'gunicorn', 'celery', 'beat'],
        help="The service to start"
    )
    parser.add_argument('-d', '--daemon', action='store_true', help='使用使用后台模式运行')
    parser.add_argument('-w', '--worker', type=int, help='指定gunicorn工作进程数')
    args = parser.parse_args()

    if args.daemon:
        DAEMON = True

    if args.worker:
        WORKERS = args.worker

    svc = args.service
    if args.action == 'start':
        start_service(svc)
    elif args.action == 'stop':
        stop_service(svc)
    elif args.action == 'status':
        show_service_status(svc)
    elif args.action == 'restart':
        stop_service(svc)
        time.sleep(5)
        start_service(svc)
    else:
        show_service_status(svc)
