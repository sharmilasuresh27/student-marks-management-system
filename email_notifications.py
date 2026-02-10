"""
Email Notification System for School Management
Add to requirements.txt: Flask-Mail==0.9.1
"""

from flask_mail import Mail, Message
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotificationSystem:
    def __init__(self, app=None):
        self.mail = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize email configuration"""
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
        app.config['MAIL_PASSWORD'] = 'your-app-password'
        app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'
        
        self.mail = Mail(app)
    
    def send_attendance_alert(self, parent_email, student_name, status, date):
        """Send attendance notification to parents"""
        subject = f"Attendance Alert - {student_name}"
        
        if status == 'ABSENT':
            body = f"""
            Dear Parent,
            
            Your child {student_name} was marked absent on {date}.
            
            Please contact the school if this is incorrect.
            
            Best regards,
            School Management System
            """
        elif status == 'LATE':
            body = f"""
            Dear Parent,
            
            Your child {student_name} was marked late on {date}.
            
            Please ensure timely arrival in future.
            
            Best regards,
            School Management System
            """
        
        return self._send_email(parent_email, subject, body)
    
    def send_performance_report(self, parent_email, student_name, marks, grade):
        """Send performance report to parents"""
        subject = f"Performance Report - {student_name}"
        
        body = f"""
        Dear Parent,
        
        Performance Report for {student_name}:
        
        Total Marks: {marks.get('total', 0)}
        Average: {marks.get('average', 0):.1f}
        Grade: {grade}
        Status: {'PASS' if grade != 'F' else 'FAIL'}
        
        Subject-wise Performance:
        Tamil: {marks.get('tamil', 0)}
        English: {marks.get('english', 0)}
        Maths: {marks.get('maths', 0)}
        Science: {marks.get('science', 0)}
        Social Science: {marks.get('social', 0)}
        
        Please contact the teachers for any concerns.
        
        Best regards,
        School Management System
        """
        
        return self._send_email(parent_email, subject, body)
    
    def send_weekly_summary(self, teacher_email, class_name, stats):
        """Send weekly summary to teachers"""
        subject = f"Weekly Summary - Class {class_name}"
        
        body = f"""
        Dear Teacher,
        
        Weekly Summary for Class {class_name}:
        
        Total Students: {stats.get('total_students', 0)}
        Average Attendance: {stats.get('avg_attendance', 0):.1f}%
        Average Performance: {stats.get('avg_performance', 0):.1f}
        
        Top Performers:
        {stats.get('toppers', 'No data available')}
        
        Students Needing Attention:
        {stats.get('weak_students', 'No data available')}
        
        Best regards,
        School Management System
        """
        
        return self._send_email(teacher_email, subject, body)
    
    def _send_email(self, recipient, subject, body):
        """Send email using Flask-Mail"""
        try:
            msg = Message(
                subject=subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[recipient]
            )
            msg.body = body
            
            self.mail.send(msg)
            return True, "Email sent successfully"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

# Integration with Flask App
def setup_email_notifications(app):
    """Setup email notifications in Flask app"""
    email_system = EmailNotificationSystem(app)
    app.email_system = email_system
    return email_system
