#!/usr/bin/python3

from dotenv  import load_dotenv


from models.engine import db_storage as ds
from models.manager import user_manager as usm

storage = ds.DBStorage()

user_manager = usm.UserManager()
user_manager.reload()