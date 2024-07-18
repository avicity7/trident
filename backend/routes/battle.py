from flask import request, Blueprint
from __main__ import app
import services.battle

battle = Blueprint('cad', __name__, url_prefix='/battle') 

@battle.route('/create-battle', methods=["POST"])
def CreateBattle():
  req = request.get_json()

  p1 = req["p1"]
  p2 = req["p2"]
  
  return services.battle.CreateBattle(p1, p2)

@battle.route('/accept-battle', methods=["POST"])
def AcceptBattle():
  req = request.get_json()

  battle_id = req["battle_id"]

  return services.battle.AcceptBattle(battle_id)


