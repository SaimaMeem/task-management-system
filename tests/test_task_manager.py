import unittest
from datetime import datetime
from unittest.mock import MagicMock

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):

	def setUp(self):
		self.storage = MagicMock()
		self.manager = TaskManager(self.storage)

	def test_add_task(self):
		task1 = self.manager.add_task("Test Task", "Description")
		self.storage.save_task.assert_called_once_with(task1)
		self.assertEqual(task1.title, "Test Task")
		self.assertEqual(task1.description, "Description")

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

	def test_complete_nonexistent_task(self):
		self.storage.get_task.return_value = None
		result = self.manager.complete_task("Non-existent Task")
		self.assertFalse(result)


if __name__ == "__main__":
	unittest.main()
