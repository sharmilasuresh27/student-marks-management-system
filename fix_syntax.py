# Fix SQL syntax error in app.py
with open('app.py', 'r') as f:
    content = f.read()

# Fix the SQL syntax error by adding missing triple quotes
content = content.replace(
    'students = conn.execute """',
    'students = conn.execute("""'
)

content = content.replace(
    '""", (teacher_class,)).fetchall()',
    '""", (teacher_class,)).fetchall()'
)

with open('app.py', 'w') as f:
    f.write(content)

print("Fixed SQL syntax error!")
