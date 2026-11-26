# Scheduling Report

## Overview
This report documents the generated appointment schedule based on `patients.csv` and `doctors.csv`.

## Input Data Summary
### Doctors
- **Dr. Smith**: General practice, available on Monday, Tuesday, Wednesday.
- **Dr. Jones**: Cardiology, available on Tuesday, Thursday.

### Patients & Preferences
- **Alice**: Prefers Monday.
- **Bob**: Prefers Tuesday.
- **Carol**: Prefers Wednesday.

## Generated Schedule (`schedule.csv`)

| Patient | Doctor | Day |
| :--- | :--- | :--- |
| Alice | Dr. Smith | Monday |
| Bob | Dr. Jones | Tuesday |
| Carol | Dr. Smith | Wednesday |

## Constraint Validation
1. **Doctor Availability**: 
   - Alice is scheduled with Dr. Smith on Monday (Dr. Smith is available Monday).
   - Bob is scheduled with Dr. Jones on Tuesday (Dr. Jones is available Tuesday).
   - Carol is scheduled with Dr. Smith on Wednesday (Dr. Smith is available Wednesday).
2. **Patient Preferences**: 
   - All patients (Alice, Bob, Carol) are scheduled on their exact preferred days (Monday, Tuesday, Wednesday respectively).
3. **Completeness**: 
   - All 3 patients have been successfully assigned an appointment.
