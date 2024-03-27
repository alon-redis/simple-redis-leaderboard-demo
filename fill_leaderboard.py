import redis
import random
from faker import Faker
import sys

def fill_redis(redis_host, redis_port):
    # Redis connection
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, db=0, decode_responses=True
    )
    
    # Clear existing leaderboard data
    redis_client.delete('leaderboard')
    
    # Faker instance for generating names
    faker = Faker()
    
    # Add players with real-sounding names and random scores
    for _ in range(1000):
        player_name = faker.name()
        player_score = random.randint(0, 99)
        redis_client.zadd('leaderboard', {player_name: player_score})

    # Add special player "MHFC" with a score of 100
    redis_client.zadd('leaderboard', {'MHFC': 100})    

    print("Redis filled with players and scores.")

if __name__ == "__main__":
    # Check for command line arguments
    if len(sys.argv) < 3:
        print("Usage: python fill_redis.py <redis_host> <redis_port>")
        sys.exit(1)
    
    # Get Redis host and port from command line arguments
    redis_host = sys.argv[1]
    redis_port = int(sys.argv[2])
    
    # Fill Redis with players and scores
    fill_redis(redis_host, redis_port)
