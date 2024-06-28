from flask.app import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import routes.magician

app.register_blueprint(routes.magician.magician)

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)