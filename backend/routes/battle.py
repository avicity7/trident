from flask import request, Blueprint
from __main__ import app
import services.battle

battle = Blueprint('cad', __name__, url_prefix='/battle') 

@battle.route('/create-battle', methods=["POST"])
def CreateBattle():
  req = request.get_json()

  p2 = req["p2"]
  
  return services.battle.CreateBattle(p2)

@battle.route('/accept-battle', methods=["POST"])
def AcceptBattle():
  req = request.get_json()

  confirmation = req["confirmation"]
  uid = req["uid"]

  return services.battle.AcceptBattle(confirmation, uid)

@battle.route('/get-current-battle', methods=["GET"])
def GetCurrentBattle():
  uid = request.args.get("uid")

  return services.battle.GetCurrentBattle(uid)
