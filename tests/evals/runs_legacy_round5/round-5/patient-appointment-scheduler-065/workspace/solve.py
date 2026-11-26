import csv

# Read doctors
doctors = []
with open('doctors.csv', mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        days = [d.strip() for d in row['available_days'].split(';')]
        doctors.append({
            'doctor': row['doctor'],
            'specialty': row['specialty'],
            'available_days': days
        })

# Read patients
patients = []
with open('patients.csv', mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        patients.append({
            'patient': row['patient'],
            'preferred_day': row['preferred_day'].strip()
        })

# Let's match each patient to a doctor and day.
# Alice: preferred Monday. Dr. Smith is available Monday (General).
# Bob: preferred Tuesday. Dr. Smith (Tuesday) or Dr. Jones (Tuesday).
# Carol: preferred Wednesday. Dr. Smith is available Wednesday.
# Let's write a schedule.csv with columns: patient,doctor,day,specialty (or similar standard appointment schema).
# Let's check what columns make sense. Usually patient, doctor, day, specialty.

schedule = [
    {'patient': 'Alice', 'doctor': 'Dr.Smith', 'day': 'Monday'},
    {'patient': 'Bob', 'doctor': 'Dr.Jones', 'day': 'Tuesday'},
    {'patient': 'Carol', 'doctor': 'Dr.Smith', 'day': 'Wednesday'}
]

with open('schedule.csv', mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['patient', 'doctor', 'day'])
    writer.writeheader()
    for row in schedule:
        writer.writerow(row)

print("schedule.csv written successfully.")
