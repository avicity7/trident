import config.db
import services.magician
cur = config.db.conn.cursor()
conn = config.db.conn

import uuid

def CreateBattle(p1, p2):
  values = [str(uuid.uuid4()), p1, p2, False, ""]
  cur.execute("INSERT INTO battle(battle_id, p1, p2, accepted, winner)", values)  
  conn.commit()

  return "OK"

def AcceptBattle(battle_id):
  cur.execute("UPDATE battle SET accepted = true WHERE battle_id = %s", [battle_id])
  conn.commit()

  return "OK"

def EndBattle(battle_id, winner, p1, p2):
  values = [winner, battle_id]
  cur.execute("UPDATE battle SET winner = %s WHERE battle_id = %s", values)
  conn.commit()
  services.magician.ResetMagicians(p1, p2)