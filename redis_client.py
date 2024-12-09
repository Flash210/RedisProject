import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

if redis_client.ping():
    print("Connected to Redis!")
else:
    raise ConnectionError("Failed to connect to Redis.")
