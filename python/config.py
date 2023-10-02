from enum import Enum
class db(Enum):
    password = 'r3Dk7jcPBsSNtoTYxhGX'
    user = 'root'
    host = '185.244.173.78'
    port = '9999'

print(db.password.value)