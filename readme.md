# Task Management System

This is a simple command-line (CLI) task management system implemented in Python.

## Functional Requirements

The application should allow users to do the following:

1. Add a new task
2. Complete a task
3. List all tasks (with an option to show only incomplete tasks)
4. Generate a report of task statistics, which should include:
   - Total number of tasks
   - Number of completed tasks
   - Number of pending tasks
   - Average time taken to complete a task
5. The application must persist user data across sessions, ensuring that all information remains intact and accessible upon returning, without resetting or losing any previously entered tasks

## Setup

1. Ensure you have Python 3.7 or higher but less than 3.12 installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory which `task_management_system` in the terminal.
4. Install Poetry if you don't have it installed:

   - for **macOS/Linux**:
       ```
       curl -sSL https://install.python-poetry.org | python3 -
       ```
   - for **Windows** using pip:
   
       ```
       pip poetry install
       ```
5. Install dependencies
   - for **macOS/Linux**:
       ```
       poetry install
       ```
6.  Running the application
    ```
    poetry run python main.py
    ```

## Running Tests

To run all the unit tests, use the following command:

```
python -m unittest discover tests
```

## Task

**Ensure and validate with tests that the app meets the required functionality** and addresses any bugs. Enhance performance and do optimisations to the best of your knowledge, while refactoring the code for better readability and maintainability. Feel free to make necessary assumptions where applicable.


## Thoughts, Justification, and Explanation of Solutions
### Required Missing Functionalities
 - **Data Persistence Across Sessions:** To ensure that user data remains intact and accessible across sessions, I have implemented a data persistence mechanism using a JSON file. This approach allows the application to store tasks and their details in a structured format, making it possible to add, edit, and delete tasks while preserving all information between sessions.


 - **Average Completion Time Calculation for Reports:** To calculate the average completion time, I have introduced a `completed_at` parameter in the `Task` class. This parameter records the timestamp when a task is completed. For generating reports, the application computes the time difference between the task's `created_at` and `completed_at` timestamps for all completed tasks. It then sums these time differences and divides by the total number of completed tasks to determine the average completion time.

### Bugs
 - List All Tasks
   - **Issue:** There was a bug in the `list_tasks` method where specifying the flag to list only pending tasks would still include completed tasks. This issue occurred because the `include_completed` parameter was not properly utilized to filter tasks based on their completion status.

   - **Fix:** I corrected this by using the `include_completed` parameter to handle the filtering of tasks. Now, the method correctly distinguishes between showing all tasks, or only pending tasks based on the provided flags.