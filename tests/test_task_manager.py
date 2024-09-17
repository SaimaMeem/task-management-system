import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):

	def setUp(self):
		self.storage = MagicMock()
		self.manager = TaskManager(self.storage)

	def test_add_task(self):
		task = self.manager.add_task("Test Task", "Description")

		self.storage.save_task.assert_called_once_with(task)
		self.assertEqual(task.title, "Test Task")
		self.assertEqual(task.description, "Description")

	def test_add_task_when_existing_task_not_completed(self):
		existing_task = Task("Existing Task", "Existing Description")
		self.storage.get_task.return_value = existing_task

		result = self.manager.add_task("Existing Task", "New Description")
		self.assertIsNone(result)
		self.storage.save_task.assert_not_called()


	def test_add_task_when_existing_task_completed(self):
		existing_task = Task("Existing Task", "Existing Description")
		existing_task.completed = True
		self.storage.get_task.return_value = existing_task

		result = self.manager.add_task("Existing Task", "New Description")
		self.assertIsNotNone(result)
		self.storage.save_task.assert_called()

	def test_edit_task(self):
		task = Task("Task to Edit", "Old Description")
		self.storage.get_task.return_value = task

		result = self.manager.edit_task("Task to Edit", "New Description")
		self.assertTrue(result)
		self.assertEqual(task.description, "New Description")
		self.storage.update_task.assert_called_once_with(task)

	def test_edit_nonexistent_task(self):
		self.storage.get_task.return_value = None

		result = self.manager.edit_task("Task to Edit", "New Description")
		self.assertFalse(result)
		self.storage.update_task.assert_not_called()

	def test_complete_task(self):
		task = Task("Task to Complete", "Description")
		self.storage.get_task.return_value = task

		result = self.manager.complete_task("Task to Complete")
		self.assertTrue(result)
		self.assertTrue(task.completed)
		self.assertIsNotNone(task.completed_at)
		self.storage.update_task.assert_called_once_with(task)

	def test_complete_nonexistent_task(self):
		self.storage.get_task.return_value = None

		result = self.manager.complete_task("Non-existent Task")
		self.assertFalse(result)
		self.storage.complete_task.assert_not_called()

	def test_delete_task(self):
		task = Task("Task to Delete", "Description")
		self.storage.get_task.return_value = task

		result = self.manager.delete_task("Task to Delete")
		self.assertTrue(result)
		self.storage.remove_task.assert_called_once_with(task)

	def test_delete_nonexistent_task(self):
		self.storage.get_task.return_value = None

		result = self.manager.delete_task("Non-existent Task")
		self.assertFalse(result)
		self.storage.remove_task.assert_not_called()

	def test_clear_all_tasks(self):
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		self.storage.get_all_tasks.return_value = tasks

		result = self.manager.delete_all_tasks()
		self.storage.clear_all_tasks.assert_called_once_with(tasks)
		self.assertEqual(result, self.storage.clear_all_tasks.return_value)

	def test_list_tasks_exclude_completed(self):
		tasks = [
		    Task("Task 1", "Description 1"),
		    Task("Task 2", "Description 2"),
		    Task("Task 3", "Description 3")
		]
		tasks[1].completed = True
		self.storage.get_all_tasks.return_value = tasks

		result = self.manager.list_tasks()
		self.assertEqual(len(result), 2)
		self.assertNotIn(tasks[1], result)

	def test_list_tasks_only_completed(self):
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		tasks[1].completed = True
		tasks[2].completed = True
		self.storage.get_all_tasks.return_value = tasks
		result = self.manager.list_tasks(only_completed=True)
		self.assertEqual(len(result), 2)
		self.assertIn(tasks[1], result)
		self.assertIn(tasks[2], result)

	def test_search_task(self):
		now = datetime(2024, 9, 17, 12, 0, 0)
		task = Task("Task to Search", "Description")
		task.created_at = now.isoformat()
		self.storage.get_task.return_value = task

		result, formatted_time = self.manager.search_task("Task to Search")
		self.assertEqual(task, result)
		self.assertEqual(formatted_time, "September 17, 2024 at 12:00 PM")

	def test_search_nonexistent_task(self):
		self.storage.get_task.return_value = None
		result = self.manager.search_task("Non-existent Task")
		self.assertIsNone(result)

	def test_generate_report(self):
		now = datetime(2024, 9, 17, 12, 0, 0)
		tasks = [
		    Task("Task 1", "Description 1"),
		    Task("Task 2", "Description 2"),
		    Task("Task 3", "Description 3")
		]
		tasks[0].completed = True
		tasks[0].completed_at = now.isoformat()
		self.storage.get_all_tasks.return_value = tasks

		report = self.manager.generate_report()
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 1)
		self.assertEqual(report["pending"], 2)

	def test_generate_report_with_no_completed_tasks(self):
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		self.storage.get_all_tasks.return_value = tasks
		report = self.manager.generate_report()
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 0)
		self.assertEqual(report["pending"], 3)
		self.assertNotIn("average_completion_time", report)

	def test_generate_report_with_all_completed_tasks(self):
		creation_time = datetime(2024, 9, 17, 10, 0, 0)
		now = datetime(2024, 9, 17, 12, 0, 0)
		tasks = [
			Task("Task 1", "Description 1"),
			Task("Task 2", "Description 2"),
			Task("Task 3", "Description 3")
		]
		for task in tasks:
			task.created_at = creation_time.isoformat()
			task.completed = True
			task.completed_at = now.isoformat()
		self.storage.get_all_tasks.return_value = tasks

		report = self.manager.generate_report()
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 3)
		self.assertEqual(report["pending"], 0)
		self.assertIn("average_completion_time", report)
		self.assertEqual(report["average_completion_time"], "120m 0s")

	def test_format_average_completion_time(self):
		average_time = timedelta(minutes=30, seconds=30)
		formatted_time = self.manager.format_average_completion_time(average_time)
		self.assertEqual(formatted_time, "30m 30s")

if __name__ == "__main__":
	unittest.main()
