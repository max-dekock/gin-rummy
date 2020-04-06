from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room

import os
import traceback

def create_app(test_config=None):
    app = Flask(__name__.split(".")[0], instance_relative_config=True)
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
    
    # Create the instance folder if necessary
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app