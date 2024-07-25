from pymongo import MongoClient

def get_category_collection(conn_str: str):
    try:
        client = MongoClient(conn_str)
        user_db = client["daily-tasks-db"]
        category_collection = user_db.categories
        return category_collection
    except Exception as e:
        print(f'Erro conectando ao MongoDB: {e}')
        raise