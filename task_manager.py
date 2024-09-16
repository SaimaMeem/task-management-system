from datetime import datetime, timedelta


class Task:

	def __init__(self, title, description, completed=False, created_at=None, completed_at=None):
		self.title = title
		self.description = description
		self.completed = completed
		self.created_at = created_at or datetime.now().isoformat()
		self.completed_at = completed_at

class TaskManager:

	def __init__(self, storage):
		self.storage = storage

	def add_task(self, title, description):
		existing_task = self.storage.get_task(title)

		# Proceed if the task doesn't exist or the existing task is completed
		if not existing_task or existing_task.completed:
			task = Task(title, description)
			self.storage.save_task(task)
			return task

		return None

	def edit_task(self, title, description):
		task = self.storage.get_task(title)
		if task:
			task.description = description
			self.storage.update_task(task)
			return task

		return None


	def complete_task(self, title):
		task = self.storage.get_task(title)
		if task:
			task.completed = True
			task.completed_at = datetime.now().isoformat()
			self.storage.update_task(task)
			return True
		return False

	def delete_task(self, title):
		task = self.storage.get_task(title)
		if task:
			self.storage.remove_task(task)
			return True
		return False

	def list_tasks(self, include_completed=False):
		tasks = self.storage.get_all_tasks()
		if not include_completed:
			tasks = [task for task in tasks if not task.completed]
		return tasks

	def generate_report(self):
		tasks = self.storage.get_all_tasks()
		total_tasks_no = len(tasks)

		# Filter out completed tasks
		completed_tasks = [task for task in tasks if task.completed]
		completed_tasks_no = len(completed_tasks)

		# Calculate total and average time for completed tasks
		if completed_tasks_no > 0:
			total_completion_time = sum(
				(datetime.fromisoformat(task.completed_at) - datetime.fromisoformat(task.created_at) for task in
				 completed_tasks), timedelta())
			average_completion_time = total_completion_time / completed_tasks_no
		else:
			average_completion_time = None

		# Build the report
		report = {
			"total": total_tasks_no,
			"completed": completed_tasks_no,
			"pending": total_tasks_no - completed_tasks_no
		}

		# Add average completion time if available
		if average_completion_time:
			report.update({"average_completion_time": self.format_average_completion_time(average_completion_time)})

		return report

	@staticmethod
	def format_average_completion_time(average_completion_time):
		total_seconds = int(average_completion_time.total_seconds())
		minutes, seconds = divmod(total_seconds, 60)
		return f"{minutes}m {seconds}s"