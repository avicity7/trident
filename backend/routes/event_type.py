from flask import request, Blueprint
from __main__ import app
import services.event_type

event_type = Blueprint('event_type', __name__, url_prefix='/event_type') 

@event_type.route('/create', methods=["POST"])
def CreateEventType():
  req = request.get_json()

  event_name= req["event_name"]
  hp_effect = req["hp_effect"]
  psion_cost = req["psion_cost"]

  return services.event_type.CreateEventType(event_name, hp_effect, psion_cost)