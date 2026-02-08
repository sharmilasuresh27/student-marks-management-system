# Fix SQL syntax error
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the SQL syntax error
for i, line in enumerate(lines):
    if 'conn.execute """' in line:
        lines[i] = line.replace('conn.execute """', 'conn.execute("""')
    elif '""", (teacher_class,)).fetchall()' in line:
        lines[i] = line.replace('""", (teacher_class,)).fetchall()', '""", (teacher_class,)).fetchall()')

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SQL syntax error fixed!")
