from flask import Flask, send_from_directory
app = Flask(__name__)

@app.route("/")
def client():
    return send_from_directory('build', 'index.html')
  
@app.route("/<path:path>")
def route(path):
    return send_from_directory('build', f'{path}.html')
  
if __name__ == '__main__':
    app.run()