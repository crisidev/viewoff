import os
from flask import Flask, render_template, url_for, send_from_directory, redirect
from showoff import ShowOff

SHOWOFF_SITE_DIR = '/home/bigo/sites/showoff.crisidev.org'
SHOWOFF_DIR = '.showoff'
DEBUG = True
SERVER_NAME = '127.0.0.1'
SERVER_PORT = 5000

app = Flask(__name__)
app.config['DEBUG'] = DEBUG

showoff_thread = None


"""
    Flask routes
"""
@app.route('/')
def root():
    icon_dimension = '24'
    showoff_directories = get_showoff_directories()
    html = render_template('header.html')
    html += render_template('body.html', showoff_directories=showoff_directories,\
            icon_dimension='x'.join([icon_dimension, icon_dimension]))
    html += render_template('footer.html', showoff_directories=showoff_directories)
    return html

@app.route('/startshowoff/<path:dirname>')
def startshowoff(dirname):
    global showoff_thread
    showoff_thread = ShowOff('serve', dirname, SHOWOFF_SITE_DIR, SHOWOFF_DIR)
    os.chdir(showoff_thread.showoff_path)
    showoff_thread.daemon = True
    showoff_thread.start()
    return redirect("https://live.crisidev.org")

@app.route('/stopshowoff')
def stopshowoff():
    global showoff_thread
    showoff_thread.kill()
    return "OK"

@app.route('/<path:dirname>')
def viewshowoff(dirname):
    return send_from_directory(SHOWOFF_SITE_DIR, dirname)


"""
    Functions
"""
def get_showoff_directories():
   return [{'dirname': dirname, 'dirname_fancy': ' '.join(dirname.split('_')).title()}\
            for dirname in os.listdir(SHOWOFF_SITE_DIR)\
            if os.path.isdir(os.path.join(SHOWOFF_SITE_DIR, dirname))\
            and os.path.isdir(os.path.join(SHOWOFF_SITE_DIR, dirname, SHOWOFF_DIR))]

if __name__ == '__main__':
    app.run(SERVER_NAME, SERVER_PORT)
