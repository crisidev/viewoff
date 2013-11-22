import os
from flask import Flask, render_template, url_for, send_from_directory, redirect
from showoff import ShowOff

SHOWOFF_SITE_DIR = '/home/bigo/sites/showoff.crisidev.org'
SHOWOFF_DIR = '.showoff'

app = Flask(__name__)
app.debug = True
showoff_thread = None


"""
    Flask routes
"""
@app.route('/')
def root():
    showoff_directories = get_showoff_directories()
    html = render_template('header.html', showoff_directories=showoff_directories)
    html += render_template('footer.html')
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
    directory_list = [dirname for dirname in os.listdir(SHOWOFF_SITE_DIR)
            if os.path.isdir(os.path.join(SHOWOFF_SITE_DIR, dirname))
                and os.path.isdir(os.path.join(SHOWOFF_SITE_DIR, dirname, SHOWOFF_DIR))]
    return directory_list 

if __name__ == '__main__':
    app.run()
