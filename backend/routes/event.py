from flask import request, Blueprint
from __main__ import app
import services.event

event = Blueprint('event', __name__, url_prefix='/event') 

@event.route('/create-event', methods=["POST"])
def CreateEvent():
  req = request.get_json()

  battle_id = req["battle_id"]
  event_id = req["event_id"]
  emitter = req["emitter"]

  return services.event.CreateEvent(battle_id, event_id, emitter)
