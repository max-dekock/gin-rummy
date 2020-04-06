from . import create_app
from .api import socketio

app = create_app()
socketio.init_app(app)
socketio.run(app, host="0.0.0.0", port="5000", debug=True)