from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.functions.load_task_open_ai import load_openai


class LoadTaskOpenAiUsecase:
    def __init__(self):
        self.repo = None

    def __call__(self, task_message):
        if not task_message:
            raise MissingParameters("task")

        task_response = load_openai(task_message)
        print("TASK AQUI CARALHOOOOO" + task_message)
        return task_response
