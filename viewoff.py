import os
from flask import Flask, render_template, url_for
#from flask.ext.autoindex import AutoIndex
from showoff import ShowOff

SHOWOFF_SITE_DIR = '/home/bigo/sites/showoff.crisidev.org'
SHOWOFF_DIR = '.showoff'

app = Flask(__name__)
app.debug = True
#AutoIndex(app, browse_root=SHOWOFF_SITE_DIR)
showoff_thread = None

@app.route('/')
def root():
    css_url = url_for('static', filename='style.css')
    render_template('header.html', css_url=css_url)
    render_template('footer.html')

@app.route('/startshowoff/<path:dirname>')
def startshowoff(dirname):
    global showoff_thread
    showoff_thread = ShowOff('serve', dirname, SHOWOFF_SITE_DIR, SHOWOFF_DIR)
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
