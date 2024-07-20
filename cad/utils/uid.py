import uuid

def GenerateUUID():
  uid = str(uuid.uuid4())
  return uid

print(GenerateUUID())