from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os, json

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'students.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT, subject TEXT, score REAL)''')
    # Insert sample data if table empty
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        sample = [
            ('Asha','Mathematics', 72.0),
            ('Rohit','Physics', 58.5),
            ('Neha','Chemistry', 35.0),
            ('Vikram','Mathematics', 88.0)
        ]
        conn.executemany("INSERT INTO students (name, subject, score) VALUES (?, ?, ?)", sample)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    subject = request.form.get('subject')
    try:
        score = float(request.form.get('score'))
    except:
        score = 0.0

    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO students (name, subject, score) VALUES (?, ?, ?)", (name, subject, score))
    conn.commit()
    conn.close()
    return redirect(url_for('result', name=name, subject=subject, score=score))

def get_recommendation(score, subject):
    if score < 40:
        return f"You need improvement in {subject}. Recommended: Watch beginner tutorials and practice fundamentals."
    elif 40 <= score < 70:
        return f"Good progress in {subject}! Revise intermediate concepts and solve practice problems."
    else:
        return f"Excellent work in {subject}! Try advanced topics and build a mini project."

@app.route('/result')
def result():
    name =  request.args.get('name','Student')
    subject = request.args.get('subject','Subject')
    score = float(request.args.get('score',0))
    recommendation = get_recommendation(score, subject)
    return render_template('result.html', name=name, subject=subject, score=score, recommendation=recommendation)

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, subject, score FROM students ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    # pass JSON for chart
    chart_data = json.dumps([{'name': r[1], 'subject': r[2], 'score': r[3]} for r in data])
    return render_template('dashboard.html', data=data, chart_data=chart_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
