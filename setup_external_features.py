"""
Setup Script for External Features
This script helps integrate all external features into the main application
"""

def setup_email_integration(app):
    """Setup email notifications"""
    try:
        from email_notifications import setup_email_notifications
        email_system = setup_email_notifications(app)
        print("✅ Email notifications setup complete")
        return email_system
    except ImportError:
        print("⚠️  Flask-Mail not installed. Run: pip install Flask-Mail==0.9.1")
        return None

def setup_pdf_integration(app):
    """Setup PDF report generation"""
    try:
        from pdf_reports import setup_pdf_reports
        pdf_generator = setup_pdf_reports()
        print("✅ PDF reports setup complete")
        return pdf_generator
    except ImportError:
        print("⚠️  ReportLab not installed. Run: pip install ReportLab==4.0.4")
        return None

def setup_api_integration(app):
    """Setup mobile API endpoints"""
    try:
        from api_endpoints import setup_mobile_api
        mobile_api = setup_mobile_api(app)
        print("✅ Mobile API setup complete")
        return mobile_api
    except ImportError:
        print("⚠️  Flask-CORS not installed. Run: pip install Flask-CORS==4.0.0")
        return None

def setup_analytics_integration(app):
    """Setup advanced analytics"""
    try:
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        print("✅ Advanced analytics setup complete")
        return True
    except ImportError:
        print("⚠️  Pandas/Scikit-learn not installed. Run: pip install pandas scikit-learn")
        return False

def integrate_all_features(app):
    """Integrate all external features"""
    print("🚀 Setting up external features...")
    
    # Setup email notifications
    email_system = setup_email_integration(app)
    
    # Setup PDF reports
    pdf_generator = setup_pdf_integration(app)
    
    # Setup mobile API
    mobile_api = setup_api_integration(app)
    
    # Setup advanced analytics
    analytics_ready = setup_analytics_integration(app)
    
    # Add new routes for external features
    add_external_routes(app, email_system, pdf_generator)
    
    print("🎉 External features integration complete!")
    return {
        'email_system': email_system,
        'pdf_generator': pdf_generator,
        'mobile_api': mobile_api,
        'analytics_ready': analytics_ready
    }

def add_external_routes(app, email_system, pdf_generator):
    """Add new routes for external features"""
    
    @app.route('/reports/student/<student_id>')
    def generate_student_report(student_id):
        """Generate PDF report for student"""
        if not pdf_generator:
            return "PDF generation not available", 503
        
        try:
            import sqlite3
            conn = sqlite3.connect('students.db')
            conn.row_factory = sqlite3.Row
            student = conn.execute(
                "SELECT * FROM students WHERE student_id = ?", 
                (student_id,)
            ).fetchone()
            conn.close()
            
            if student:
                filename = f"report_{student_id}.pdf"
                output_path = f"static/{filename}"
                
                success = pdf_generator.generate_student_report(dict(student), output_path)
                if success:
                    return f"/static/{filename}"
                else:
                    return "Report generation failed", 500
            else:
                return "Student not found", 404
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    @app.route('/reports/class/<class_name>')
    def generate_class_report(class_name):
        """Generate PDF report for class"""
        if not pdf_generator:
            return "PDF generation not available", 503
        
        try:
            import sqlite3
            conn = sqlite3.connect('students.db')
            conn.row_factory = sqlite3.Row
            
            # Get class statistics
            students = conn.execute(
                "SELECT * FROM students WHERE class = ? ORDER BY total DESC", 
                (class_name,)
            ).fetchall()
            
            # Calculate class statistics
            total_students = len(students)
            if total_students > 0:
                totals = [s['total'] for s in students]
                class_average = sum(totals) / total_students
                highest_score = max(totals)
                lowest_score = min(totals)
                pass_count = sum(1 for s in students if s['grade'] != 'F')
                pass_percentage = (pass_count / total_students) * 100
                
                # Get top 5 performers
                toppers = [dict(s) for s in students[:5]]
            else:
                class_average = highest_score = lowest_score = pass_percentage = 0
                toppers = []
            
            conn.close()
            
            class_data = {
                'class_name': class_name,
                'total_students': total_students,
                'class_average': class_average,
                'highest_score': highest_score,
                'lowest_score': lowest_score,
                'pass_percentage': pass_percentage,
                'toppers': toppers
            }
            
            filename = f"class_report_{class_name}.pdf"
            output_path = f"static/{filename}"
            
            success = pdf_generator.generate_class_report(class_data, output_path)
            if success:
                return f"/static/{filename}"
            else:
                return "Report generation failed", 500
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    @app.route('/send-notification', methods=['POST'])
    def send_notification():
        """Send email notification"""
        if not email_system:
            return "Email system not available", 503
        
        try:
            data = request.get_json()
            notification_type = data.get('type')
            recipient = data.get('recipient')
            student_data = data.get('student_data', {})
            
            if notification_type == 'attendance':
                success, message = email_system.send_attendance_alert(
                    recipient, 
                    student_data.get('name', ''),
                    student_data.get('status', ''),
                    student_data.get('date', '')
                )
            elif notification_type == 'performance':
                success, message = email_system.send_performance_report(
                    recipient,
                    student_data.get('name', ''),
                    student_data.get('marks', {}),
                    student_data.get('grade', '')
                )
            else:
                return "Invalid notification type", 400
            
            if success:
                return jsonify({'success': True, 'message': message})
            else:
                return jsonify({'success': False, 'error': message}), 500
        except Exception as e:
            return f"Error: {str(e)}", 500

# Installation guide
def print_installation_guide():
    """Print installation guide for external features"""
    print("""
🚀 EXTERNAL FEATURES INSTALLATION GUIDE
=====================================

1. INSTALL REQUIRED PACKAGES:
   pip install -r requirements.txt

2. SETUP INSTRUCTIONS:
   Add this to your app.py:

   from setup_external_features import integrate_all_features
   
   # After app initialization
   app = Flask(__name__)
   features = integrate_all_features(app)

3. AVAILABLE FEATURES:
   ✅ Email Notifications (Flask-Mail)
   ✅ PDF Reports (ReportLab)
   ✅ Mobile API (Flask-CORS)
   ✅ Advanced Analytics (Pandas, Scikit-learn)

4. NEW ENDPOINTS:
   📧 /send-notification - Send email notifications
   📊 /reports/student/<id> - Generate student PDF report
   📈 /reports/class/<class> - Generate class PDF report
   📱 /api/* - Mobile app endpoints

5. CONFIGURATION:
   - Update email settings in email_notifications.py
   - Configure CORS origins for mobile app
   - Set up PDF output directory permissions

6. TESTING:
   - Test email notifications with valid SMTP settings
   - Verify PDF generation in static/ directory
   - Test API endpoints with mobile app or Postman
    """)

if __name__ == "__main__":
    print_installation_guide()
