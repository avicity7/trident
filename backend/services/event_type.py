import config.db
from random import randint
cur = config.db.conn.cursor()
conn = config.db.conn

def CreateEventType(event_name, hp_effect, psion_cost):
  r = cur.execute("SELECT event_id FROM cad_event_type")
  ids = r.fetchmany()
  
  event_id = randint(100000, 999999)
  while event_id in ids:  
    event_id = randint(100000, 999999)

  cur.execute("INSERT INTO cad_event_type(event_id, event_name, hp_effect, psion_cost) VALUES (%s, %s, %s, %s)", [event_id, event_name, hp_effect, psion_cost])
  conn.commit()
  
  return "OK"
  
  

