import config.db
import services.battle
cur = config.db.conn.cursor()

def LinkDevice(cad_id, user_id):
  cur.execute("INSERT INTO cad(cad_id, user_id) VALUES(%s, %s)", [cad_id, user_id])
  cur.commit()
  
  return "OK"

def CreateEvent(battle_id, event_id, emitter):
  cur.execute("SELECT hp_effect, psion_cost FROM cad_event_type WHERE event_id = %s", [event_id])
  r = cur.fetchone()
  hp_effect = r[0]
  psion_cost = r[1]

  cur.execute("INSERT INTO cad_event(battle_id, event_id, emitter) VALUES (%s, %s, %s)", [battle_id, event_id, emitter])

  cur.execute("SELECT psions FROM magician WHERE user_id = %s", [emitter])
  r = cur.fetchone()
  psion_count = r[0]
  new_psions = psion_count - psion_cost
  cur.execute("UPDATE magician SET psions = %s WHERE user_id = %s", [new_psions, emitter])

  cur.execute("SELECT p1, p2 FROM battle_id WHERE battle_id = %s", [battle_id])
  r = cur.fetchone()
  p1 = r[0]
  p2 = r[1]
  receiver = ""
  if (p1 == receiver):
    receiver = p2
  else:
    receiver = p1

  cur.execute("SELECT hp FROM magician WHERE user_id = %s", [receiver])
  r = cur.fetchone()
  receiver_hp = r[0]
  new_receiver_hp = receiver_hp + hp_effect
  if (new_receiver_hp <= 0):
   services.battle.EndBattle(battle_id, emitter, p1, p2) 
  else:
    cur.execute("UPDATE magician SET hp = %s WHERE user_id = %s", [new_receiver_hp, receiver])
  
  cur.commit()
  return "OK"
