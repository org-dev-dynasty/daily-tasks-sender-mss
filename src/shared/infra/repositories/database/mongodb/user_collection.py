from pymongo import MongoClient

def get_users_collection(conn_str: str):
  try:
    client = MongoClient(conn_str)
    daily_tasks_db = client["daily-tasks-db"]
    users_collection = daily_tasks_db.users
    print('MongoDB connection successful')
    return users_collection
  except Exception as e:
    print(f'Erro conectando ao MongoDB: {e}')
    raise
