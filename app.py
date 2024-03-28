from flask import Flask, render_template, request, redirect, url_for, session
import redis
import random
from generate_questions import generate_math_questions
import sys

app = Flask(__name__)
app.secret_key = "super_secret_key"

def get_player_statistics(redis_client):
    perfect_score_players = redis_client.zcount('leaderboard', 100, 100)
    high_score_players = redis_client.zcount('leaderboard', 90, 100)
    return perfect_score_players, high_score_players

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Play page
@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        player_name = request.form['player_name']
        questions = generate_math_questions(num_questions=10)
        session['player_name'] = player_name
        template_context = {
            'player_name': player_name,
            'questions': questions,
            'enumerate': enumerate
        }
        return render_template('play.html', **template_context)
    
    return render_template('play_form.html')

# Leaderboard page
@app.route('/leaderboard')
def leaderboard():
    if len(sys.argv) < 3:
        print("Usage: python app.py <redis_host> <redis_port>")
        sys.exit(1)
    
    redis_host = sys.argv[1]
    redis_port = int(sys.argv[2])
    
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, db=0, decode_responses=True
    )
    
    leaderboard = redis_client.zrevrange('leaderboard', 0, -1, withscores=True)
    num_players = redis_client.zcard('leaderboard')
    
    perfect_score_players, high_score_players = get_player_statistics(redis_client)
    
    template_context = {
        'leaderboard': leaderboard,
        'num_players': num_players,
        'perfect_score_players': perfect_score_players,
        'high_score_players': high_score_players,
        'enumerate': enumerate
    }
    
    return render_template('leaderboard.html', **template_context)

# Process player answers and calculate score
@app.route('/process_answers', methods=['POST'])
def process_answers():
    if request.method == 'POST':
        player_name = session.get('player_name')
        questions = [request.form[f'answer_{i+1}'] for i in range(10)]
        player_score = random.randint(0, 99)
        
        if len(sys.argv) < 3:
            print("Usage: python app.py <redis_host> <redis_port>")
            sys.exit(1)
        
        redis_host = sys.argv[1]
        redis_port = int(sys.argv[2])
        
        redis_client = redis.StrictRedis(
            host=redis_host, port=redis_port, db=0, decode_responses=True
        )
        
        redis_client.zadd('leaderboard', {player_name: player_score})
        
        return redirect(url_for('leaderboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000)
