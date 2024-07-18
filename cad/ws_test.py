import socketio
import requests
import os
from dotenv import load_dotenv
import utils
sio = socketio.Client()

load_dotenv() 

backend_uri = os.environ["BACKEND_URI"]
id = os.environ["CAD_ID"]

while True:
  with socketio.SimpleClient() as sio:
    sio.connect(backend_uri)
    message = sio.receive()
    if (message[0] == id):
     r = requests.get(f'{backend_uri}/magician/get-all-magicians') 
     if (r.status_code == 200):
      print(r.json())