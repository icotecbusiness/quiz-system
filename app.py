# =============================
# FINAL WEB-BASED TEST SYSTEM
# READY FOR RENDER DEPLOYMENT
# =============================

from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
from io import BytesIO
from datetime import datetime

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)
app.secret_key = 'secret123'

# -------- DATABASE ----------
def get_db():
    db_path = os.path.join(os.getcwd(), 'database.db')
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

# -------- INIT DATABASE ------
def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        question TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct TEXT
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        subject_id INTEGER,
        score INTEGER
    )
    """)

    # Insert default subjects if empty
    count = db.execute("SELECT COUNT(*) as c FROM subjects").fetchone()['c']
    if count == 0:
        db.execute("INSERT INTO subjects(name) VALUES ('MS Word')")
        db.execute("INSERT INTO subjects(name) VALUES ('MS Excel')")
        db.execute("INSERT INTO subjects(name) VALUES ('Operating Systems')")
        db.execute("INSERT INTO subjects(name) VALUES ('Computer Networks')")

    db.commit()

# 🔥 CALL INIT
init_db()

# -------- HOME --------------
@app.route('/')
def home():
    return render_template('index.html')

# -------- REGISTER ----------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (request.form['name'], request.form['email'], request.form['password'], 'student')
        )
        db.commit()
        return redirect('/login')
    return render_template('register.html')

# -------- LOGIN -------------
@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    if request.method == 'POST':
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (request.form['email'], request.form['password'])
        ).fetchone()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['username'] = user['name']

            if user['role'] == 'admin':
                return redirect('/admin')
            return redirect('/dashboard')
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

# -------- LOGOUT ------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -------- DASHBOARD ---------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()

    subjects = db.execute("SELECT * FROM subjects").fetchall()

    completed = db.execute(
        "SELECT subject_id FROM results WHERE user_id=?",
        (session['user_id'],)
    ).fetchall()

    completed_ids = [row['subject_id'] for row in completed]

    return render_template('dashboard.html',
                           subjects=subjects,
                           completed_subject_ids=completed_ids)

# -------- QUIZ -------------
@app.route('/quiz/<int:subject_id>', methods=['GET','POST'])
def quiz(subject_id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()

    if request.method == 'POST':
        questions = db.execute(
            "SELECT * FROM questions WHERE subject_id=?",
            (subject_id,)
        ).fetchall()

        # Ensure all answered
        for q in questions:
            if request.form.get(str(q['id'])) is None:
                return "⚠️ Answer all questions."

        score = 0
        for q in questions:
            if request.form.get(str(q['id'])) == q['correct']:
                score += 1

        db.execute(
            "INSERT INTO results(user_id,subject_id,score) VALUES(?,?,?)",
            (session['user_id'], subject_id, score)
        )
        db.commit()

        total = len(questions)
        percent = (score / total) * 100 if total else 0

        return render_template('result.html',
                               score=score,
                               total=total,
                               percentage=round(percent,2))

    questions = db.execute(
        "SELECT * FROM questions WHERE subject_id=?",
        (subject_id,)
    ).fetchall()

    return render_template('quiz.html', questions=questions)

# -------- MY RESULTS --------
@app.route('/my_results')
def my_results():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()

    results = db.execute("""
        SELECT subjects.name as subject, results.score, subjects.id as subject_id
        FROM results
        JOIN subjects ON subjects.id = results.subject_id
        WHERE results.user_id=?
    """, (session['user_id'],)).fetchall()

    final = []
    for r in results:
        total = db.execute(
            "SELECT COUNT(*) as cnt FROM questions WHERE subject_id=?",
            (r['subject_id'],)
        ).fetchone()['cnt']

        percent = (r['score'] / total) * 100 if total else 0

        final.append({
            'subject': r['subject'],
            'score': r['score'],
            'total': total,
            'percentage': round(percent,2)
        })

    return render_template('my_results.html', results=final)

# -------- PDF CERTIFICATE ----
@app.route('/my_certificate_pdf')
def my_certificate_pdf():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()

    student = db.execute("SELECT * FROM users WHERE id=?",
                         (session['user_id'],)).fetchone()

    results = db.execute("""
        SELECT subjects.name as subject, results.score, subjects.id as subject_id
        FROM results
        JOIN subjects ON subjects.id = results.subject_id
        WHERE results.user_id=?
    """, (session['user_id'],)).fetchall()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>ICOTEC TRAINING CENTER</b>", styles['Title']))
    elements.append(Paragraph("P.O Box 515-01020 Kenol | Tel: 0750118615", styles['Normal']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph("<b>PRELIMINARY RESULTS</b>", styles['Heading1']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Student: <b>{student['name']}</b>", styles['Normal']))
    elements.append(Spacer(1,20))

    data = [["Subject","Score","Total","%","Status"]]

    for r in results:
        total = db.execute(
            "SELECT COUNT(*) as cnt FROM questions WHERE subject_id=?",
            (r['subject_id'],)
        ).fetchone()['cnt']

        percent = (r['score'] / total) * 100 if total else 0
        status = "PASS" if percent >= 50 else "FAIL"

        data.append([r['subject'], r['score'], total, round(percent,2), status])

    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white)
    ]))

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return send_file(buffer,
                     as_attachment=True,
                     download_name="results.pdf",
                     mimetype='application/pdf')

# -------- ADMIN ------------
@app.route('/admin')
def admin():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect('/login')

    db = get_db()

    results = db.execute("""
        SELECT users.name as student, subjects.name as subject, results.score
        FROM results
        JOIN users ON users.id = results.user_id
        JOIN subjects ON subjects.id = results.subject_id
    """).fetchall()

    questions = db.execute("SELECT * FROM questions").fetchall()

    return render_template('admin.html',
                           results=results,
                           questions=questions)

# -------- RUN --------------
if __name__ == '__main__':
    app.run()