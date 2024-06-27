from pymongo import MongoClient

def get_users_collection(conn_str: str):
  try:
    client = MongoClient(conn_str)
    user_db = client["daily-tasks-db"]
    users_collection = user_db.users
    print('MongoDB connection successful')  # Adicionar print para verificar a conexão
    return users_collection
  except Exception as e:
    print(f'Erro conectando ao MongoDB: {e}')
    raise
