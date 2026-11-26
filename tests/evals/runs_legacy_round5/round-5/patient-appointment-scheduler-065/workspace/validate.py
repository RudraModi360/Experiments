import csv

def validate():
    doctors = {}
    with open('doctors.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            doctors[r['doctor']] = [d.strip() for d in r['available_days'].split(';')]

    with open('schedule.csv', mode='r') as f:
        reader = csv.DictReader(f)
        schedule = list(reader)

    assert len(schedule) == 3, f"Expected 3 appointments, got {len(schedule)}"
    
    for row in schedule:
        doc = row['doctor']
        day = row['day']
        assert day in doctors[doc], f"Doctor {doc} is not available on {day}"
    
    print("Validation passed successfully!")

if __name__ == '__main__':
    validate()
