from models.task import Task

class TaskService:
    def __init__(self):
        self.tasks_by_user = {}

    def add_task(self, username, title, description):
        task = Task(title, description)
        if username not in self.tasks_by_user:
            self.tasks_by_user[username] = []
        self.tasks_by_user[username].append(task)

    def get_tasks(self, username):
        return self.tasks_by_user.get(username, [])
