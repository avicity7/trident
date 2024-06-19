from flask import request, Blueprint
from __main__ import app
import services.magician

magician = Blueprint('magician', __name__, url_prefix='/magician') 

@magician.route('/create-magician', methods=["POST"])
def CreateMagician():
  req = request.get_json()

  username = req['username']
  password = req['password']

  return services.magician.CreateMagician(username, password)

@magician.route('/get-all-magicians', methods=["GET"])
def GetAllMagicians():
  return services.magician.GetAllMagicians()

@magician.route('/update-magician-health', methods=["PUT"])
def UpdateMagicianHealth():
  req = request.get_json()
  
  uid = req['uid']
  value = req['value']
  
  return services.magician.CreateMagician(uid, value)

@magician.route('/reset-magicians', methods=["POST"])
def ResetMagicians():
  req = request.get_json()

  uid_1 = req['uid_1']
  uid_2 = req['uid_2']
  
  return services.magician.CreateMagician(uid_1, uid_2)