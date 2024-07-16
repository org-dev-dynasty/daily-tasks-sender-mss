from pymongo import MongoClient

def get_tasks_collection(conn_str: str):
    try:
        client = MongoClient(conn_str)
        user_db = client["daily-tasks-db"]
        tasks_collection = user_db.tasks
        return tasks_collection
    except Exception as e:
        print(f'Erro conectando ao MongoDB: {e}')
        raise
