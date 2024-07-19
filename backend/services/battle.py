from __main__ import socketio
import config.db
import random
import services.magician
cur = config.db.conn.cursor()
conn = config.db.conn

import uuid

def CreateBattle(p2):
  battle_id = str(uuid.uuid4())
  confirmation = random.randint(100000, 999999)
  values = [battle_id, "00000000-0000-0000-0000-000000000000", p2, False, "00000000-0000-0000-0000-000000000000", confirmation]
  cur.execute("INSERT INTO battle(battle_id, p1, p2, accepted, winner, confirmation) VALUES (%s, %s, %s, %s, %s, %s)", values)  
  conn.commit()

  return [battle_id, confirmation]

def GetCurrentBattle(uid):
  cur.execute("SELECT * FROM battle WHERE winner = '00000000-0000-0000-0000-000000000000' AND (p1 = %s OR p2 = %s)", [uid, uid])
  r = cur.fetchall() 

  return r

def AcceptBattle(confirmation, uid):
  try: 
    cur.execute("SELECT p1, p2 FROM battle WHERE confirmation = %s", [confirmation])
    r = cur.fetchall()
    p1 = r[0][0]
    p2 = r[0][1]
    cur.execute("UPDATE battle SET p1 = %s, accepted = true, confirmation = 0 WHERE confirmation = %s", [uid, confirmation])
    conn.commit()

    socketio.emit(p1)
    socketio.emit(p2)

    return ["OK"]
  except:
    return ["ERROR"]

def EndBattle(battle_id, winner, p1, p2):
  values = [winner, battle_id]
  cur.execute("UPDATE battle SET winner = %s WHERE battle_id = %s", values)
  conn.commit()
  services.magician.ResetMagicians(p1, p2)