from flask.app import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

import routes.magician
import routes.battle
import routes.cad
import routes.event
import routes.event_type

app.register_blueprint(routes.magician.magician)
app.register_blueprint(routes.battle.battle)
app.register_blueprint(routes.cad.cad, name="casting_device")
app.register_blueprint(routes.event.event)
app.register_blueprint(routes.event_type.event_type)


if __name__ == '__main__':
  socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=True)