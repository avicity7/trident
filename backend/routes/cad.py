from flask import request, Blueprint
from __main__ import app
import services.cad

cad = Blueprint('cad', __name__, url_prefix='/cad') 

@cad.route('/link-device', methods=["POST"])
def LinkDevice():
  req = request.get_json()
  
  cad_id = req["cad_id"] 
  username = req["username"]
  
  return services.cad.LinkDevice(cad_id, username)

@cad.route('get-link', methods=["GET"])
def GetLink():
  cad_id = request.args.get("cad_id")

  return services.cad.GetLink(cad_id)
