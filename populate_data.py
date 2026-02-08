import sqlite3
import random
from datetime import datetime

def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

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

def populate_database():
    conn = get_db()
    c = conn.cursor()
    
    # Clear existing data
    c.execute("DELETE FROM students")
    
    # Generate sample students for each class
    for class_name in ['A', 'B', 'C']:
        teacher_name = {
            'A': 'Mrs. Priya Sharma',
            'B': 'Mr. Rajesh Kumar', 
            'C': 'Ms. Ananya Patel'
        }[class_name]
        
        # Create 15-20 students per class
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
            
            total, average, grade, status = calculate_grade_and_status(marks)
            student_id = generate_student_id(class_name)
            
            c.execute("""
                INSERT INTO students (student_id, name, class, class_teacher, 
                                    tamil, english, maths, science, social, 
                                    total, average, grade, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, name, class_name, teacher_name,
                  marks[0], marks[1], marks[2], marks[3], marks[4], 
                  total, average, grade, status))
    
    conn.commit()
    conn.close()
    print("✅ Database populated with sample students!")
    print("📊 Summary:")
    
    # Print summary
    conn = get_db()
    c = conn.cursor()
    
    for class_name in ['A', 'B', 'C']:
        c.execute("SELECT COUNT(*) as count, AVG(total) as avg_total FROM students WHERE class = ?", (class_name,))
        result = c.fetchone()
        print(f"   Class {class_name}: {result['count']} students, Avg Total: {result['avg_total']:.1f}")
        
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

if __name__ == "__main__":
    populate_database()
