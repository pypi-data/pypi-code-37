from flask import Flask
from flask import jsonify
from functools import partial
from http import server
import socketserver
from pathlib import Path
import click

app = Flask(__name__)
_directory = None


@click.group()
def main():
    pass


@main.command()
def init():
    import setuptools
    print(setuptools.find_packages())
    print("Do some initialization")


@main.command()
@click.option("--port", default=5000, type=int)
@click.option("--directory", default=None)
def start(port, directory):
    if directory is None:
        directory = str(Path.cwd())
    handler = partial(server.SimpleHTTPRequestHandler, directory=directory)
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port: {port}\nWith directory path: {str(directory)}")
        httpd.serve_forever()


@main.command()
@click.option("--port", default=5000, type=int)
@click.option("--directory", default=str(Path.cwd()))
def start(port, directory):
    global _directory
    _directory = directory
    print(_directory)
    app.run(debug=True, host='0.0.0.0', port=port)


@app.route("/files")
def files():
    global _directory
    return jsonify({
        "paths": [str(p) for p in Path(_directory).glob("**/*")]
    })


if __name__ == "__main__":
    main()
