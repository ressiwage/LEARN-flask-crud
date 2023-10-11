from enum import Enum
import socket
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
class db(Enum):
    password = 'r3Dk7jcPBsSNtoTYxhGX'
    user = 'root'
    host = ip_address
    port = '9999'

