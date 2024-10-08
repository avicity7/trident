from __main__ import socketio
import config.db
cur = config.db.conn.cursor()
conn = config.db.conn

import uuid
import bcrypt

def CreateMagician(username, password):
  cur.execute("SELECT * FROM magician WHERE username = %s", [username])
  r = cur.fetchall()

  s = bcrypt.gensalt()
  password = str.encode(password)
  password = bcrypt.hashpw(password, s).decode()

  if len(r) == 0:
    cur.execute("""
      INSERT INTO magician(user_id, username, password, hp)
      VALUES (%s, %s, %s, %s)
    """, (str(uuid.uuid4()), username, password, 100))
    conn.commit()
    return {"response": "OK"}
  else: 
    return {"response": "EXISTING"}

def LoginMagician(username, password):
  cur.execute("SELECT * FROM magician WHERE username = %s", [username])
  r = cur.fetchall()
  if len(r):
    hash = str.encode(r[0][2])
    password = str.encode(password)
    if bcrypt.checkpw(password, hash):
      cur.execute("SELECT c.cad_id FROM magician m JOIN cad c ON c.user_id = m.user_id WHERE username = %s", [username])
      try:
        r = cur.fetchall()[0][0]
        return {"response": r}
      except:
        return {"response": "OK"}
    else:
      return {"response": "WRONG PASSWORD"}
  else:
    return {"response": "WRONG PASSWORD"}

def GetAllMagicians():
  cur.execute("SELECT * FROM magician")
  r = cur.fetchall()
  socketio.emit("1234")
  return r

def GetState(user_id):
  cur.execute("SELECT username, hp, psions FROM magician WHERE user_id = %s", [user_id])
  r = cur.fetchall()
  return r

def UpdateMagicianHealth(uid, value):
  cur.execute("SELECT hp FROM magician WHERE user_id = %s", [uid])
  hp = cur.fetchall()[0][0]
  cur.execute("UPDATE magician SET hp = %s WHERE user_id = %s", (hp + value, uid))
  conn.commit()
  return "OK"

def RegeneratePsions(uid):
  cur.execute("UPDATE magician SET psions = psions + 10 WHERE user_id = %s", [uid])
  conn.commit()
  socketio.emit(uid)
  return "OK"
  

def ResetMagicians(uid_1, uid_2):
  cur.execute("UPDATE magician SET hp = 100, psions = 100 WHERE user_id = %s OR user_id = %s", (uid_1, uid_2))
  conn.commit()
  return "OK"

def GetHistory(username):
  cur.execute("SELECT user_id FROM magician WHERE username = %s", [username])
  r = cur.fetchall()[0]
  uid = r[0]
  cur.execute("SELECT * FROM battle WHERE p1 = %s OR p2 = %s", [uid])
  r = cur.fetchall()
  return r