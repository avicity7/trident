from flask import request, Blueprint
from __main__ import app
import services.cad

cad = Blueprint('cad', __name__, url_prefix='/cad') 

@cad.route('/link-device', methods=["POST"])
def LinkDevice():
  req = request.get_json()
  
  cad_id = req["cad_id"] 
  uid = req["uid"]
  
  return services.cad.LinkDevice(cad_id, uid)
