import json

class Project:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def complete_task(self, task):
        task.complete()

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]

    def get_incomplete_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def display_tasks(self):
        print("Aktualne zadania w projekcie:")
        print("Tytuł\tOpis\tPriorytet\tStatus")
        for task in self.tasks:
            completed = "Zakończone" if task.completed else "Nie zakończone"
            print(f"{task.title}\t{task.description}\t{task.priority}\t{completed}")
        print("--------------------")

class Task:
    def __init__(self, title, description, priority, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed

    def complete(self):
        self.completed = True

    def edit(self, new_title, new_description, new_priority):
        self.title = new_title
        self.description = new_description
        self.priority = new_priority

class ProjectManager:
    def __init__(self):
        self.projects = []

    def create_project(self, title, description, due_date):
        project = Project(title, description, due_date)
        self.projects.append(project)
        return project

    def remove_project(self, project):
        self.projects.remove(project)

    def save_projects(self, filename):
        data = []
        for project in self.projects:
            project_data = {
                "title": project.title,
                "description": project.description,
                "due_date": project.due_date,
                "tasks": [
                    {
                        "title": task.title,
                        "description": task.description,
                        "priority": task.priority,
                        "completed": task.completed
                    }
                    for task in project.tasks
                ]
            }
            data.append(project_data)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_projects(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        self.projects = []
        for project_data in data:
            project = Project(project_data["title"], project_data["description"], project_data["due_date"])
            for task_data in project_data["tasks"]:
                task = Task(task_data["title"], task_data["description"], task_data["priority"])
                task.completed = task_data["completed"]
                project.add_task(task)

            self.projects.append(project)

def save_tasks(tasks, filename):
    with open(filename, 'w') as file:
        json.dump(tasks, file)

def load_tasks(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

project_manager = ProjectManager()

project1 = project_manager.create_project("Aplikacja do zarządzania zadaniami", "Aplikacja webowa do śledzenia zadań", "2023-06-30")

tasks = load_tasks('tasks.json')
for task_data in tasks:
    task = Task(task_data['title'], task_data['description'], task_data['priority'], task_data['completed'])
    project1.add_task(task)

def add_new_task(project):
    title = input("Podaj tytuł zadania: ")
    description = input("Podaj opis zadania: ")
    priority = input("Podaj priorytet zadania: ")
    task = Task(title, description, priority)
    project.add_task(task)
    print("Dodano nowe zadanie:")
    print("Tytuł:", task.title)
    print("Opis:", task.description)
    print("Priorytet:", task.priority)
    print("--------------------")


while True:
    command = input("Wprowadź komendę (add - dodaj nowe zadanie, delete - usuń zadanie, complete - oznacz zadanie jako zakończone, display - wyświetl zadania, quit - wyjście): ")
    if command == "add":
        add_new_task(project1)
    elif command == "delete":
        task_title = input("Podaj tytuł zadania do usunięcia: ")
        for task in project1.tasks:
            if task.title == task_title:
                project1.remove_task(task)
                print(f"Usunięto zadanie o tytule: {task_title}")
                break
        else:
            print("Zadanie o podanym tytule nie zostało znalezione.")
    elif command == "complete":
        task_title = input("Podaj tytuł zadania do oznaczenia jako zakończone: ")
        for task in project1.tasks:
            if task.title == task_title:
                task.complete()
                print(f"Zadanie o tytule {task_title} zostało oznaczone jako zakończone.")
                break
        else:
            print("Zadanie o podanym tytule nie zostało znalezione.")
    elif command == "display":
        project1.display_tasks()
    elif command == "quit":

        tasks = []
        for task in project1.tasks:
            task_data = {
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'completed': task.completed
            }
            tasks.append(task_data)
        save_tasks(tasks, 'tasks.json')

        print("Program zakończony.")
        break
