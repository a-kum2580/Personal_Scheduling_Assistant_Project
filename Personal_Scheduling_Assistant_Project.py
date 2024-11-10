from datetime import datetime, timedelta
from heapq import heappop, heappush
import matplotlib.pyplot as plt

# Task class to represent a single task with properties such as name, type, deadline, priority, and duration
class Task:
    def __init__(self, name, task_type, deadline, priority, duration):
        self.name = name
        self.task_type = task_type  # "personal" or "academic"
        self.deadline = deadline  # datetime object
        self.priority = priority  # Integer priority level
        self.duration = duration  # Duration in minutes

    def __repr__(self):
        return f"{self.name} ({self.task_type}) - Priority: {self.priority}, Due: {self.deadline.strftime('%Y-%m-%d %H:%M')}, Duration: {self.duration} min"

# TaskManager class to manage task addition, retrieval, and scheduling
class TaskManager:
    def __init__(self):
        self.tasks = []  # Min-heap for priority-based task sorting
        self.schedule = []  # List of scheduled tasks

    # Method to add a task into the priority queue
    def add_task(self, task):
        heappush(self.tasks, (task.priority, task.deadline, task))

    # Retrieve upcoming tasks sorted by deadline
    def get_upcoming_tasks(self):
        return [task for _, _, task in sorted(self.tasks, key=lambda x: x[1])]

    # Method to schedule tasks based on priority and deadline
    def schedule_tasks(self):
        current_time = datetime.now()
        scheduled_tasks = []
        
        for priority, deadline, task in sorted(self.tasks):
            if current_time + timedelta(minutes=task.duration) <= deadline:
                scheduled_tasks.append(task)
                current_time += timedelta(minutes=task.duration)
        
        self.schedule = scheduled_tasks
        return self.schedule

    # Analyze task density by plotting the distribution of deadlines over time
    def analyze_task_density(self):
        deadlines = [task.deadline for _, _, task in self.tasks]
        deadlines.sort()
        density_times = [deadlines[0] + timedelta(hours=i) for i in range(int((deadlines[-1] - deadlines[0]).total_seconds() // 3600) + 1)]
        density_values = [sum(1 for deadline in deadlines if deadline <= time) for time in density_times]
        
        plt.figure()
        plt.plot(density_times, density_values, marker='o', color="purple")
        plt.xlabel("Time")
        plt.ylabel("Number of Tasks Due")
        plt.title("Task Density Over Time")
        plt.grid(True)
        plt.show()

# Plot Gantt chart to visualize scheduled tasks with enhanced aesthetics
def plot_gantt_chart(tasks):
    if not tasks:
        print("No tasks available to plot.")
        return
    
    fig, gnt = plt.subplots(figsize=(10, 5))  # Set a larger figure size for better readability
    gnt.set_ylim(0, 50)
    gnt.set_xlim(min(task.deadline for task in tasks), max(task.deadline for task in tasks) + timedelta(minutes=60))
    gnt.set_yticks([15, 25])
    gnt.set_yticklabels(['Academic', 'Personal'])
    gnt.set_xlabel('Time')
    gnt.set_title('Task Schedule Gantt Chart')
    
    # Loop through tasks to plot based on type and duration with custom colors and labels
    for task in tasks:
        start = task.deadline - timedelta(minutes=task.duration)
        color = 'skyblue' if task.task_type == "academic" else 'salmon'  # Use different colors for task types
        gnt.broken_barh([(start, timedelta(minutes=task.duration))], 
                        (15 if task.task_type == "academic" else 25, 9),
                        facecolors=color, edgecolor='black', label=task.name)
    
    # Add a legend for task types and ensure no duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    gnt.legend(unique_labels.values(), unique_labels.keys())
    
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

# Function to prompt the user to input tasks manually
def get_user_input(manager):
    print("Enter your tasks. Type 'done' when finished.")
    
    while True:
        name = input("Task name (or type 'done' to finish): ")
        if name.lower() == 'done':
            break

        task_type = input("Task type (academic/personal): ").strip().lower()
        while task_type not in ['academic', 'personal']:
            task_type = input("Please enter a valid task type (academic/personal): ").strip().lower()

        # Deadline input with error handling
        while True:
            deadline_str = input("Deadline (YYYY-MM-DD HH:MM): ")
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
                break
            except ValueError:
                print("Invalid format. Please enter the deadline in the format YYYY-MM-DD HH:MM")

        priority = int(input("Priority (1 for highest priority): "))
        duration = int(input("Duration in minutes: "))

        # Create a task object and add it to the manager
        task = Task(name, task_type, deadline, priority, duration)
        manager.add_task(task)
        print(f"Task '{name}' added.\n")

# Menu function to provide user with available options
def display_menu(manager):
    # Add some predefined tasks to demonstrate functionality
    manager.add_task(Task("Calculus Assignment", "academic", datetime.now() + timedelta(hours=5), 1, 120))
    manager.add_task(Task("Project Report", "academic", datetime.now() + timedelta(hours=12), 2, 180))
    manager.add_task(Task("Self-Care", "personal", datetime.now() + timedelta(hours=8), 3, 60))
    
    while True:
        print("\n--- Personal Scheduling Assistant ---")
        print("1. Add Task")
        print("2. View Upcoming Tasks")
        print("3. Schedule Tasks")
        print("4. Analyze Task Density")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            get_user_input(manager)
        elif choice == '2':
            upcoming_tasks = manager.get_upcoming_tasks()
            if upcoming_tasks:
                print("\nUpcoming Tasks:")
                for task in upcoming_tasks:
                    print(task)
            else:
                print("No upcoming tasks.")
        elif choice == '3':
            scheduled_tasks = manager.schedule_tasks()
            if scheduled_tasks:
                print("\nScheduled Tasks:")
                for task in scheduled_tasks:
                    print(task)
                plot_gantt_chart(scheduled_tasks)
            else:
                print("No tasks available to schedule.")
        elif choice == '4':
            manager.analyze_task_density()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Main function to initiate the program and call the menu
def main():
    manager = TaskManager()
    display_menu(manager)

# Run the main function
if __name__ == "__main__":
    main()
