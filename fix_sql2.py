# Fix SQL syntax error in export-word function
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the SQL syntax error in export-word
for i, line in enumerate(lines):
    if 'students = conn.execute """' in line and i > 600:  # export-word function
        lines[i] = line.replace('conn.execute """', 'conn.execute("""')

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Export-word SQL syntax error fixed!")
