from django.conf import settings
import hashlib

def get_hash(password, user_id, register_date):
    hash_object = hashlib.sha512(str(str(register_date) + str(settings.SECRET_KEY) + str(password) + str(user_id)).encode("utf-8"))
    return hash_object.hexdigest()