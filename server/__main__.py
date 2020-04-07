from . import create_app
from .api import socketio
import os

PORT = os.environ.get('PORT', 5000)

app = create_app()
socketio.init_app(app)
socketio.run(app, host="0.0.0.0", port=PORT, debug=True)