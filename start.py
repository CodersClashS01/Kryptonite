import io
import os
import subprocess
from pathlib import Path
from threading import Thread

base = Path(__file__).parent.resolve()
website_path = base / 'website'
my_env = os.environ.copy()
my_env['PYTHONPATH'] = ':'.join([str(base)] + [path for path in my_env.get('PYTHONPATH', '').split(':') if path])


def run_website():
    proc = subprocess.Popen(["flask", "run"], cwd=str(website_path), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env=my_env)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        if line.strip():
            print("website:", line.strip('\n'))


def run_bot():
    proc = subprocess.Popen(["python", "main.py"], cwd=str(base), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env=my_env)
    for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
        if line.strip():
            print("bot    :", line.strip('\n'))


if __name__ == '__main__':
    website_thread = Thread(target=run_website)
    bot_thread = Thread(target=run_bot)
    website_thread.start()
    bot_thread.start()
    website_thread.join()
    bot_thread.join()
