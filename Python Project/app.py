from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123",  # Replace with your actual MySQL password
        database="student_db"
    )

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']

    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, age, grade))
    conn.commit()
    conn.close()

    return "<h3>Student added successfully! <a href='/'>Go back</a> | <a href='/students'>View Students</a></h3>"

# Show all students
@app.route('/students')
def students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, age, grade FROM students")
    student_list = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=student_list)

if __name__ == '__main__':
    app.run(debug=True)
