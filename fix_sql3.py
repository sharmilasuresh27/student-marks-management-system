# Fix SQL syntax error in student_profile function
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the SQL syntax error in student_profile
for i, line in enumerate(lines):
    if 'student = conn.execute """' in line:
        lines[i] = line.replace('conn.execute """', 'conn.execute("""')
    elif 'WHERE id = ? AND class =?' in line:
        lines[i] = line.replace('WHERE id = ? AND class =?', 'WHERE id = ? AND class = ?')

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Student-profile SQL syntax error fixed!")
