import json
from task_manager import Task


class Storage:

	def __init__(self, filename="tasks.json"):
		self.tasks = []
		self.filename = filename
		self.load_tasks_from_file()

	def load_tasks_from_file(self):
		try:
			with open(self.filename, "r") as file:
				data = json.load(file)
				self.tasks = [Task.from_dict(task) for task in data.get('tasks', [])]

		except (FileNotFoundError, json.JSONDecodeError):
			# Handle case when file does not exist or contains invalid JSON
			self.tasks = []

	def save_task_to_file(self):
		with open(self.filename, "w") as file:
			json.dump({"tasks": [task.to_dict() for task in self.tasks]}, file, indent=2)

	def save_task(self, task):
		self.tasks.append(task)
		self.save_task_to_file()

	def update_task(self, updated_task):
		for i, task in enumerate(self.tasks):
			if task.title.lower() == updated_task.title.lower():
				self.tasks[i] = updated_task
				self.save_task_to_file()
				break

	def get_task(self, title):
		for task in self.tasks:
			if task.title.lower() == title.lower() and not task.completed:
				return task
		return None

	def remove_task(self, deleted_task):
		for task in self.tasks:
			if task.title.lower() == deleted_task.title.lower():
				self.tasks.remove(task)
				self.save_task_to_file()
				break

	def get_all_tasks(self):
		return list(self.tasks)

	def clear_all_tasks(self, tasks):
		if tasks:
			tasks.clear()
			self.save_task_to_file()
			return True
		return False
