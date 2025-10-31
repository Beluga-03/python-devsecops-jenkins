from flask import Flask, jsonify, request


# Add this at the top of app.py
DATABASE_PASSWORD = "hardcoded_password_123"  # Security issue!
API_KEY = "sk-1234567890abcdef"  # Security issue!
SECRET_TOKEN = "my_secret_token_12345"  # Security issue!


app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "task": "Learn DevSecOps", "completed": False},
    {"id": 2, "task": "Setup Jenkins Pipeline", "completed": False}
]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to DevSecOps Lab!", "status": "running"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = {
        "id": len(tasks) + 1,
        "task": request.json.get('task'),
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# Add a vulnerable function
def connect_database():
    import sqlite3
    # Hardcoded credentials - BAD PRACTICE
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % request.args.get('user')  # SQL Injection vulnerability
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)