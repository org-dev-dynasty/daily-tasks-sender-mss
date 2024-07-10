from pymongo import MongoClient

def get_tasks_collection(conn_str: str):
  try:
    client = MongoClient(conn_str)
    daily_tasks_db = client["daily-tasks-db"]
    tasks_collection = daily_tasks_db.tasks
    print('MongoDB connection successful')
    return tasks_collection
  except Exception as e:
    print(f'Erro conectando ao MongoDB: {e}')
    raise
