import os
from pathlib import Path
from flask import Flask, render_template_string, request, redirect, url_for
import subprocess

app = Flask(__name__)

FILES_DIR = "/media/nikolask/2T_BackUp/Archived/Phd_Docs/"  # Change to your directory

@app.route("/")
def index():
    files = []
    for root, dirs, filenames in os.walk(FILES_DIR):
        for fname in filenames:
            fullpath = os.path.join(root, fname)
            mtime = os.path.getmtime(fullpath)
            files.append((mtime, fullpath))
    files.sort(reverse=True)
    html = '''
        <html><body><h1>Files</h1><ul>
        {% for _, f in files %}
          <li>
            <a href="{{ url_for('open_file', fpath=f) }}">{{ f }}</a>
          </li>
        {% endfor %}
        </ul></body></html>
    '''
    return render_template_string(html, files=files)

@app.route("/open")
def open_file():
    fpath = request.args.get('fpath')
    if fpath and os.path.exists(fpath):
        if os.uname().sysname == 'Darwin':
            subprocess.Popen(['open', fpath])
        else:
            subprocess.Popen(['xdg-open', fpath])
        return f"<p>Opened: {fpath}</p><p><a href='/'>Back</a></p>"
    return "<p>File not found!</p><p><a href='/'>Back</a></p>"

if __name__ == '__main__':
    app.run(port=5000, debug=False)
