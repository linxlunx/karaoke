from flask import Flask, render_template, redirect, request
import json
import hashlib
from time import time
import subprocess
import json
from config import SPLEETER_PATH, YOUTUBE_DL_PATH

app = Flask(__name__, static_folder='static')

def exec_cmd(cmd):
    msg = subprocess.Popen(
        cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    return msg.stdout.read()


@app.route('/', methods=['GET', 'POST'])
def main_index():
    music_path = 'static/music'
    extracted_path = 'static/extracted'
    if request.method == 'GET':
        # clean the data, so we don't save the file
        exec_cmd('rm -rf {}/*'.format(music_path))
        exec_cmd('rm -rf {}/*'.format(extracted_path))
        
        return render_template('index.html')
    if request.method == 'POST':
        url = request.form.get('url')
        if url is None:
            return redirect('/')

        filename = str(time()) + hashlib.md5(url.encode('utf-8')).hexdigest()
        full_file = '{}/{}.mp3'.format(music_path, filename)

        # download file
        cmd_download = '{} --extract-audio --audio-format mp3 \
        --print-json --no-warnings "{}" -o {}'.format(
            YOUTUBE_DL_PATH,
            url, 
            full_file
        )
        res = exec_cmd(cmd_download)
        title = json.loads(res.decode('utf-8'))['title']

        # extract
        extracted_file = '{}/{}'.format(extracted_path, filename)
        cmd_extract = '{} separate -p spleeter:2stems -o {} {}'.format(
            SPLEETER_PATH,
            extracted_file,
            full_file
        )
        exec_cmd(cmd_extract)
        extracted = '/{}/{}/accompaniment.wav'.format(extracted_file, filename)
        
        return render_template('posted.html', extracted=extracted, title=title)        

if __name__ == '__main__':
    app.debug = True
    app.run()
