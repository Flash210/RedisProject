import time
from threading import Thread
from task_manager import TaskManager
from notification_system import NotificationSystem
from notification_listener import notification_listener

if __name__ == "__main__":
    task_manager = TaskManager()
    notification_system = NotificationSystem()

    user_id = "Houcem"

    # Add Task
    task_id = task_manager.add_task(user_id, "Complete the Redis Project", "2024-12-30")

    # Mark Task as Complete
    task_manager.complete_task(task_id)

    # Get User Tasks
    tasks = task_manager.get_user_tasks(user_id)
    print("Pending Tasks:", tasks)

    # Send Notification
    notification_system.send_notification(user_id, "Your task is due soon!", "warning")

    # Get Recent Notifications
    notifications = notification_system.get_recent_notifications(user_id)
    print("Recent Notifications:", notifications)

    # Start Notification Listener in a Separate Thread
    listener_thread = Thread(target=notification_listener, args=(user_id,))
    listener_thread.start()

    # Simulate New Notification
    time.sleep(2)
    notification_system.send_notification(user_id, "You have a new message.", "info")
