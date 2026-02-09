# This is a backup of the fixed attendance calendar code
# The main issue was in the attendance_calendar function where we need to handle invalid dates

# Fixed code for attendance_calendar function:
def attendance_calendar():
    teacher_class = session.get('teacher_class')
    conn = get_db()
    
    # Get current month and year
    from datetime import datetime, date
    today = date.today()
    current_month = today.strftime('%Y-%m')
    
    # Get attendance data for the current month
    attendance_data = conn.execute("""
        SELECT 
            s.name,
            s.student_id,
            a.date,
            a.status,
            COUNT(*) as total_records
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id 
        WHERE s.class = ? AND strftime('%Y-%m', a.date) = ?
        GROUP BY s.id, s.name, a.date, a.status
        ORDER BY s.name, a.date
    """, (teacher_class, current_month)).fetchall()
    
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
