from flask import render_template, send_from_directory
from werkzeug.exceptions import NotFound
from pathlib import Path, PurePosixPath
from .converter import RegexConverter
from flask import Flask, request

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


@app.route('/<regex("[^|?]*"):root_path>', methods=['GET'])
def index(root_path):
    path = Path.cwd() / root_path
    if not path.exists() and not path.is_dir():
        raise NotFound()
    files = []
    for file in path.iterdir():
        if file.is_dir():
            files.append({'is_dir': True, 'root_path': f'{PurePosixPath(root_path) / file.name}', 'name': file.name})
        elif file.suffix == '.mp4':
            files.append({'is_dir': False, 'root_path': root_path, 'name': file.name})
    return render_template('index.html', files=files)


@app.route('/play', methods=['GET'])
def play():
    file = request.args.get('file')
    root_path = request.args.get('root_path')
    return render_template('play.html', file=PurePosixPath('media') / root_path / file)


@app.route('/media/<path:file>', methods=['GET'])
def media(file):
    return send_from_directory(Path.cwd(), file)
