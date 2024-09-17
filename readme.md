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


## Explanation of Solutions
### Required Missing Functionalities
 - **Data Persistence Across Sessions:** To ensure that user data remains intact and accessible across sessions, I have implemented a data persistence mechanism using a JSON file. This approach allows the application to store tasks and their details in a structured format, making it possible to add, edit, and delete tasks while preserving all information between sessions.


 - **Average Completion Time Calculation for Reports:** To calculate the average completion time, I have introduced a `completed_at` parameter in the `Task` class. This parameter records the timestamp when a task is completed. For generating reports, the application computes the time difference between the task's `created_at` and `completed_at` timestamps for all completed tasks. It then sums these time differences and divides by the total number of completed tasks to determine the average completion time.

### Bugs
 - List All Tasks
   - **Issue:** There was a bug in the `list_tasks` method where specifying the flag to list only pending tasks would still include completed tasks. This issue occurred because the `include_completed` parameter was not properly utilized to filter tasks based on their completion status.

   - **Fix:** I corrected this by using the `include_completed` parameter to handle the filtering of tasks. Now, the method correctly distinguishes between showing all tasks, or only pending tasks based on the provided flags.

### Refactoring
- The `main` class has been refactored to organize task management operations into individual functions (`handle_add`, `handle_update`, etc.) to improve modularity. It uses `argparse` to handle command-line arguments and maps them to specific handler functions via a dictionary. This approach simplifies command execution, enhances readability, and separates concerns, making the code easier to maintain and extend.

-  The `Task` class now includes `to_dict` and `from_dict` methods. These methods enable easier conversion between `Task` objects and dictionaries, facilitating storage and retrieval in a structured format like JSON.
    - `to_dict` converts the task's attributes into a dictionary.
    - `from_dict` is a class method that reconstructs a Task object from a dictionary. 

   This addition improves data persistence and serialization, making it easier to store tasks in files and reload them during application startup.

### Additional Functionalities
Upon reviewing the system, I identified and added several essential functionalities:
    
- **Add Task:** Tasks are now case-insensitive, meaning '**Task 1**', '**task 1**', and '**TASK 1**' are considered the same. A task with the same name cannot be added if it is pending, but it can be added if the existing task is completed.

- **Update Task:** Only the task description can be updated. The task title remains unique and unchangeable.

- **Delete Task:** Tasks can be deleted based on their title.

- **Clear Task List:** Allows for the complete removal of all tasks, providing a fresh start.

- **List Only Completed Tasks:** Provides an option to filter by using flag(`--completed`) and list only the completed tasks.

- **Search Task and Show Details:** Enables searching for a task by its title and displays its details.

 - **Format Average Completion Time:** Converts the average completion time into a more readable format, enhancing usability over the default datetime format.


### Proposed Improvements

To enhance the task management system’s functionality, security, and reporting capabilities, the following improvements are recommended:

 - **Unique Task ID:** Introduce a unique identifier for each task. This change ensures that tasks are distinguished by an ID rather than titles, which may be duplicated.

  - **Due Date Feature:** Add an option to specify a due date for tasks. This feature will allow the system to track and report tasks based on their due dates, identifying overdue tasks and improving task management.

  - **In-Progress Status:** Introduce an "**In Progress**" status for tasks. This addition will provide better task separation and enable more detailed reporting on tasks that are currently underway.


### CLI Commands for Additional Functionalities
- **Update Task:**

        poetry run python main.py update "Buy groceries" "Milk, eggs, butter, and bread"

- **Delete Task:**

        poetry run python main.py delete "Pay Internet Bill"

- **Clear Task List:**

        poetry run python main.py clear

- **List Only Completed Tasks:**

        poetry run python main.py list --completed

- **Search Task and Show Details:**

        poetry run python main.py search "Buy groceries"

### Test Cases for Additional Functionalities
I have added some new test cases to ensure the new functionalities work as intended and to enhance overall system reliability. These tests cover:
- Test Add Task When Existing Task Not Completed
- Test Add Task When Existing Task Completed
- Test Edit Task
- Test Edit Nonexistent Task
- Test Complete Task
- Test Delete Task
- Test Delete Nonexistent Task
- Test Clear All Tasks
- Test List Tasks Only Completed
- Test Search Task
- Test Search Nonexistent Task
- Test Generate Report With No Completed Tasks
- Test Generate Report With All Completed Tasks
- Test Format Average Completion Time