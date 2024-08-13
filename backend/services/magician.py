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

def ResetMagicians(uid_1, uid_2):
  cur.execute("UPDATE magician SET hp = 100, psions = 100 WHERE user_id = %s OR user_id = %s", (uid_1, uid_2))
  conn.commit()
  return "OK"