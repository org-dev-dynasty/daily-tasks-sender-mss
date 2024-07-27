from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.functions.load_task_open_ai import load_openai
from src.shared.infra.repositories.database.mongodb.prompt_collection import get_prompt, insert_prompt
import json
import logging

class LoadTaskOpenAiUsecase:
    def __init__(self):
        self.repo = None

    def __call__(self, task_message):
        if not task_message:
            raise MissingParameters("task")            
        
        
        resp = load_openai(task_message)
        
        print(f"Response from OpenAI: {resp}")
        print(f"Type Response from OpenAI: {type(resp)}")
        task = json.loads(resp)
        
        # insert_prompt()
        
        return task