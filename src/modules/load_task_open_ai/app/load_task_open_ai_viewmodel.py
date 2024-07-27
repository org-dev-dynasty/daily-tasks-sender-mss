class LoadTaskOpenAiViewodel:
    task_name: str
    task_date: str
    task_description: str
    task_local: str

    def __init__(self, task: dict) -> None:
        self.task_name = task.get('task_name')
        self.task_date = task.get('task_date')
        self.task_description = task.get('task_description')
        self.task_local = task.get('task_local')

    def to_dict(self):
        return {
            "task_name": self.task_name,
            "task_date": self.task_date,
            "task_description": self.task_description,
            "task_local": self.task_local,
            "message": "Your was successfully processed by OpenAI"
        }
