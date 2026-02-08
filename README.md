# 🎓 School Management System

A professional, real-time school management system built with Flask, SQLite, and modern web technologies. Perfect for resume building and internship evaluations.

## ✨ Features

### 🔐 Authentication System
- **Teacher Login**: Secure login with name, password, and class selection
- **Class-Based Access**: Teachers can only access their assigned class students
- **Session Management**: Secure session handling with logout functionality

### 📊 Academic Management
- **Student CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Auto-Generated Student IDs**: Unique IDs in format `STD2024A1234`
- **Subject-Wise Marks**: Tamil, English, Maths, Science, Social Science
- **Automatic Calculations**: Total, Average, Grade, and Pass/Fail status
- **Enhanced Grading**: A+, A, B+, B, C, D, F grade system

### 🏆 Advanced Analytics
- **Dashboard**: Class statistics, performance metrics, recent students
- **Class Toppers**: Individual class champions with detailed analysis
- **School Topper**: Overall best performer with comprehensive metrics
- **Weak Students**: Academic support identification with recommendations
- **All Classes View**: Comprehensive school-wide rankings

### 🎨 Professional UI/UX
- **Modern Design**: Gradient backgrounds with glassmorphism effects
- **Class-Specific Colors**: A (Red), B (Teal), C (Blue) color coding
- **Responsive Design**: Works perfectly on all devices
- **Interactive Elements**: Hover effects, smooth animations, sortable tables
- **Real-Time Search**: Filter students by name or ID

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Flask
- SQLite3 (included with Python)

### Installation
1. Clone the repository
2. Navigate to project directory
3. Install dependencies:
   ```bash
   pip install flask
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open browser: `http://127.0.0.1:5000`

### Demo Credentials
- **Class A**: Mrs. Priya Sharma / `priya123`
- **Class B**: Mr. Rajesh Kumar / `rajesh123`
- **Class C**: Ms. Ananya Patel / `ananya123`

## 📁 Project Structure

```
Student Mark Management System/
├── app.py                    # Main Flask application
├── students.db               # SQLite database
├── populate_data.py          # Database population script
├── README.md                # This file
├── static/
│   └── style.css           # Modern responsive styling
└── templates/
    ├── login.html           # Teacher login page
    ├── dashboard.html       # Statistics dashboard
    ├── index.html          # Main student management
    ├── edit.html           # Student edit interface
    ├── class_toppers.html  # Class champions view
    ├── school_topper.html  # School champion view
    ├── weak_students.html  # Academic support view
    └── all_classes.html    # Comprehensive overview
```

## 🗄️ Database Schema

### Teachers Table
```sql
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    assigned_class TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Students Table
```sql
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
);
```

## 🎯 Key Features Demonstrated

### Technical Skills
- **Full-Stack Development**: Flask backend with SQLite database
- **Template Engineering**: Advanced Jinja2 with complex filtering
- **Database Design**: Proper relationships and constraints
- **Authentication**: Role-based access control
- **API Development**: RESTful routes and proper HTTP methods
- **Frontend Development**: Modern HTML5, CSS3, JavaScript

### Professional Practices
- **Error Handling**: Comprehensive exception management
- **Code Organization**: Clean separation of concerns
- **Security**: Input validation and SQL injection prevention
- **Responsive Design**: Mobile-first approach
- **Performance**: Optimized queries and efficient algorithms

### Business Logic
- **Data Analysis**: Statistical calculations and rankings
- **Academic Logic**: Grade calculations and pass/fail determination
- **User Experience**: Intuitive navigation and workflows
- **Data Visualization**: Charts and performance metrics

## 🌟 Sample Data

The system includes realistic sample data:
- **45+ Students** across 3 classes
- **Varied Performance**: Mix of excellent, good, average, and poor performers
- **Realistic Names**: Diverse student names for authenticity
- **Proper Distribution**: Balanced performance across classes

## 📱 Screenshots & Features

### Login Page
- Modern glassmorphism design
- Class selection with visual feedback
- Demo credentials display

### Dashboard
- Real-time statistics
- Class performance metrics
- Quick access to all features

### Student Management
- Sortable data tables
- Real-time search and filtering
- Visual indicators for performance
- Rank badges for top performers

### Analytics Views
- Class toppers with detailed analysis
- School-wide rankings and comparisons
- Weak students identification with recommendations

## 🔧 Customization

### Adding New Classes
1. Update teacher credentials in `create_tables()` function
2. Add class-specific colors in CSS
3. Update templates with new class options

### Modifying Subjects
1. Update database schema
2. Modify grade calculation logic
3. Update form fields and table columns

## 🚀 Deployment

### Production Setup
1. Set `debug = False` in `app.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure proper database with migrations
4. Set up environment variables for secrets

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## 📞 Troubleshooting

### Common Issues
- **Template Errors**: Check Jinja2 syntax and variable names
- **Database Issues**: Verify SQLite file permissions
- **Port Conflicts**: Change port in `app.py`

### Debug Mode
Development mode includes:
- Detailed error pages
- Interactive debugger
- Auto-reload on changes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open-source and available under the MIT License.

## 📞 Contact

Built with ❤️ for educational institutions and learning management.

---

**Perfect for:**
- 🎓 Technical Interviews
- 💼 Internship Evaluations  
- 🏆 Portfolio Demonstrations
- 📚 Academic Projects
