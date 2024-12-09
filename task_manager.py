from redis_client import redis_client

class TaskManager:
    def __init__(self):
        self.next_task_id_key = "task:next_id"
        redis_client.setnx(self.next_task_id_key, 1)

    def get_next_task_id(self):
        return redis_client.incr(self.next_task_id_key)



    def add_task(self, user_id, description, due_date, expiration=86400):
        task_id = self.get_next_task_id()
        task_key = f"task:{task_id}"

        redis_client.hset(task_key, mapping={
            "user_id": user_id,
            "description": description,
            "due_date": due_date,
            "status": "pending"
        })
        redis_client.rpush(f"tasks:pending:{user_id}", task_id)
        redis_client.expire(task_key, expiration)
        redis_client.sadd("active_users", user_id)

        print(f"Task {task_id} added for user {user_id}")
        return task_id

    def complete_task(self, task_id):
        task_key = f"task:{task_id}"
        if redis_client.exists(task_key):
            redis_client.hset(task_key, "status", "completed")
            print(f"Task {task_id} marked as completed.")
        else:
            print(f"Task {task_id} does not exist or has expired.")

    def get_user_tasks(self, user_id):
        pending_tasks = redis_client.lrange(f"tasks:pending:{user_id}", 0, -1)
        tasks = [redis_client.hgetall(f"task:{task_id}") for task_id in pending_tasks]
        return tasks
