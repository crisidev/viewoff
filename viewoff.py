import os
from flask import Flask
from flask.ext.autoindex import AutoIndex
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
import pty
import psutil
import signal
from datetime import datetime

SHOWOFF_SITE_DIR = '/home/bigo/sites/showoff.crisidev.org'
SHOWOFF_DIR = '.showoff'

class ShowOff(Thread):
    def __init__(self, command, dirname):
        Thread.__init__(self)
        self.command = ['showoff ' + command]
        self.dirname = dirname
        self.showoff_path = os.path.join(SHOWOFF_SITE_DIR, dirname, SHOWOFF_DIR)
        self.logfilename = datetime.now().strftime(dirname + '_%H_%M_%d_%m_%Y.log')
        self.logfile = open(os.path.join(self.showoff_path, self.logfilename), 'a')
        self.thread = None

    def run(self):
        if os.path.isdir(self.showoff_path):
            self.thread = Popen(self.command, stdout=self.logfile, stderr=self.logfile, shell=True)
        else:
            return IOError('directory `%s` not found.' % self.dirname)

    def kill(self):
        if self.thread:
            proc = psutil.Process(self.thread.pid)
            child_pid = proc.get_children(recursive=True)
            for pid in child_pid:
                os.kill(pid.pid, signal.SIGTERM)
            self.logfile.close()
            os.kill(self.thread.pid, signal.SIGTERM)
        else:
            return ValueError('thread `ShowOff` not found.')

app = Flask(__name__)
app.debug = True
AutoIndex(app, browse_root=SHOWOFF_SITE_DIR)
showoff_thread = None

@app.route('/startshowoff/<path:dirname>')
def startshowoff(dirname):
    global showoff_thread
    showoff_thread = ShowOff('serve', dirname)
    os.chdir(showoff_thread.showoff_path)
    showoff_thread.daemon = True
    showoff_thread.start()
    return "OK"

@app.route('/stopshowoff')
def stopshowoff():
    global showoff_thread
    showoff_thread.kill()
    return "OK"

if __name__ == '__main__':
    app.run()
