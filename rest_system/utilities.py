import uuid

def get_new_token():
    return str(str(uuid.uuid4()) + str(uuid.uuid4())).replace("-", "")[:64]

def get_new_big_token():
    return str(str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())).replace("-", "")[:128]