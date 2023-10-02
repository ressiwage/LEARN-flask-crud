from .create import create_db_resources
from .config import db
from sqlalchemy import Boolean

creds = {
    # база данных
    'library': {
        "hostname": f'{db.host.value}:{db.port.value}',
        "username": db.user.value,
        "password": db.password.value,
        "dbname": "library"
    },
    
    
}
engines, tables, inspectors = create_db_resources(creds)