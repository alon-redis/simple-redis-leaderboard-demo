# Leaderboard Application

This is a simple leaderboard application built with Python Flask and Redis. Users can play a game, answer questions, and view the leaderboard with player scores.

## Prerequisites

Before running the application, make sure you have the following installed:

- Ubuntu Server (22.04 or later)
- Redis Server

## Installation

1. **Python 3:** If you haven't installed Python 3, you can install it using the following commands:

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```

2. **Redis-Py:**
   
   Install the Redis client for Python using pip:

    ```bash
    pip3 install redis
    ```

3. **Flask:**

    Install Flask, a lightweight WSGI web application framework:

    ```bash
    pip3 install flask
    ```

4. **Faker (Optional - for generating fake player names):**

    If you want to use Faker to generate fake player names, install it:

    ```bash
    pip3 install faker
    ```

## How to Run the Application

1. Clone the repository:

    ```bash
    git clone https://github.com/alon-redis/simple-redis-leaderboard-demo.git
    cd simple-redis-leaderboard-demo/
    ```

2. Start the Redis Server:

    Ensure that Redis Server is running on your system. If not, start it using:

    ```bash
    redis-server
    ```

3. Run the Flask App:

    Run the Flask application script `app.py`:

    ```bash
    python3 app.py <redis_host> <redis_port>
    ```

    Replace `<redis_host>` and `<redis_port>` with your Redis server host and port.

4. Access the Application:

    Open a web browser and go to:

    ```
    http://public IP:12000/
    ```

## Usage

- Click on the "Play" button to start playing the game.
- Answer the questions and submit your answers.
- View the leaderboard to see the scores of all players.
- The leaderboard also displays the number of players, perfect score players (100), and high score players (90-100).
