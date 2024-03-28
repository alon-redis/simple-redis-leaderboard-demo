import redis
import random
import string
import sys

# Function to generate random strings
def random_string(length):
    letters = string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# Check if the required arguments are provided
if len(sys.argv) != 6:
    print("Usage: python script.py <redis_host> <redis_port> <num_players> <num_games> <loop_count>")
    sys.exit(1)

# Parse command-line arguments
host = sys.argv[1]
port = int(sys.argv[2])
num_players = int(sys.argv[3])
num_games = int(sys.argv[4])
loop_count = int(sys.argv[5])

# Create a Redis connection pool
pool = redis.ConnectionPool(host=host, port=port, max_connections=25)

# Generate game names
game_names = [f"game_{random_string(5)}" for _ in range(num_games)]

# Generate player names
player_names = [f"player{random_string(5)}" for _ in range(num_players)]

# Run the loop
for _ in range(loop_count):
    # Connect to Redis using the connection pool
    r = redis.Redis(connection_pool=pool)

    # Generate player scores
    scores = [random.randint(0, 999) for _ in range(num_players * num_games)]

    # Store player scores in Redis leaderboards
    for game_name in game_names:
        for i, player_name in enumerate(player_names):
            score = scores[i::num_players]
            for s in score:
                r.zadd(game_name, {player_name: s})

    # Print the top 5 players and scores for each game
    for game_name in game_names:
#        print(f"\nTop 5 players for {game_name}:")
        leaderboard = r.zrevrangebyscore(game_name, '+inf', '-inf', withscores=True, start=0, num=5)
#        for player, score in leaderboard:
#            print(f"{player.decode('utf-8')}: {score}")
