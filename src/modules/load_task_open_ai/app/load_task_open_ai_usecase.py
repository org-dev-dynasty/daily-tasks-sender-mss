from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.functions.load_task_open_ai import load_openai
from src.shared.infra.repositories.database.mongodb.prompt_collection import insert_prompt


class LoadTaskOpenAiUsecase:
    def __init__(self):
        self.repo = None

    def __call__(self, task_message):
        if not task_message:
            raise MissingParameters("task")
        insert_prompt() 
        print("TASK AQUI CARALHOOOOO" + task_message)
        return {"task": task_message }
