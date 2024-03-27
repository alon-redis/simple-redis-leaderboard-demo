from flask import Flask, render_template, request, redirect, url_for, session
import redis
import random
from generate_questions import generate_math_questions

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Redis connection
redis_host = "redis-10000.aws-alon-4758.env0.qa.redislabs.com"
redis_port = 10000
redis_db = 0
redis_client = redis.StrictRedis(
    host=redis_host, port=redis_port, db=redis_db, decode_responses=True
)

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
    # Get leaderboard from Redis
    leaderboard = redis_client.zrevrange('leaderboard', 0, -1, withscores=True)
    
    # Pass enumerate function to template context
    template_context = {
        'leaderboard': leaderboard,
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
        player_score = random.randint(0, 100)
        
        # Store player score in Redis leaderboard
        redis_client.zadd('leaderboard', {player_name: player_score})
        
        # Redirect to leaderboard page
        return redirect(url_for('leaderboard'))

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000)
