from pymongo import MongoClient
import os
import uuid

def get_prompt_collection(conn_str: str):
    try:
        client = MongoClient(conn_str)
        user_db = client["daily-tasks-db"]
        category_collection = user_db.prompts
        return category_collection
    except Exception as e:
        print(f'Erro conectando ao MongoDB: {e}')
        raise

def insert_prompt():
  try:  
    prompt_col = get_prompt_collection(os.environ.get("MONGODB_URL"))

    prompt_desc = """
    Você receberá uma tarefa do dia a dia. Quero que você atue como um assistente pessoal. Sua tarefa é registrar eventos e me lembrar deles com base nas informações fornecidas. Para cada evento, por favor, extraia e armazene os seguintes pontos chave:

    Nome do evento: Crie um nome descritivo e conciso para o evento com base nas palavras-chave fornecidas.
    Data: A data do evento.
    Hora: O horário do evento.
    Descrição: Uma breve descrição do evento, com até 60 palavras.
    Local: O local do evento, se estiver especificado.
    Certifique-se de capturar todas as informações relevantes e formatá-las de maneira clara e organizada.

    Exemplo de entrada de evento:
    "Lembre-me de um evento importante que ocorrerá na próxima semana. Vou no médico doutor Luis Carlos, na quarta-feira, às 14h. Vou fazer um check-up geral. Depois vou ver um filme para descansar."

    Exemplo de saída esperada:
    {
      "task_name": "Check-up com Dr. Luis Carlos",
      "task_date": "Data a definir",
      "task_hour": "14:00",
      "task_description": "Consulta médica com o Dr. Luis Carlos para um check-up geral",
      "task_local": "Clínica do Dr. Luis Carlos"
    }, lembre se que no final antes de enviar a resposta, você deve formatar a resposta em um JSON de um linha
    de maneira que fique fácil de usar o metodo json.loads() do Python para transformar a resposta em um dicionário Python.

    Caso o usuário não informe alguma informação explicitamente, você deve marcar está informação não informada como null. Use o seguinte formato JSON para a resposta em caso ele não informar nada:
    {
      "task_name": null,
      "task_date": null,
      "task_hour": null,
      "task_description": null,
      "task_local": null
    }, mas apenas mostre null caso o usuário não informe a informação, mas para o caso do nome do evento, você deve informar um nome padrão, como "Evento sem nome".
    Lembre se que no final antes de enviar a resposta, você deve formatar a resposta em um JSON de um linha
    de maneira que fique fácil de usar o metodo json.loads() do Python para transformar a resposta em um dicionário Python.
    """

    prompt = {
        "_id": str(uuid.uuid4()),
        "prompt_name": "Prompt de filtragem DailyTasks",
        "prompt_description": prompt_desc,
        "prompt_status": "active"
    }

    prompt_col.insert_one(prompt)
  
  except Exception as e:
    print(f'Erro inserindo prompt no MongoDB: {e}')
    raise e
  
def get_prompt():
  try:
    prompt_col = get_prompt_collection(os.environ.get("MONGODB_URL"))
    prompt = prompt_col.find_one({"prompt_name": "Prompt de filtragem DailyTasks"})
    return prompt.get("prompt_description")
  except Exception as e:
    print(f'Erro recuperando prompt no MongoDB: {e}')
    raise e
