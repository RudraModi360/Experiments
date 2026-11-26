import csv
import statistics

# Read grades.csv
with open('grades.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

students_data = []

for row in rows:
    student = row['student']
    a1 = float(row['assignment1'])
    a2 = float(row['assignment2'])
    a3 = float(row['assignment3'])
    w1 = float(row['weight1'])
    w2 = float(row['weight2'])
    w3 = float(row['weight3'])
    
    # Compute final grade
    final_grade = (a1 * w1) + (a2 * w2) + (a3 * w3)
    
    # Determine letter grade
    # Standard scale: >= 90: A, >= 80: B, >= 70: C, >= 60: D, < 60: F
    if final_grade >= 90:
        letter = 'A'
    elif final_grade >= 80:
        letter = 'B'
    elif final_grade >= 70:
        letter = 'C'
    elif final_grade >= 60:
        letter = 'D'
    else:
        letter = 'F'
        
    students_data.append({
        'student': student,
        'assignment1': a1,
        'assignment2': a2,
        'assignment3': a3,
        'weight1': w1,
        'weight2': w2,
        'weight3': w3,
        'final_grade': round(final_grade, 2),
        'letter_grade': letter
    })

# Write grades_out.csv
fieldnames = ['student', 'assignment1', 'assignment2', 'assignment3', 'weight1', 'weight2', 'weight3', 'final_grade', 'letter_grade']
with open('grades_out.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for s in students_data:
        writer.writerow(s)

# Compute class stats
final_grades = [s['final_grade'] for s in students_data]
class_mean = statistics.mean(final_grades)
class_median = statistics.median(final_grades)
class_min = min(final_grades)
class_max = max(final_grades)
class_stdev = statistics.stdev(final_grades) if len(final_grades) > 1 else 0.0

# Count letter grades
letter_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
for s in students_data:
    letter_counts[s['letter_grade']] += 1

# Write stats.md
stats_content = f"""# Class Grade Statistics

## Summary Statistics
- **Total Students:** {len(students_data)}
- **Class Mean Final Grade:** {class_mean:.2f}
- **Class Median Final Grade:** {class_median:.2f}
- **Minimum Final Grade:** {class_min:.2f}
- **Maximum Final Grade:** {class_max:.2f}
- **Standard Deviation:** {class_stdev:.2f}

## Letter Grade Distribution
- **A:** {letter_counts['A']}
- **B:** {letter_counts['B']}
- **C:** {letter_counts['C']}
- **D:** {letter_counts['D']}
- **F:** {letter_counts['F']}

## Student Grades Summary
| Student | Final Grade | Letter Grade |
|:---|:---:|:---:|
"""
for s in students_data:
    stats_content += f"| {s['student']} | {s['final_grade']:.2f} | {s['letter_grade']} |\n"

with open('stats.md', mode='w', encoding='utf-8') as f:
    f.write(stats_content)

print("Processing complete. Generated grades_out.csv and stats.md.")
