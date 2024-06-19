from flask.app import Flask

app = Flask(__name__)

import routes.magician

app.register_blueprint(routes.magician.magician)

if __name__ == '__main__':
  app.run(debug=True, use_reloader=True)