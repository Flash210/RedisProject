import time
import json
from redis_client import redis_client

class NotificationSystem:
    def __init__(self):
        self.notification_history_limit = 100

    def send_notification(self, user_id, message, notification_type="info"):
        timestamp = int(time.time())
        notification_key = f"notification:{user_id}:{timestamp}"

        redis_client.hset(notification_key, mapping={
            "message": message,
            "type": notification_type,
            "timestamp": timestamp
        })
        redis_client.expire(notification_key, 86400)
        redis_client.lpush(f"notifications:history:{user_id}", notification_key)
        redis_client.ltrim(f"notifications:history:{user_id}", 0, self.notification_history_limit - 1)

        redis_client.publish(f"notifications:{user_id}", json.dumps({
            "message": message,
            "type": notification_type,
            "timestamp": timestamp
        }))

        print(f"Notification sent to user {user_id}: {message}")

    def get_recent_notifications(self, user_id):
        notification_keys = redis_client.lrange(f"notifications:history:{user_id}", 0, -1)
        notifications = [redis_client.hgetall(key) for key in notification_keys]
        return notifications
