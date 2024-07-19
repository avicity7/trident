from flask import request, Blueprint
from __main__ import app
import services.event

event = Blueprint('event', __name__, url_prefix='/event') 

@event.route("/get-event-type", methods=["GET"])
def GetEventType():
  event_id = request.args.get("event_id")

  return services.event.GetEventType(event_id)

@event.route('/create-event', methods=["POST"])
def CreateEvent():
  req = request.get_json()

  battle_id = req["battle_id"]
  event_id = req["event_id"]
  emitter = req["emitter"]

  return services.event.CreateEvent(battle_id, event_id, emitter)

@event.route('/process-event', methods=["POST"])
def CreateEvent():
  req = request.get_json()

  battle_id = req["battle_id"]
  uid = req["uid"]

  return services.event.ProcessEvent(battle_id, uid)
