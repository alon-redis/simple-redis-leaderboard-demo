from flask import Flask, render_template, request, redirect, url_for, session
import redis
import random
from generate_questions import generate_math_questions
import sys

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Play page
@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        # Get player name from form
        player_name = request.form['player_name']
        
        # Generate math questions
        questions = generate_math_questions(num_questions=10)
        
        # Store player name in session
        session['player_name'] = player_name
        print(session['player_name'])
        
        # Pass enumerate function to template context
        template_context = {
            'player_name': player_name,
            'questions': questions,
            'enumerate': enumerate
        }
        
        # Render play page with questions
        return render_template('play.html', **template_context)
    
    # If accessed via link, redirect to play form
    return render_template('play_form.html')

# Leaderboard page
@app.route('/leaderboard')
def leaderboard():
    # Get Redis host and port from command line arguments
    if len(sys.argv) < 3:
        print("Usage: python app.py <redis_host> <redis_port>")
        sys.exit(1)
    
    redis_host = sys.argv[1]
    redis_port = int(sys.argv[2])
    
    # Redis connection
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, db=0, decode_responses=True
    )
    
    # Get leaderboard from Redis
    leaderboard = redis_client.zrevrange('leaderboard', 0, -1, withscores=True)
    
    # Count number of players
    num_players = redis_client.zcard('leaderboard')
    
    # Count number of players with perfect score (100)
    perfect_score_players = redis_client.zcount('leaderboard', 100, 100)
    
    # Count number of players with score between 90 and 100
    high_score_players = redis_client.zcount('leaderboard', 90, 100)
    
    # Pass data to template context
    template_context = {
        'leaderboard': leaderboard,
        'num_players': num_players,
        'perfect_score_players': perfect_score_players,
        'high_score_players': high_score_players,
        'enumerate': enumerate
    }
    
    # Render leaderboard page
    return render_template('leaderboard.html', **template_context)

# Process player answers and calculate score
@app.route('/process_answers', methods=['POST'])
def process_answers():
    if request.method == 'POST':
        player_name = session.get('player_name')
        questions = [request.form[f'answer_{i+1}'] for i in range(10)]
        
        # Calculate player score (random number between 0 and 100)
        player_score = random.randint(0, 99)
        
        # Get Redis host and port from command line arguments
        if len(sys.argv) < 3:
            print("Usage: python app.py <redis_host> <redis_port>")
            sys.exit(1)
        
        redis_host = sys.argv[1]
        redis_port = int(sys.argv[2])
        
        # Redis connection
        redis_client = redis.StrictRedis(
            host=redis_host, port=redis_port, db=0, decode_responses=True
        )
        
        # Store player score in Redis leaderboard
        redis_client.zadd('leaderboard', {player_name: player_score})
        
        # Redirect to leaderboard page
        return redirect(url_for('leaderboard'))

# Liveboard page
@app.route('/liveboard')
def liveboard():
    # Get Redis host and port from command line arguments
    if len(sys.argv) < 3:
        print("Usage: python app.py <redis_host> <redis_port>")
        sys.exit(1)
    
    redis_host = sys.argv[1]
    redis_port = int(sys.argv[2])
    
    # Redis connection
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, db=0, decode_responses=True
    )
    
    # Fetch 5 game keys using SCAN command
    cursor = '0'
    count = 5
    game_keys = []
    cursor, keys = redis_client.scan(cursor=cursor, count=count)
    game_keys.extend(keys)
    
    # Retrieve game boards for each key
    liveboard_data = []
    for key in game_keys:
        game_board = redis_client.zrevrange(key, 0, 9, withscores=True)
        liveboard_data.append(game_board)
    
    # Pass data to template context
    template_context = {
        'liveboard_data': liveboard_data,
        'enumerate': enumerate
    }
    
    # Render liveboard page
    return render_template('liveboard.html', **template_context)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000)
