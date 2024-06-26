from pymongo import MongoClient

def get_users_collection(conn_str: str):
  client = MongoClient(conn_str)
  user_db = client["daily-tasks-db"]
  users_collection = user_db.users
  return users_collection
  
