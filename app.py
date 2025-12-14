from flask import Flask, jsonify, render_template, request, redirect, session, flash, url_for
import random
import string
import pymysql

app = Flask(__name__)
app.secret_key = 'veriden_attendance_2025_secret'

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Killer_9704',
        database='veriden',
        cursorclass=pymysql.cursors.DictCursor
    )

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        user_id = request.form.get('user_id')
        password = request.form.get('password', '')

        conn = get_db_connection()
        cur = conn.cursor()
        
        if user_type == 'teacher':
            cur.execute("SELECT * FROM teachers WHERE teacher_id=%s AND password=%s", (user_id, password))
            teacher = cur.fetchone()
            if teacher:
                session['user_type'] = 'teacher'
                session['user_id'] = user_id
                conn.close()
                return redirect('/teacher_dashboard')
                
        elif user_type == 'student':
            cur.execute("SELECT * FROM students WHERE student_id=%s", (user_id,))
            student = cur.fetchone()
            if student:
                session['user_type'] = 'student'
                session['user_id'] = user_id
                conn.close()
                return redirect('/student_dashboard')
        
        conn.close()
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'user_type' not in session or session['user_type'] != 'teacher':
        return redirect('/')
    
    attendance_data = []
    if 'current_lecture' in session:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.name, a.is_present, a.blur_detected, a.submitted_at 
            FROM attendance a 
            JOIN students s ON a.student_id = s.student_id 
            WHERE a.lecture_id = %s
        """, (session['current_lecture'],))
        attendance_data = cur.fetchall()
        conn.close()
    
    if request.method == 'POST':
        lecture_id = request.form.get('lecture_id', '').upper().strip()
        subject_code = request.form.get('subject_code')
        
        if not lecture_id or not subject_code:
            flash('Please fill all fields!', 'error')
            return render_template('teacher_dashboard.html', attendance=attendance_data)
        
        code = generate_code()
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT lecture_id FROM lectures WHERE lecture_id=%s", (lecture_id,))
        if cur.fetchone():
            flash(f"Lecture {lecture_id} already exists!", 'error')
        else:
            cur.execute("SELECT subject_code FROM subjects WHERE subject_code=%s AND teacher_id=%s", (subject_code, session['user_id']))
            subject_check = cur.fetchone()
            if subject_check:
                cur.execute("""
                    INSERT INTO lectures (lecture_id, teacher_id, subject_code, generated_code, lecture_datetime) 
                    VALUES (%s, %s, %s, %s, NOW())
                """, (lecture_id, session['user_id'], subject_code, code))
                conn.commit()
                session['current_lecture'] = lecture_id
                flash(f"✅ Lecture {lecture_id} ({subject_code}) - Code: {code}", 'success')
            else:
                flash(f"You don't teach {subject_code}!", 'error')
        conn.close()
    
    return render_template('teacher_dashboard.html', attendance=attendance_data)

@app.route('/get_teacher_subjects')
def get_teacher_subjects():
    if 'user_type' not in session or session['user_type'] != 'teacher':
        return jsonify([])
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT subject_code, subject_name 
        FROM subjects 
        WHERE teacher_id = %s
    """, (session['user_id'],))
    subjects = cur.fetchall()
    conn.close()
    return jsonify(subjects)


@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect('/')

    if request.method == 'POST':
        lecture_id = request.form.get('lecture_id', '').strip().upper()
        typed_code = request.form.get('typed_code', '').strip()

        # Basic validation
        if not lecture_id or not typed_code:
            flash('Please enter both lecture ID and 6-digit code.', 'error')
            return render_template('student_dashboard.html')

        if len(typed_code) != 6 or not typed_code.isdigit():
            flash('Code must be exactly 6 digits.', 'error')
            return render_template('student_dashboard.html')

        conn = get_db_connection()
        cur = conn.cursor()

        # Get the latest lecture row for this ID
        cur.execute("""
            SELECT lecture_id, generated_code
            FROM lectures
            WHERE UPPER(lecture_id) = %s
            ORDER BY lecture_datetime DESC
            LIMIT 1
        """, (lecture_id,))
        lecture = cur.fetchone()

        if not lecture:
            conn.close()
            flash(f'Lecture "{lecture_id}" not found.', 'error')
            return render_template('student_dashboard.html')

        db_code = lecture['generated_code'].strip()
        is_present = 1 if typed_code == db_code else 0

        # Save attendance
        blur_detected = 1 if request.form.get('blur_detected') == '1' else 0

        cur.execute("""
            INSERT INTO attendance
            (lecture_id, student_id, typed_code, is_present, blur_detected, submitted_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (lecture_id, session['user_id'], typed_code, is_present, blur_detected))

        conn.commit()
        conn.close()

        if is_present:
            flash('Submitted successfully! You are marked PRESENT.', 'success')
        else:
            flash('Wrong code for this lecture.', 'error')

        return render_template('student_dashboard.html')

    # GET
    return render_template('student_dashboard.html')



@app.route('/student_submission', methods=['GET', 'POST'])
def student_submission():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect('/')
    
    # ✅ PRESERVE lecture_id during submission
    lecture_id = request.form.get('lecture_id') or session.get('lecture_id')
    if not lecture_id:
        return redirect('/student_dashboard')
    
    if request.method == 'POST':
        typed_code = request.form.get('typed_code', '').strip()
        if not typed_code or len(typed_code) != 6:
            # Show error on SAME page, don't redirect
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT generated_code FROM lectures WHERE lecture_id=%s ORDER BY lecture_datetime DESC LIMIT 1", (lecture_id,))
            lecture = cur.fetchone()
            conn.close()
            return render_template('student_submission.html', 
                                 lecture_id=lecture_id, 
                                 code=lecture['generated_code'] if lecture else None,
                                 error="Enter valid 6-digit code!")
        
        # ✅ SAVE ATTENDANCE
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT generated_code FROM lectures WHERE lecture_id=%s ORDER BY lecture_datetime DESC LIMIT 1", (lecture_id,))
        lecture = cur.fetchone()
        
        is_present = 1 if lecture and typed_code == lecture['generated_code'] else 0
        
        cur.execute("""
            INSERT INTO attendance (lecture_id, student_id, typed_code, is_present, blur_detected, submitted_at) 
            VALUES (%s, %s, %s, %s, 0, NOW())
        """, (lecture_id, session['user_id'], typed_code, is_present))
        conn.commit()
        conn.close()
        
        # ✅ SHOW SUCCESS ON RESULT PAGE - NO session clear!
        return render_template('submission_result.html', 
                             status="✅ Submitted successfully!" if is_present else "❌ Wrong code!", 
                             is_present=is_present,
                             lecture_id=lecture_id)
    
    # GET request - show timer page
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT generated_code FROM lectures WHERE lecture_id=%s ORDER BY lecture_datetime DESC LIMIT 1", (lecture_id,))
    lecture = cur.fetchone()
    conn.close()
    
    return render_template('student_submission.html', 
                         lecture_id=lecture_id, 
                         code=lecture['generated_code'] if lecture else None)


@app.route('/submission_result')
def submission_result():
    status = request.args.get('status', 'Processed')
    is_present = request.args.get('is_present', '0') == '1'
    return render_template('submission_result.html', status=status, is_present=is_present)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
