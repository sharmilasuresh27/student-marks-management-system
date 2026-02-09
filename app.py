from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'school_management_2024_secure_key'

def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    c = conn.cursor()
    
    # Create teachers table
    c.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            assigned_class TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create attendance table
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date DATE NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('PRESENT', 'ABSENT', 'LATE')),
            remarks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    """)
    
    # Drop and recreate students table with new schema
    c.execute("DROP TABLE IF EXISTS students")
    c.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            class_teacher TEXT NOT NULL,
            tamil INTEGER,
            english INTEGER,
            maths INTEGER,
            science INTEGER,
            social INTEGER,
            total INTEGER,
            average REAL,
            grade TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert default teachers
    teachers = [
        ('Mrs. Priya Sharma', 'priya123', 'A'),
        ('Mr. Rajesh Kumar', 'rajesh123', 'B'),
        ('Ms. Ananya Patel', 'ananya123', 'C')
    ]
    
    c.execute("DELETE FROM teachers")
    c.executemany("INSERT INTO teachers (name, password, assigned_class) VALUES (?, ?, ?)", teachers)
    
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

create_tables()

# Auto-populate database with sample data on startup
def auto_populate_data():
    conn = get_db()
    c = conn.cursor()
    
    # Check if data already exists
    c.execute("SELECT COUNT(*) as count FROM students")
    result = c.fetchone()
    
    if result['count'] == 0:
        print("🎓 Auto-populating database with sample students...")
        
        # Sample student names for realism
        student_names = {
            'A': [
                "Arjun Kumar", "Priya Sharma", "Rahul Verma", "Anjali Patel", "Vikram Singh",
                "Kavya Reddy", "Rohit Gupta", "Neha Joshi", "Amit Mishra", "Sneha Choudhary",
                "Karan Malhotra", "Divya Nair", "Rajat Kapoor", "Meera Iyer", "Pavan Kumar"
            ],
            'B': [
                "Sanjay Rao", "Lakshmi Menon", "Mohan Das", "Rekha Singh", "Vijay Kumar",
                "Anita Sharma", "Suresh Babu", "Geeta Devi", "Manoj Tiwari", "Pooja Yadav",
                "Deepak Reddy", "Shanti Devi", "Ramesh Patel", "Usha Kumari", "Ajay Singh"
            ],
            'C': [
                "Madhavi Nair", "Krishnan Iyer", "Swati Joshi", "Naveen Kumar", "Anjali Desai",
                "Rohit Sharma", "Kavita Malhotra", "Sunil Gupta", "Rashmi Verma", "Pankaj Kapoor",
                "Meena Singh", "Vikas Rao", "Sunita Devi", "Arvind Kumar", "Chandrika Patel"
            ]
        }
        
        teacher_names = {
            'A': 'Mrs. Priya Sharma',
            'B': 'Mr. Rajesh Kumar', 
            'C': 'Ms. Ananya Patel'
        }
        
        # Generate sample students for each class
        for class_name in ['A', 'B', 'C']:
            num_students = random.randint(15, 20)
            selected_names = random.sample(student_names[class_name], min(num_students, len(student_names[class_name])))
            
            for i, name in enumerate(selected_names):
                # Generate realistic marks with some variation
                marks = []
                for _ in range(5):  # 5 subjects
                    # Create a mix of performance levels
                    performance_level = random.choices(
                        ['excellent', 'good', 'average', 'below_average', 'poor'],
                        weights=[0.15, 0.25, 0.30, 0.20, 0.10]
                    )[0]
                    
                    if performance_level == 'excellent':
                        mark = random.randint(85, 100)
                    elif performance_level == 'good':
                        mark = random.randint(70, 84)
                    elif performance_level == 'average':
                        mark = random.randint(50, 69)
                    elif performance_level == 'below_average':
                        mark = random.randint(35, 49)
                    else:  # poor
                        mark = random.randint(20, 34)
                    
                    marks.append(mark)
                
                # Calculate totals and grades
                total = sum(marks)
                average = total / len(marks)
                status = "PASS" if all(m >= 35 for m in marks) else "FAIL"
                
                if average >= 90: grade = "A+"
                elif average >= 80: grade = "A"
                elif average >= 70: grade = "B+"
                elif average >= 60: grade = "B"
                elif average >= 50: grade = "C"
                elif average >= 35: grade = "D"
                else: grade = "F"
                
                # Generate student ID
                year = datetime.now().year
                random_num = random.randint(1000, 9999)
                student_id = f"STD{year}{class_name}{random_num}"
                
                c.execute("""
                    INSERT INTO students (student_id, name, class, class_teacher, 
                                        tamil, english, maths, science, social, 
                                        total, average, grade, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (student_id, name, class_name, teacher_names[class_name],
                      marks[0], marks[1], marks[2], marks[3], marks[4], 
                      total, average, grade, status))
        
        conn.commit()
        conn.close()
        print("✅ Database auto-populated with sample students!")
        
        # Print summary
        conn = get_db()
        c = conn.cursor()
        
        for class_name in ['A', 'B', 'C']:
            c.execute("SELECT COUNT(*) as count, AVG(total) as avg_total FROM students WHERE class = ?", (class_name,))
            result = c.fetchone()
            print(f"   📚 Class {class_name}: {result['count']} students, Avg Total: {result['avg_total']:.1f}")
            
            # Show topper
            c.execute("SELECT name, total FROM students WHERE class = ? ORDER BY total DESC LIMIT 1", (class_name,))
            topper = c.fetchone()
            if topper:
                print(f"   🏆 Class {class_name} Topper: {topper['name']} ({topper['total']} marks)")
        
        # Show school topper
        c.execute("SELECT name, class, total FROM students ORDER BY total DESC LIMIT 1")
        school_topper = c.fetchone()
        if school_topper:
            print(f"   🥇 School Topper: {school_topper['name']} from Class {school_topper['class']} ({school_topper['total']} marks)")
        
        conn.close()
    else:
        print("📊 Database already contains data - skipping auto-population")

# Auto-populate on startup
auto_populate_data()

def generate_student_id(student_class):
    year = datetime.now().year
    random_num = random.randint(1000, 9999)
    return f"STD{year}{student_class}{random_num}"

def calculate_grade_and_status(marks):
    total = sum(marks)
    average = total / len(marks)
    status = "PASS" if all(m >= 35 for m in marks) else "FAIL"
    
    if average >= 90: grade = "A+"
    elif average >= 80: grade = "A"
    elif average >= 70: grade = "B+"
    elif average >= 60: grade = "B"
    elif average >= 50: grade = "C"
    elif average >= 35: grade = "D"
    else: grade = "F"
    
    return total, average, grade, status

def get_teacher_class():
    if 'teacher_id' in session:
        conn = get_db()
        teacher = conn.execute("SELECT assigned_class FROM teachers WHERE id = ?", 
                              (session['teacher_id'],)).fetchone()
        conn.close()
        return teacher['assigned_class'] if teacher else None
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        assigned_class = request.form.get('class')
        
        conn = get_db()
        teacher = conn.execute("""
            SELECT * FROM teachers 
            WHERE name = ? AND password = ? AND assigned_class = ?
        """, (username, password, assigned_class)).fetchone()
        conn.close()
        
        if teacher:
            session['teacher_id'] = teacher['id']
            session['teacher_name'] = teacher['name']
            session['teacher_class'] = teacher['assigned_class']
            flash(f'Welcome {teacher["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials! Please check your name, password, and class.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'teacher_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get class statistics
    total_students = conn.execute(
        "SELECT COUNT(*) as count FROM students WHERE class = ?", 
        (teacher_class,)
    ).fetchone()['count']
    
    passed_students = conn.execute(
        "SELECT COUNT(*) as count FROM students WHERE class = ? AND status = 'PASS'", 
        (teacher_class,)
    ).fetchone()['count']
    
    failed_students = total_students - passed_students
    
    # Get perfect attendance students for current month
    from datetime import datetime, date
    today = date.today()
    current_month = today.strftime('%Y-%m')
    
    # Calculate total school days in current month (excluding weekends)
    import calendar
    cal = calendar.monthcalendar(today.year, today.month)
    school_days = 0
    for week in cal:
        for day in week:
            if day != 0 and week.index(day) < 5:  # Monday to Friday (0-4)
                if date(today.year, today.month, day) <= today:
                    school_days += 1
    
    # Get perfect attendance students for this class
    perfect_attendance_count = 0
    if school_days > 0:
        all_students = conn.execute(
            "SELECT id FROM students WHERE class = ?", 
            (teacher_class,)
        ).fetchall()
        
        for student in all_students:
            present_days = conn.execute(
                "SELECT COUNT(*) as count FROM attendance a WHERE a.student_id = ? AND a.status = 'PRESENT' AND strftime('%Y-%m', a.date) = ?", 
                (student['id'], current_month)
            ).fetchone()
            
            if present_days and present_days['count'] == school_days:
                perfect_attendance_count += 1
    
    # Get class topper
    class_topper = conn.execute(
        "SELECT * FROM students WHERE class = ? ORDER BY total DESC LIMIT 1", 
        (teacher_class,)
    ).fetchone()
    
    # Get recent students
    recent_students = conn.execute(
        "SELECT * FROM students WHERE class = ? ORDER BY created_at DESC LIMIT 5", 
        (teacher_class,)
    ).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_students=total_students,
                         passed_students=passed_students,
                         failed_students=failed_students,
                         perfect_attendance_count=perfect_attendance_count,
                         class_topper=class_topper,
                         recent_students=recent_students,
                         teacher_class=teacher_class)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    teacher_class = session.get('teacher_class')
    error = None
    
    if request.method == "POST":
        name = request.form.get("name").strip()
        try:
            marks = [
                int(request.form.get("tamil")),
                int(request.form.get("english")),
                int(request.form.get("maths")),
                int(request.form.get("science")),
                int(request.form.get("social"))
            ]
            
            if not name:
                error = "Student name cannot be empty!"
            elif any(m > 100 or m < 0 for m in marks):
                error = "Marks should be between 0 and 100 only!"
            
            if error:
                students = get_class_students(teacher_class)
                return render_template("index.html", students=students, error=error, teacher_class=teacher_class)
            
            total, average, grade, status = calculate_grade_and_status(marks)
            student_id = generate_student_id(teacher_class)
            
            conn = get_db()
            c = conn.cursor()
            c.execute("""
                INSERT INTO students (student_id, name, class, class_teacher, 
                                    tamil, english, maths, science, social, 
                                    total, average, grade, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, name, teacher_class, session['teacher_name'], 
                  marks[0], marks[1], marks[2], marks[3], marks[4], 
                  total, average, grade, status))
            conn.commit()
            conn.close()
            
            flash(f'Student {name} added successfully!', 'success')
            return redirect(url_for('index'))
            
        except ValueError:
            error = "Please enter valid numbers for marks!"
    
    students = get_class_students(teacher_class)
    return render_template("index.html", students=students, error=error, teacher_class=teacher_class)

def get_class_students(teacher_class):
    conn = get_db()
    students = conn.execute("""
        SELECT *, ROW_NUMBER() OVER (ORDER BY total DESC) as rank 
        FROM students WHERE class = ? 
        ORDER BY total DESC
    """, (teacher_class,)).fetchall()
    conn.close()
    return students

@app.route("/delete/<int:id>")
@login_required
def delete(id):
    teacher_class = session.get('teacher_class')
    conn = get_db()
    student = conn.execute("SELECT class FROM students WHERE id = ?", (id,)).fetchone()
    
    if student and student['class'] == teacher_class:
        conn.execute("DELETE FROM students WHERE id = ?", (id,))
        conn.commit()
        flash('Student deleted successfully!', 'success')
    else:
        flash('You can only delete students from your class!', 'error')
    
    conn.close()
    return redirect(url_for('index'))

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
def edit(id):
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    if request.method == "POST":
        name = request.form.get("name")
        marks = [
            int(request.form.get("tamil")),
            int(request.form.get("english")),
            int(request.form.get("maths")),
            int(request.form.get("science")),
            int(request.form.get("social"))
        ]
        
        total, average, grade, status = calculate_grade_and_status(marks)
        
        conn.execute("""
            UPDATE students SET name=?, tamil=?, english=?, maths=?, science=?, social=?, 
            total=?, average=?, grade=?, status=? WHERE id=? AND class=?
        """, (name, marks[0], marks[1], marks[2], marks[3], marks[4], 
              total, average, grade, status, id, teacher_class))
        conn.commit()
        flash('Student updated successfully!', 'success')
        conn.close()
        return redirect(url_for('index'))

    student = conn.execute("SELECT * FROM students WHERE id = ? AND class = ?", 
                          (id, teacher_class)).fetchone()
    conn.close()
    
    if not student:
        flash('Student not found or access denied!', 'error')
        return redirect(url_for('index'))
    
    return render_template("edit.html", student=student)

@app.route("/class-toppers")
@login_required
def class_toppers():
    conn = get_db()
    toppers = {}
    
    for class_name in ['A', 'B', 'C']:
        topper = conn.execute("""
            SELECT * FROM students 
            WHERE class = ? ORDER BY total DESC LIMIT 1
        """, (class_name,)).fetchone()
        toppers[class_name] = topper
    
    conn.close()
    return render_template("class_toppers.html", toppers=toppers)

@app.route("/school-topper")
@login_required
def school_topper():
    conn = get_db()
    topper = conn.execute("""
        SELECT * FROM students 
        ORDER BY total DESC LIMIT 1
    """).fetchone()
    conn.close()
    return render_template("school_topper.html", topper=topper)

@app.route("/weak-students")
@login_required
def weak_students():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    weak_students = conn.execute("""
        SELECT * FROM students 
        WHERE class = ? AND (status = 'FAIL' OR average < 50)
        ORDER BY average ASC
    """, (teacher_class,)).fetchall()
    
    conn.close()
    return render_template("weak_students.html", weak_students=weak_students, teacher_class=teacher_class)

@app.route("/all-classes")
@login_required
def all_classes():
    conn = get_db()
    all_students = conn.execute("""
        SELECT *, ROW_NUMBER() OVER (PARTITION BY class ORDER BY total DESC) as class_rank,
               ROW_NUMBER() OVER (ORDER BY total DESC) as school_rank
        FROM students 
        ORDER BY class, total DESC
    """).fetchall()
    conn.close()
    return render_template("all_classes.html", students=all_students)

@app.route("/analytics")
@login_required
def analytics():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get performance data for charts
    performance_data = conn.execute("""
        SELECT 
            name,
            total,
            average,
            grade,
            status,
            created_at
        FROM students 
        WHERE class = ?
        ORDER BY total DESC
    """, (teacher_class,)).fetchall()
    
    # Get subject-wise averages
    subject_averages = conn.execute("""
        SELECT 
            AVG(tamil) as tamil_avg,
            AVG(english) as english_avg,
            AVG(maths) as maths_avg,
            AVG(science) as science_avg,
            AVG(social) as social_avg
        FROM students 
        WHERE class = ?
    """, (teacher_class,)).fetchone()
    
    # Get grade distribution
    grade_distribution = conn.execute("""
        SELECT 
            grade,
            COUNT(*) as count
        FROM students 
        WHERE class = ?
        GROUP BY grade
        ORDER BY grade
    """, (teacher_class,)).fetchall()
    
    # Get monthly performance trend
    monthly_trend = conn.execute("""
        SELECT 
            strftime('%Y-%m', created_at) as month,
            AVG(total) as avg_total,
            COUNT(*) as student_count
        FROM students 
        WHERE class = ?
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month DESC
        LIMIT 6
    """, (teacher_class,)).fetchall()
    
    conn.close()
    return render_template("analytics_simple.html", 
                         performance_data=performance_data,
                         subject_averages=subject_averages,
                         grade_distribution=grade_distribution,
                         monthly_trend=monthly_trend,
                         teacher_class=teacher_class)

@app.route("/export-pdf")
@login_required
def export_pdf():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    students = conn.execute("""
        SELECT * FROM students 
        WHERE class = ? 
        ORDER BY total DESC
    """, (teacher_class,)).fetchall()
    conn.close()
    
    # Simple HTML for PDF generation
    html_content = f"""
    <html>
    <head>
        <title>Class {teacher_class} Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .pass {{ color: green; font-weight: bold; }}
            .fail {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Class {teacher_class} Performance Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <table>
            <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Tamil</th>
                <th>English</th>
                <th>Maths</th>
                <th>Science</th>
                <th>Social</th>
                <th>Total</th>
                <th>Average</th>
                <th>Grade</th>
                <th>Status</th>
            </tr>
    """
    
    for student in students:
        status_class = "pass" if student['status'] == 'PASS' else "fail"
        html_content += f"""
            <tr>
                <td>{student['student_id']}</td>
                <td>{student['name']}</td>
                <td>{student['tamil']}</td>
                <td>{student['english']}</td>
                <td>{student['maths']}</td>
                <td>{student['science']}</td>
                <td>{student['social']}</td>
                <td>{student['total']}</td>
                <td>{student['average']:.1f}</td>
                <td>{student['grade']}</td>
                <td class="{status_class}">{student['status']}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    # In a real implementation, you would use a PDF library like ReportLab
    # For now, we'll return it as HTML that can be saved as PDF
    from flask import Response
    return Response(html_content, mimetype='text/html',
                    headers={'Content-Disposition': f'attachment; filename=class_{teacher_class}_report.html'})
    
@app.route("/export-word")
@login_required
def export_word():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    students = conn.execute("""
        SELECT * FROM students 
        WHERE class = ? 
        ORDER BY total DESC
    """, (teacher_class,)).fetchall()
    conn.close()
    
    # Generate HTML that can be opened in Word
    word_content = f"""
    <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
    <head>
        <meta charset="utf-8">
        <title>Class {teacher_class} Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; font-weight: bold; }}
            td {{ border: 1px solid #ddd; padding: 10px; }}
            .pass {{ color: #27ae60; font-weight: bold; }}
            .fail {{ color: #e74c3c; font-weight: bold; }}
            .grade-a {{ color: #8e44ad; font-weight: bold; }}
            .grade-b {{ color: #2980b9; font-weight: bold; }}
            .grade-c {{ color: #f39c12; font-weight: bold; }}
            .grade-d {{ color: #e67e22; font-weight: bold; }}
            .grade-f {{ color: #c0392b; font-weight: bold; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <h1>Class {teacher_class} Performance Report</h1>
        <p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Class Teacher:</strong> {session.get('teacher_name', 'N/A')}</p>
        <p><strong>Total Students:</strong> {len(students)}</p>
        
        <table>
            <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Tamil</th>
                <th>English</th>
                <th>Maths</th>
                <th>Science</th>
                <th>Social</th>
                <th>Total</th>
                <th>Average</th>
                <th>Grade</th>
                <th>Status</th>
            </tr>
    """
    
    for student in students:
        status_class = "pass" if student['status'] == 'PASS' else "fail"
        grade_class = f"grade-{student['grade'][0].lower()}" if student['grade'] else ""
        
        word_content += f"""
            <tr>
                <td>{student['student_id']}</td>
                <td><strong>{student['name']}</strong></td>
                <td>{student['tamil']}</td>
                <td>{student['english']}</td>
                <td>{student['maths']}</td>
                <td>{student['science']}</td>
                <td>{student['social']}</td>
                <td><strong>{student['total']}</strong></td>
                <td>{student['average']:.1f}</td>
                <td class="{grade_class}">{student['grade']}</td>
                <td class="{status_class}">{student['status']}</td>
            </tr>
        """
    
    # Add summary statistics
    passed_count = len([s for s in students if s['status'] == 'PASS'])
    failed_count = len(students) - passed_count
    avg_total = sum(s['total'] for s in students) / len(students) if students else 0
    
    word_content += f"""
        </table>
        
        <h2>Summary Statistics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
            <tr>
                <td>Total Students</td>
                <td>{len(students)}</td>
            </tr>
            <tr>
                <td>Passed Students</td>
                <td class="pass">{passed_count}</td>
            </tr>
            <tr>
                <td>Failed Students</td>
                <td class="fail">{failed_count}</td>
            </tr>
            <tr>
                <td>Pass Percentage</td>
                <td>{(passed_count/len(students)*100):.1f}%</td>
            </tr>
            <tr>
                <td>Average Total Marks</td>
                <td>{avg_total:.1f}</td>
            </tr>
        </table>
        
        <div class="footer">
            <p>This report was generated automatically by the School Management System.</p>
            <p>&copy; 2024 School Management System. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    from flask import Response
    return Response(word_content, mimetype='application/msword',
                    headers={'Content-Disposition': f'attachment; filename=class_{teacher_class}_report.doc'})
    
@app.route("/toggle-theme", methods=['POST'])
@login_required
def toggle_theme():
    theme = request.form.get('theme', 'light')
    session['theme'] = theme
    return {'success': True, 'theme': theme}

@app.route("/bulk-import", methods=['GET', 'POST'])
@login_required
def bulk_import():
    teacher_class = session.get('teacher_class')
    
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            flash('No file selected!', 'error')
            return redirect(url_for('bulk_import'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('bulk_import'))
        
        if file and file.filename.endswith('.csv'):
            try:
                # Read CSV file
                import csv
                import io
                
                stream = io.StringIO(file.stream.read().decode("utf-8"))
                csv_reader = csv.reader(stream)
                
                # Skip header row
                next(csv_reader, None)
                
                conn = get_db()
                c = conn.cursor()
                
                imported_count = 0
                error_count = 0
                
                for row in csv_reader:
                    if len(row) >= 5:  # name + 5 subjects
                        try:
                            name = row[0].strip()
                            marks = [
                                int(row[1].strip()) if len(row) > 1 else 0,  # tamil
                                int(row[2].strip()) if len(row) > 2 else 0,  # english
                                int(row[3].strip()) if len(row) > 3 else 0,  # maths
                                int(row[4].strip()) if len(row) > 4 else 0,  # science
                                int(row[5].strip()) if len(row) > 5 else 0   # social
                            ]
                            
                            # Validate marks
                            if any(m > 100 or m < 0 for m in marks):
                                error_count += 1
                                continue
                            
                            total, average, grade, status = calculate_grade_and_status(marks)
                            student_id = generate_student_id(teacher_class)
                            
                            c.execute("""
                                INSERT INTO students (student_id, name, class, class_teacher, 
                                                    tamil, english, maths, science, social, 
                                                    total, average, grade, status)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (student_id, name, teacher_class, session['teacher_name'], 
                                  marks[0], marks[1], marks[2], marks[3], marks[4], 
                                  total, average, grade, status))
                            imported_count += 1
                            
                        except (ValueError, IndexError) as e:
                            error_count += 1
                            continue
                
                conn.commit()
                conn.close()
                
                if imported_count > 0:
                    flash(f'Successfully imported {imported_count} students! {error_count} rows had errors.', 'success')
                else:
                    flash('No valid students found in CSV file!', 'error')
                    
            except Exception as e:
                flash(f'Error processing CSV file: {str(e)}', 'error')
        else:
            flash('Please upload a CSV file!', 'error')
        
        return render_template("bulk_import.html")

@app.route("/student-profile/<int:id>")
@login_required
def student_profile(id):
    teacher_class = session.get('teacher_class')
    conn = get_db()
    student = conn.execute("""
        SELECT * FROM students 
        WHERE id = ? AND class = ?
    """, (id, teacher_class)).fetchone()
    conn.close()
    
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template("student_profile.html", student=student, teacher_class=teacher_class)

@app.route("/attendance")
@login_required
def attendance():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get selected date from query parameter or use today
    from datetime import date
    attendance_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    
    # Validate date is not in the future
    try:
        selected_date_obj = date.fromisoformat(attendance_date)
        if selected_date_obj > date.today():
            flash('Cannot view attendance for future dates!', 'error')
            attendance_date = date.today().strftime('%Y-%m-%d')
    except ValueError:
        flash('Invalid date format!', 'error')
        attendance_date = date.today().strftime('%Y-%m-%d')
    
    # Get all students for the class
    students = conn.execute("""
        SELECT * FROM students 
        WHERE class = ? 
        ORDER BY name
    """, (teacher_class,)).fetchall()
    
    # Get attendance records for the selected date
    attendance_records = {}
    for student in students:
        attendance = conn.execute("""
            SELECT status, remarks FROM attendance 
            WHERE student_id = ? AND date = ?
        """, (student['id'], attendance_date)).fetchone()
        
        attendance_records[student['id']] = {
            'status': attendance['status'] if attendance else 'PRESENT',
            'remarks': attendance['remarks'] if attendance else ''
        }
    
    # Calculate statistics for the selected date
    present_count = sum(1 for record in attendance_records.values() if record['status'] == 'PRESENT')
    absent_count = sum(1 for record in attendance_records.values() if record['status'] == 'ABSENT')
    late_count = sum(1 for record in attendance_records.values() if record['status'] == 'LATE')
    
    conn.close()
    return render_template("attendance.html", 
                     students=students, 
                     attendance_records=attendance_records,
                     today=attendance_date,
                     present_count=present_count,
                     absent_count=absent_count,
                     late_count=late_count,
                     teacher_class=teacher_class)

@app.route("/mark-attendance", methods=['POST'])
@login_required
def mark_attendance():
    teacher_class = session.get('teacher_class')
    
    if request.method == 'POST':
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        
        conn = get_db()
        c = conn.cursor()
        
        # Get form data
        attendance_data = request.form.to_dict()
        
        marked_count = 0
        for key, value in attendance_data.items():
            if key.startswith('attendance_'):
                student_id = key.split('_')[1]
                status = value
                remarks = request.form.get(f'remarks_{student_id}', '')
                
                # Check if attendance already exists
                existing = c.execute("""
                    SELECT id FROM attendance 
                    WHERE student_id = ? AND date = ?
                """, (student_id, today)).fetchone()
                
                if existing:
                    # Update existing record
                    c.execute("""
                        UPDATE attendance 
                        SET status = ?, remarks = ? 
                        WHERE student_id = ? AND date = ?
                    """, (status, remarks, student_id, today))
                else:
                    # Insert new record
                    c.execute("""
                        INSERT INTO attendance (student_id, date, status, remarks)
                        VALUES (?, ?, ?, ?)
                    """, (student_id, today, status, remarks))
                
                marked_count += 1
        
        conn.commit()
        conn.close()
        
        if marked_count > 0:
            flash(f'Successfully marked attendance for {marked_count} students!', 'success')
        else:
            flash('No attendance data received!', 'error')
    
    return redirect(url_for('attendance'))

@app.route("/attendance-report")
@login_required
def attendance_report():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get attendance summary for the last 30 days
    attendance_summary = conn.execute(
        "SELECT s.name, s.student_id, COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) as present_days, COUNT(CASE WHEN a.status = 'ABSENT' THEN 1 END) as absent_days, COUNT(CASE WHEN a.status = 'LATE' THEN 1 END) as late_days, COUNT(*) as total_days FROM students s LEFT JOIN attendance a ON s.id = a.student_id WHERE s.class = ? AND a.date >= date('now', '-30 days') GROUP BY s.id, s.name ORDER BY s.name", 
        (teacher_class,)
    ).fetchall()
    
    conn.close()
    return render_template("attendance_report.html", 
                         attendance_summary=attendance_summary,
                         teacher_class=teacher_class)

@app.route("/attendance-calendar")
@login_required
def attendance_calendar():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get current month and year
    from datetime import datetime, date
    today = date.today()
    current_month = today.strftime('%Y-%m')
    
    # Get attendance data for the current month
    attendance_data = conn.execute(
        "SELECT s.name, s.student_id, a.date, a.status FROM students s LEFT JOIN attendance a ON s.id = a.student_id WHERE s.class = ? AND strftime('%Y-%m', a.date) = ? ORDER BY s.name, a.date", 
        (teacher_class, current_month)
    ).fetchall()
    
    # Get calendar data
    calendar_data = {}
    for student in conn.execute("SELECT * FROM students WHERE class = ? ORDER BY name", (teacher_class,)).fetchall():
        calendar_data[student['id']] = {
            'name': student['name'],
            'student_id': student['student_id'],
            'attendance': {}
        }
        
        # Fill attendance for each day of the month
        for day in range(1, 32):
            try:
                day_date = date(today.year, today.month, day)
                if day_date.strftime('%Y-%m-%d') <= today.strftime('%Y-%m-%d'):
                    for record in attendance_data:
                        if record['student_id'] == student['id'] and record['date'] == day_date.strftime('%Y-%m-%d'):
                            calendar_data[student['id']]['attendance'][day] = record['status']
                            break
            except ValueError:
                # Skip invalid dates (like February 30th)
                break
    
    conn.close()
    return render_template("attendance_calendar.html", 
                         calendar_data=calendar_data,
                         current_month=current_month,
                         teacher_class=teacher_class)

@app.route("/perfect-attendance")
@login_required
def perfect_attendance():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get students with 100% attendance for the current month across all classes
    from datetime import datetime, date
    today = date.today()
    current_month = today.strftime('%Y-%m')
    
    # Calculate total school days in current month (excluding weekends)
    import calendar
    cal = calendar.monthcalendar(today.year, today.month)
    school_days = 0
    for week in cal:
        for day in week:
            if day != 0 and week.index(day) < 5:  # Monday to Friday (0-4)
                if date(today.year, today.month, day) <= today:
                    school_days += 1
    
    # Get all students from all classes and their attendance
    all_students = conn.execute(
        "SELECT s.id, s.name, s.student_id, s.class FROM students s ORDER BY s.class, s.name"
    ).fetchall()
    
    perfect_attendance_students = []
    for student in all_students:
        # Count present days for this student
        present_days = conn.execute(
            "SELECT COUNT(*) as count FROM attendance a WHERE a.student_id = ? AND a.status = 'PRESENT' AND strftime('%Y-%m', a.date) = ?", 
            (student['id'], current_month)
        ).fetchone()
        
        if present_days and present_days['count'] == school_days:
            perfect_attendance_students.append({
                'name': student['name'],
                'student_id': student['student_id'],
                'class': student['class'],
                'attended_days': present_days['count'],
                'total_school_days': school_days,
                'attendance_percentage': 100.0
            })
    
    conn.close()
    return render_template("perfect_attendance.html", 
                         perfect_attendance_students=perfect_attendance_students,
                         current_month=current_month,
                         school_days=school_days,
                         teacher_class=teacher_class)

@app.route("/attendance-analytics")
@login_required
def attendance_analytics():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    from datetime import date, datetime, timedelta
    today = date.today()
    
    # Calculate comprehensive analytics
    analytics = {}
    
    # Total students
    analytics['total_students'] = conn.execute(
        "SELECT COUNT(*) as count FROM students WHERE class = ?", 
        (teacher_class,)
    ).fetchone()['count']
    
    # Today's attendance
    today_str = today.strftime('%Y-%m-%d')
    today_attendance = conn.execute(
        "SELECT status, COUNT(*) as count FROM attendance a "
        "JOIN students s ON a.student_id = s.id "
        "WHERE s.class = ? AND a.date = ? "
        "GROUP BY status", 
        (teacher_class, today_str)
    ).fetchall()
    
    attendance_status = {row['status']: row['count'] for row in today_attendance}
    analytics['present_today'] = attendance_status.get('PRESENT', 0)
    analytics['absent_today'] = attendance_status.get('ABSENT', 0)
    analytics['late_today'] = attendance_status.get('LATE', 0)
    
    # Overall attendance rate (last 30 days)
    attendance_rate = conn.execute(
        "SELECT "
        "CASE "
        "WHEN COUNT(*) > 0 THEN "
        "ROUND((COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*)), 1) "
        "ELSE 0 "
        "END as rate "
        "FROM attendance a "
        "JOIN students s ON a.student_id = s.id "
        "WHERE s.class = ? AND a.date >= date('now', '-30 days')", 
        (teacher_class,)
    ).fetchone()
    analytics['attendance_rate'] = attendance_rate['rate'] if attendance_rate else 0
    
    # Perfect attendance students
    current_month = today.strftime('%Y-%m')
    import calendar
    cal = calendar.monthcalendar(today.year, today.month)
    school_days = sum(1 for week in cal for day in week 
                     if day != 0 and week.index(day) < 5 and date(today.year, today.month, day) <= today)
    
    perfect_attendance = 0
    if school_days > 0:
        students = conn.execute("SELECT id FROM students WHERE class = ?", (teacher_class,)).fetchall()
        for student in students:
            present_days = conn.execute(
                "SELECT COUNT(*) as count FROM attendance WHERE student_id = ? AND status = 'PRESENT' AND strftime('%Y-%m', date) = ?", 
                (student['id'], current_month)
            ).fetchone()
            if present_days and present_days['count'] == school_days:
                perfect_attendance += 1
    
    analytics['perfect_attendance'] = perfect_attendance
    
    # Average daily attendance
    avg_daily = conn.execute(
        "SELECT AVG(daily_count) as avg_count FROM ("
        "SELECT COUNT(*) as daily_count "
        "FROM attendance a "
        "JOIN students s ON a.student_id = s.id "
        "WHERE s.class = ? AND a.date >= date('now', '-30 days') "
        "GROUP BY a.date"
        ")",
        (teacher_class,)
    ).fetchone()
    analytics['avg_daily_attendance'] = round(avg_daily['avg_count'], 1) if avg_daily and avg_daily['avg_count'] else 0
    
    # Monthly trend data (last 6 months)
    monthly_data = []
    monthly_labels = []
    for i in range(5, -1, -1):
        month_date = today.replace(day=1) - timedelta(days=30*i)
        month_str = month_date.strftime('%Y-%m')
        month_label = month_date.strftime('%b %Y')
        
        # Simplified monthly rate calculation
        month_rate = conn.execute(
            "SELECT COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*) as rate "
            "FROM attendance a "
            "JOIN students s ON a.student_id = s.id "
            "WHERE s.class = ? AND strftime('%Y-%m', a.date) = ?",
            (teacher_class, month_str)
        ).fetchone()
        
        monthly_data.append(month_rate['rate'] if month_rate and month_rate['rate'] else 0)
        monthly_labels.append(month_label)
    
    analytics['monthly_data'] = monthly_data
    analytics['monthly_labels'] = monthly_labels
    
    # Attendance distribution
    analytics['distribution'] = [
        analytics['present_today'],
        analytics['absent_today'], 
        analytics['late_today']
    ]
    
    # Weekly pattern (simplified)
    weekly_pattern = []
    for i in range(5):  # Monday to Friday
        day_pattern = conn.execute(
            "SELECT COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*) as rate "
            "FROM attendance a "
            "JOIN students s ON a.student_id = s.id "
            "WHERE s.class = ? AND a.date >= date('now', '-30 days') "
            "AND strftime('%w', a.date) = ?",
            (teacher_class, str(i))
        ).fetchone()
        
        weekly_pattern.append(day_pattern['rate'] if day_pattern and day_pattern['rate'] else 0)
    
    analytics['weekly_pattern'] = weekly_pattern
    
    # Alerts and concerns
    alerts = []
    concern_students = []
    
    # Low attendance rate alert
    if analytics['attendance_rate'] < 75:
        alerts.append({
            'type': 'danger',
            'title': '⚠️ Low Attendance Rate',
            'message': f'Class attendance rate is {analytics["attendance_rate"]}% (below 75%)'
        })
    
    # High absentees alert
    if analytics['absent_today'] > analytics['total_students'] * 0.2:  # More than 20% absent
        alerts.append({
            'type': 'warning',
            'title': '📊 High Absenteeism',
            'message': f'{analytics["absent_today"]} students absent today ({round(analytics["absent_today"]/analytics["total_students"]*100)}%)'
        })
    
    # Students with attendance concerns
    concerned_students = conn.execute(
        "SELECT s.id, s.name, s.student_id, "
        "(SELECT COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*) as attendance_rate "
        "FROM attendance a "
        "WHERE a.student_id = s.id AND a.date >= date('now', '-30 days')) as attendance_rate "
        "FROM students s "
        "WHERE s.class = ? "
        "ORDER BY attendance_rate ASC "
        "LIMIT 5",
        (teacher_class,)
    ).fetchall()
    
    for student in concerned_students:
        concern_students.append({
            'name': student['name'],
            'student_id': student['student_id'],
            'attendance_rate': round(student['attendance_rate'], 1),
            'concern': 'Low attendance rate'
        })
    
    analytics['alerts'] = alerts
    analytics['concern_students'] = concern_students
    
    conn.close()
    return render_template("attendance_analytics.html", analytics=analytics, teacher_class=teacher_class)

@app.route("/attendance-alerts")
@login_required
def attendance_alerts():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    from datetime import date, datetime, timedelta
    today = date.today()
    
    alerts = {}
    
    # Count different types of alerts
    alerts['critical'] = 0
    alerts['warning'] = 0
    alerts['info'] = 0
    alerts['resolved'] = 0
    
    # Generate active alerts based on current attendance situation
    active_alerts = []
    
    # Check for high absenteeism
    today_str = today.strftime('%Y-%m-%d')
    today_attendance = conn.execute("""
        SELECT status, COUNT(*) as count FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE s.class = ? AND a.date = ?
        GROUP BY status
    """, (teacher_class, today_str)).fetchall()
    
    attendance_status = {row['status']: row['count'] for row in today_attendance}
    total_students = conn.execute("SELECT COUNT(*) as count FROM students WHERE class = ?", (teacher_class,)).fetchone()['count']
    
    if total_students > 0:
        absent_rate = (attendance_status.get('ABSENT', 0) / total_students) * 100
        if absent_rate > 20:  # More than 20% absent
            active_alerts.append({
                'id': 1,
                'type': 'critical',
                'severity': 'High',
                'title': '🚨 High Absenteeism Alert',
                'message': f'{attendance_status.get("ABSENT", 0)} students absent today ({absent_rate:.1f}% of class)',
                'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'affected_students': get_absent_students(conn, teacher_class, today_str)
            })
            alerts['critical'] += 1
    
    # Check for students with low attendance
    low_attendance_students = conn.execute("""
        SELECT s.id, s.name, s.student_id,
               (SELECT COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*))
               as attendance_rate
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date >= date('now', '-30 days')
        WHERE s.class = ?
        GROUP BY s.id, s.name, s.student_id
        HAVING attendance_rate < 80 AND attendance_rate > 0
        ORDER BY attendance_rate ASC
        LIMIT 5
    """, (teacher_class,)).fetchall()
    
    if low_attendance_students:
        active_alerts.append({
            'id': 2,
            'type': 'warning',
            'severity': 'Medium',
            'title': '⚠️ Low Attendance Warning',
            'message': f'{len(low_attendance_students)} students have attendance below 80%',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'affected_students': low_attendance_students
        })
        alerts['warning'] += 1
    
    # Check for consecutive absences
    consecutive_absent = conn.execute("""
        SELECT s.id, s.name, s.student_id, COUNT(*) as consecutive_days
        FROM students s
        JOIN attendance a ON s.id = a.student_id
        WHERE s.class = ? AND a.status = 'ABSENT'
        AND a.date >= date('now', '-7 days')
        GROUP BY s.id, s.name, s.student_id
        HAVING consecutive_days >= 3
        ORDER BY consecutive_days DESC
        LIMIT 3
    """, (teacher_class,)).fetchall()
    
    if consecutive_absent:
        active_alerts.append({
            'id': 3,
            'type': 'warning',
            'severity': 'Medium',
            'title': '📅 Consecutive Absences',
            'message': f'{len(consecutive_absent)} students have 3+ consecutive absences',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'affected_students': consecutive_absent
        })
        alerts['warning'] += 1
    
    # Add info alert for perfect attendance
    current_month = today.strftime('%Y-%m')
    import calendar
    cal = calendar.monthcalendar(today.year, today.month)
    school_days = sum(1 for week in cal for day in week 
                     if day != 0 and week.index(day) < 5 and date(today.year, today.month, day) <= today)
    
    perfect_attendance = 0
    if school_days > 0:
        students = conn.execute("SELECT id FROM students WHERE class = ?", (teacher_class,)).fetchall()
        for student in students:
            present_days = conn.execute(
                "SELECT COUNT(*) as count FROM attendance WHERE student_id = ? AND status = 'PRESENT' AND strftime('%Y-%m', date) = ?", 
                (student['id'], current_month)
            ).fetchone()
            if present_days and present_days['count'] == school_days:
                perfect_attendance += 1
    
    if perfect_attendance > 0:
        active_alerts.append({
            'id': 4,
            'type': 'info',
            'severity': 'Low',
            'title': '🏆 Perfect Attendance',
            'message': f'{perfect_attendance} students have 100% attendance this month!',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'affected_students': []
        })
        alerts['info'] += 1
    
    alerts['active_alerts'] = active_alerts
    
    # Recent alert history (mock data for demonstration)
    alerts['recent_alerts'] = [
        {
            'type': 'warning',
            'status': 'resolved',
            'title': 'Low Attendance Warning',
            'message': '5 students had attendance below 80%',
            'time': '2026-02-08 14:30',
            'resolved_by': 'Auto-resolved'
        },
        {
            'type': 'critical',
            'status': 'resolved',
            'title': 'High Absenteeism Alert',
            'message': '8 students absent (26.7% of class)',
            'time': '2026-02-08 09:15',
            'resolved_by': 'Teacher Action'
        }
    ]
    
    # Mock settings (in real app, these would be stored in database)
    alerts['settings'] = {
        'alert_absent_threshold': True,
        'alert_low_attendance': True,
        'alert_consecutive_absent': True,
        'email_notifications': True,
        'daily_summary': False,
        'parent_notifications': True
    }
    
    conn.close()
    return render_template("attendance_alerts.html", alerts=alerts, teacher_class=teacher_class)

def get_absent_students(conn, teacher_class, date_str):
    """Helper function to get absent students for a specific date"""
    return conn.execute("""
        SELECT s.id, s.name, s.student_id,
               (SELECT COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*))
               as attendance_rate
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date >= date('now', '-30 days')
        WHERE s.class = ? AND s.id IN (
            SELECT student_id FROM attendance WHERE date = ? AND status = 'ABSENT'
        )
        GROUP BY s.id, s.name, s.student_id
    """, (teacher_class, date_str)).fetchall()

if __name__ == "__main__":
    app.run(debug=True)