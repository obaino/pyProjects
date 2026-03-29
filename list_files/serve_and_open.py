import os
from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

FILES_DIR = "/media/nikolask/2T_BackUp/Archived/Phd_Docs/"  # Change this to your directory

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").lower()
    files = []
    errors = []

    for root, dirs, filenames in os.walk(FILES_DIR):
        for fname in filenames:
            try:
                if query and query not in fname.lower():
                    continue

                fullpath = os.path.join(root, fname)
                mtime = os.path.getmtime(fullpath)
                files.append((mtime, fullpath))

            except OSError as e:
                errors.append((os.path.join(root, fname), str(e)))
                continue

    files.sort(reverse=True)

    html = """
    <h1>Files</h1>
    <form method="get">
      <input type="text" name="q" value="{{ query }}" placeholder="Search...">
      <button type="submit">Search</button>
    </form>

    <p>Found {{ files|length }} files.</p>

    {% if errors %}
      <p>Skipped {{ errors|length }} unreadable files.</p>
    {% endif %}

    <ul>
    {% for mtime, path in files %}
      <li><a href="/open?path={{ path|urlencode }}">{{ path }}</a></li>
    {% endfor %}
    </ul>
    """
    return render_template_string(html, files=files, query=query, errors=errors)


@app.route("/open")
def open_file():
    relpath = request.args.get("path", "")
    fullpath = os.path.abspath(os.path.join(FILES_DIR, relpath))
    basepath = os.path.abspath(FILES_DIR)

    if not fullpath.startswith(basepath + os.sep):
        return "Invalid path!", 400

    if not os.path.exists(fullpath):
        return f"<h3>File not found!</h3><p>{fullpath}</p><p><a href='/'>Back</a></p>"

    subprocess.Popen(["mpv", fullpath])
    return f"<h3>Opened in mpv:</h3><p>{fullpath}</p><p><a href='/'>Back</a></p>"

if __name__ == '__main__':
    app.run(port=5000, debug=False)
