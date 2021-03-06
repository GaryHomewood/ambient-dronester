from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
from livereload import Server

import os
import platform
import subprocess
import signal
import config

app = Flask(__name__)
app.secret_key = config.app_secret_key

@app.route("/")
def index():
    session.pop('pid', None)
    return render_template("index.html")

@app.route("/volume", methods=["POST"])
def volume():
    content = request.get_json()
    setVolume(str(content['volume']))
    return 'ok'

@app.route("/play", methods=["POST"])
def play():
    content = request.get_json()
    if 'pid' in session:
        # stop the drone if there is one
        os.killpg(os.getpgid(int(session['pid'])), signal.SIGTERM)
        session.pop('pid', None)
        return 'ok'
    setVolume(str(content['volume']))
    center = str(content['center'])
    wave = str(content['wave'])
    playNoiseCmd = './noise.sh 59 ' + center + ' ' + wave + ' brown'
    proc = subprocess.Popen(playNoiseCmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, preexec_fn = os.setsid)
    # save the drone id so it can be turned off
    pid = os.getpgid(proc.pid)
    session['pid'] = str(pid)
    return 'ok'

@app.route("/present")
def present():
    return render_template("present.html")

def setVolume(volume):
    setVolumeCmd = ''
    if platform.system() == 'Darwin':
        setVolumeCmd = 'osascript -e \'set volume output volume ' + volume + '\''
    if platform.system() == 'Linux':
        setVolumeCmd = 'amixer set \'Power Amplifier\' ' + volume + '%'
    if setVolumeCmd:
        subprocess.Popen(setVolumeCmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, preexec_fn = os.setsid)
    return
