import config.db
cur = config.db.conn.cursor()

def LinkDevice(cad_id, uid):
  cur.execute("INSERT INTO cad(cad_id, user_id) VALUES(%s, %s)", [cad_id, uid])
  cur.commit()
  
  return "OK"
