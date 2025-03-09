from flask import Flask, request, jsonify
import mariadb
import sys

app = Flask(__name__)

# Database Configuration
config = {
    'host': 'localhost',
    'user': 'phelix',
    'password': 'phelix',
    'database': 'Kazi',
    'port': 3306
}

# Test Database Connection
try:
    conn = mariadb.connect(**config)
    cursor = conn.cursor()
    print("Connected to MariaDB database")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

# Worker Login Endpoint
@app.route('/api/worker/login', methods=['POST'])
def worker_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    try:
        cursor.execute(
            "SELECT * FROM workers WHERE email = ? AND password = ?",
            (email, password)
        )
        worker = cursor.fetchone()

        if worker:
            return jsonify({'success': True, 'message': 'Login successful', 'user': worker})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    except mariadb.Error as e:
        print(f"Error during worker login: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Employer Login Endpoint
@app.route('/api/employer/login', methods=['POST'])
def employer_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    try:
        cursor.execute(
            "SELECT * FROM employers WHERE email = ? AND password = ?",
            (email, password)
        )
        employer = cursor.fetchone()

        if employer:
            return jsonify({'success': True, 'message': 'Login successful', 'user': employer})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    except mariadb.Error as e:
        print(f"Error during employer login: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Start the Server
if __name__ == '__main__':
    app.run(debug=True, port=5000)