import config.db
cur = config.db.conn.cursor()
conn = config.db.conn

def LinkDevice(cad_id, uid):
  cur.execute("INSERT INTO cad(cad_id, user_id) VALUES(%s, %s)", [cad_id, uid])
  conn.commit()
  
  return "OK"

def GetLink(cad_id):
  cur.execute("SELECT user_id FROM cad WHERE cad_id = %s", [cad_id])
  r = cur.fetchall()

  return r
