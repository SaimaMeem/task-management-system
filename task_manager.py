from datetime import datetime


class Task:

	def __init__(self, title, description, completed=False, created_at=None):
		self.title = title
		self.description = description
		self.completed = completed
		self.created_at = created_at or datetime.now().isoformat()

class TaskManager:

	def __init__(self, storage):
		self.storage = storage

	def add_task(self, title, description):
		task = Task(title, description)
		self.storage.save_task(task)
		return task

	def complete_task(self, title):
		task = self.storage.get_task(title)
		if task:
			task.completed = True
			self.storage.update_task(task)
			return True
		return False

	def list_tasks(self, include_completed=False):
		tasks = self.storage.get_all_tasks()
		if not include_completed:
			tasks = [task for task in tasks if not task.completed]
		return tasks

	def generate_report(self):
		tasks = self.storage.get_all_tasks()
		total_tasks = len(tasks)
		completed_tasks = len([task for task in tasks if task.completed])

		report = {
		    "total": total_tasks,
		    "completed": completed_tasks,
		    "pending": total_tasks - completed_tasks
		}

		return report

