"""
"""
import os
import signal
import psutil
from threading import Thread
from datetime import datetime
from subprocess import Popen

class ShowOff(Thread):
    """
    """
    def __init__(self, command, dirname, showoff_site_dir, showoff_dir):
        """
        """
        Thread.__init__(self)
        self.command = ['showoff ' + command]
        self.dirname = dirname
        self.showoff_path = os.path.join(showoff_site_dir, dirname, showoff_dir)
        self.logfilename = datetime.now().strftime(dirname + '_%H_%M_%d_%m_%Y.log')
        self.logfile = open(os.path.join(self.showoff_path, self.logfilename), 'a')
        self.thread = None

    def run(self):
        """
        """
        if os.path.isdir(self.showoff_path):
            self.thread = Popen(self.command, stdout=self.logfile, stderr=self.logfile, shell=True)
        else:
            return IOError('directory `%s` not found.' % self.dirname)

    def kill(self):
        """
        """
        if self.thread:
            proc = psutil.Process(self.thread.pid)
            child_pid = proc.get_children(recursive=True)
            for pid in child_pid:
                os.kill(pid.pid, signal.SIGTERM)
            self.logfile.close()
            os.kill(self.thread.pid, signal.SIGTERM)
        else:
            return ValueError('thread `ShowOff` not found.')
