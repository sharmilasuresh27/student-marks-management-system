"""
RESTful API Endpoints for Mobile App Integration
Add to requirements.txt: Flask-CORS==4.0.0
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime, date

class MobileAPI:
    def __init__(self, app):
        self.app = app
        self.setup_cors()
        self.setup_routes()
    
    def setup_cors(self):
        """Setup CORS for mobile app access"""
        CORS(self.app, resources={
            r"/api/*": {
                "origins": ["*"],
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/students', methods=['GET'])
        def get_students():
            """Get all students for a class"""
            teacher_class = request.args.get('class')
            if not teacher_class:
                return jsonify({'error': 'Class parameter required'}), 400
            
            try:
                conn = sqlite3.connect('students.db')
                conn.row_factory = sqlite3.Row
                students = conn.execute(
                    "SELECT * FROM students WHERE class = ? ORDER BY name", 
                    (teacher_class,)
                ).fetchall()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'data': [dict(student) for student in students],
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/student/<student_id>', methods=['GET'])
        def get_student(student_id):
            """Get specific student details"""
            try:
                conn = sqlite3.connect('students.db')
                conn.row_factory = sqlite3.Row
                student = conn.execute(
                    "SELECT * FROM students WHERE student_id = ?", 
                    (student_id,)
                ).fetchone()
                conn.close()
                
                if student:
                    return jsonify({
                        'success': True,
                        'data': dict(student)
                    })
                else:
                    return jsonify({'error': 'Student not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/attendance', methods=['GET'])
        def get_attendance():
            """Get attendance data"""
            teacher_class = request.args.get('class')
            date_filter = request.args.get('date')
            
            if not teacher_class:
                return jsonify({'error': 'Class parameter required'}), 400
            
            try:
                conn = sqlite3.connect('students.db')
                conn.row_factory = sqlite3.Row
                
                query = """
                    SELECT s.student_id, s.name, a.date, a.status, a.remarks
                    FROM students s
                    LEFT JOIN attendance a ON s.id = a.student_id
                    WHERE s.class = ?
                """
                params = [teacher_class]
                
                if date_filter:
                    query += " AND a.date = ?"
                    params.append(date_filter)
                
                query += " ORDER BY s.name, a.date"
                
                attendance = conn.execute(query, params).fetchall()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'data': [dict(record) for record in attendance],
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/attendance', methods=['POST'])
        def mark_attendance():
            """Mark attendance via API"""
            data = request.get_json()
            
            if not data or 'student_id' not in data or 'status' not in data:
                return jsonify({'error': 'Missing required fields'}), 400
            
            try:
                conn = sqlite3.connect('students.db')
                cursor = conn.cursor()
                
                # Check if attendance already exists
                existing = cursor.execute(
                    "SELECT id FROM attendance WHERE student_id = ? AND date = ?",
                    (data['student_id'], data.get('date', date.today().strftime('%Y-%m-%d')))
                ).fetchone()
                
                if existing:
                    # Update existing
                    cursor.execute(
                        "UPDATE attendance SET status = ?, remarks = ? WHERE student_id = ? AND date = ?",
                        (data['status'], data.get('remarks', ''), data['student_id'], data.get('date', date.today().strftime('%Y-%m-%d')))
                    )
                else:
                    # Insert new
                    cursor.execute(
                        "INSERT INTO attendance (student_id, date, status, remarks) VALUES (?, ?, ?, ?)",
                        (data['student_id'], data.get('date', date.today().strftime('%Y-%m-%d')), data['status'], data.get('remarks', ''))
                    )
                
                conn.commit()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'message': 'Attendance marked successfully',
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/analytics', methods=['GET'])
        def get_analytics():
            """Get class analytics"""
            teacher_class = request.args.get('class')
            
            if not teacher_class:
                return jsonify({'error': 'Class parameter required'}), 400
            
            try:
                conn = sqlite3.connect('students.db')
                conn.row_factory = sqlite3.Row
                
                # Basic stats
                total_students = conn.execute(
                    "SELECT COUNT(*) as count FROM students WHERE class = ?", 
                    (teacher_class,)
                ).fetchone()['count']
                
                # Performance stats
                performance = conn.execute("""
                    SELECT 
                        AVG(total) as avg_total,
                        MAX(total) as max_total,
                        MIN(total) as min_total,
                        COUNT(CASE WHEN grade != 'F' THEN 1 END) as pass_count,
                        COUNT(*) as total_count
                    FROM students WHERE class = ?
                """, (teacher_class,)).fetchone()
                
                # Attendance stats (last 30 days)
                attendance_stats = conn.execute("""
                    SELECT 
                        COUNT(CASE WHEN a.status = 'PRESENT' THEN 1 END) * 100.0 / COUNT(*) as attendance_rate
                    FROM attendance a
                    JOIN students s ON a.student_id = s.id
                    WHERE s.class = ? AND a.date >= date('now', '-30 days')
                """, (teacher_class,)).fetchone()
                
                conn.close()
                
                analytics = {
                    'total_students': total_students,
                    'average_total': round(performance['avg_total'], 1) if performance['avg_total'] else 0,
                    'highest_score': performance['max_total'] or 0,
                    'lowest_score': performance['min_total'] or 0,
                    'pass_percentage': round((performance['pass_count'] / performance['total_count'] * 100), 1) if performance['total_count'] else 0,
                    'attendance_rate': round(attendance_stats['attendance_rate'], 1) if attendance_stats['attendance_rate'] else 0,
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify({
                    'success': True,
                    'data': analytics
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/notifications', methods=['GET'])
        def get_notifications():
            """Get notifications for mobile app"""
            teacher_class = request.args.get('class')
            
            if not teacher_class:
                return jsonify({'error': 'Class parameter required'}), 400
            
            try:
                # Mock notifications (in real app, these would come from database)
                notifications = [
                    {
                        'id': 1,
                        'type': 'attendance',
                        'title': 'Low Attendance Alert',
                        'message': '3 students have attendance below 80%',
                        'timestamp': datetime.now().isoformat(),
                        'read': False
                    },
                    {
                        'id': 2,
                        'type': 'performance',
                        'title': 'Performance Update',
                        'message': 'Weekly performance report is ready',
                        'timestamp': datetime.now().isoformat(),
                        'read': False
                    }
                ]
                
                return jsonify({
                    'success': True,
                    'data': notifications
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500

# Integration helper
def setup_mobile_api(app):
    """Setup mobile API endpoints"""
    return MobileAPI(app)
