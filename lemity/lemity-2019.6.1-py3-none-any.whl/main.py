from toolset import get_localhost
from .app import app
import sys


def main():
    port = sys.argv[2] if len(sys.argv) > 2 else 8000
    app.run(host=get_localhost(), port=port, debug=False, threaded=True)
