"""
PDF Report Generation System
Add to requirements.txt: ReportLab==4.0.4, Pillow==10.0.0
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
    
    def generate_student_report(self, student_data, output_path):
        """Generate individual student report card"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("STUDENT REPORT CARD", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Student Information
        student_info = [
            ['Student Name:', student_data['name']],
            ['Student ID:', student_data['student_id']],
            ['Class:', student_data['class']],
            ['Date:', datetime.now().strftime('%Y-%m-%d')]
        ]
        
        info_table = Table(student_info, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Marks Table
        marks_heading = Paragraph("ACADEMIC PERFORMANCE", self.heading_style)
        story.append(marks_heading)
        story.append(Spacer(1, 12))
        
        marks_data = [
            ['Subject', 'Marks', 'Grade'],
            ['Tamil', str(student_data.get('tamil', 0)), self._get_grade(student_data.get('tamil', 0))],
            ['English', str(student_data.get('english', 0)), self._get_grade(student_data.get('english', 0))],
            ['Mathematics', str(student_data.get('maths', 0)), self._get_grade(student_data.get('maths', 0))],
            ['Science', str(student_data.get('science', 0)), self._get_grade(student_data.get('science', 0))],
            ['Social Science', str(student_data.get('social', 0)), self._get_grade(student_data.get('social', 0))],
        ]
        
        marks_table = Table(marks_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        marks_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(marks_table)
        story.append(Spacer(1, 20))
        
        # Summary
        summary_data = [
            ['Total Marks', str(student_data.get('total', 0))],
            ['Average', f"{student_data.get('average', 0):.1f}"],
            ['Overall Grade', student_data.get('grade', 'N/A')],
            ['Status', student_data.get('status', 'N/A')]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Remarks
        remarks_heading = Paragraph("TEACHER'S REMARKS", self.heading_style)
        story.append(remarks_heading)
        story.append(Spacer(1, 12))
        
        remarks = student_data.get('remarks', 'Good performance. Keep up the good work!')
        remarks_para = Paragraph(remarks, self.styles['Normal'])
        story.append(remarks_para)
        
        # Build PDF
        doc.build(story)
        return True
    
    def generate_class_report(self, class_data, output_path):
        """Generate class performance report"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph(f"CLASS {class_data['class_name']} PERFORMANCE REPORT", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Class Statistics
        stats_heading = Paragraph("CLASS STATISTICS", self.heading_style)
        story.append(stats_heading)
        story.append(Spacer(1, 12))
        
        stats_data = [
            ['Total Students', str(class_data.get('total_students', 0))],
            ['Class Average', f"{class_data.get('class_average', 0):.1f}"],
            ['Highest Score', str(class_data.get('highest_score', 0))],
            ['Lowest Score', str(class_data.get('lowest_score', 0))],
            ['Pass Percentage', f"{class_data.get('pass_percentage', 0):.1f}%"]
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # Top Performers
        toppers_heading = Paragraph("TOP PERFORMERS", self.heading_style)
        story.append(toppers_heading)
        story.append(Spacer(1, 12))
        
        toppers_data = [['Rank', 'Student Name', 'Total', 'Average', 'Grade']]
        for i, student in enumerate(class_data.get('toppers', []), 1):
            toppers_data.append([
                str(i),
                student['name'],
                str(student['total']),
                f"{student['average']:.1f}",
                student['grade']
            ])
        
        toppers_table = Table(toppers_data, colWidths=[0.8*inch, 2*inch, 1*inch, 1*inch, 1*inch])
        toppers_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(toppers_table)
        
        # Build PDF
        doc.build(story)
        return True
    
    def generate_attendance_report(self, attendance_data, output_path):
        """Generate attendance report"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("ATTENDANCE REPORT", self.title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Attendance Summary
        summary_heading = Paragraph("ATTENDANCE SUMMARY", self.heading_style)
        story.append(summary_heading)
        story.append(Spacer(1, 12))
        
        summary_data = [
            ['Total Working Days', str(attendance_data.get('total_days', 0))],
            ['Present Days', str(attendance_data.get('present_days', 0))],
            ['Absent Days', str(attendance_data.get('absent_days', 0))],
            ['Late Days', str(attendance_data.get('late_days', 0))],
            ['Attendance Percentage', f"{attendance_data.get('attendance_percentage', 0):.1f}%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(summary_table)
        
        # Build PDF
        doc.build(story)
        return True
    
    def _get_grade(self, marks):
        """Get grade based on marks"""
        if marks >= 90:
            return 'A+'
        elif marks >= 80:
            return 'A'
        elif marks >= 70:
            return 'B+'
        elif marks >= 60:
            return 'B'
        elif marks >= 50:
            return 'C'
        elif marks >= 40:
            return 'D'
        else:
            return 'F'

# Integration helper
def setup_pdf_reports():
    """Setup PDF report generation"""
    return PDFReportGenerator()
