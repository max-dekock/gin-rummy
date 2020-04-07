from flask import Flask, redirect
from flask_socketio import SocketIO, send, emit, join_room

from whitenoise import WhiteNoise

import os
import traceback

def create_app(test_config=None):
    app = Flask(__name__.split(".")[0], static_folder='dist/')
    app.config.from_mapping(
        SECRET_KEY="dev",
        REDIS_DB=("127.0.0.1", 6379, 0) # (host, port, db)
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Configure whitenoise to serve static files
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='dist/')

    @app.route('/')
    def serve_app():
        return redirect('/index.html')

    return app