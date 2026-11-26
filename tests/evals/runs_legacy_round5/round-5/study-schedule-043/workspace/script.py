import csv
import datetime

# Date range: 2026-11-16 to 2026-12-18 (33 days)
# Exams:
# - Algebra: 2026-12-10
# - Geometry: 2026-12-15
# - Statistics: 2026-12-18

start_date = datetime.date(2026, 11, 16)
end_date = datetime.date(2026, 12, 18)

# Let's generate a complete day-by-day plan with specific daily topics, hours, revision slots, spaced repetition tags.
# Weekdays: 2.0 hours, Weekends/Holidays: 4.0 hours (or targeted exam prep days).

schedule = [
    # Week 1: Algebra Core
    ("2026-11-16", "Monday", "Unit 1: Algebra", "Linear equations and inequalities (solving & graphing)", 2.5, "Day 1 baseline study", "Initial learning"),
    ("2026-11-17", "Tuesday", "Unit 1: Algebra", "Systems of equations: Substitution method", 2.0, "Practice 5 word problems", "Spaced Rep: Linear Equations (Day +1)"),
    ("2026-11-18", "Wednesday", "Unit 1: Algebra", "Systems of equations: Elimination method", 2.0, "Compare substitution vs elimination", "Spaced Rep: Systems Substitution (Day +1)"),
    ("2026-11-19", "Thursday", "Unit 1: Algebra", "Polynomial addition, subtraction, and multiplication", 2.0, "Distributive property drills", "Spaced Rep: Systems Elimination (Day +1)"),
    ("2026-11-20", "Friday", "Unit 1: Algebra", "Factoring polynomials (GCF and grouping)", 2.0, "Identify common factoring patterns", "Spaced Rep: Polynomial Operations (Day +1)"),
    ("2026-11-21", "Saturday", "Unit 1: Algebra", "Factoring quadratic polynomials ($ax^2 + bx + c$)", 4.0, "Intensive factoring problem set", "Spaced Rep: Linear & Systems Review (Day +5)"),
    ("2026-11-22", "Sunday", "Unit 1: Algebra", "Algebra Unit Review & Error Log Analysis", 3.5, "Identify weak sub-topics", "Spaced Rep: Polynomials & Factoring (Day +3)"),

    # Week 2: Geometry Core & Algebra Spaced Rep
    ("2026-11-23", "Monday", "Unit 2: Geometry", "Triangles: Congruence criteria (SSS, SAS, ASA, AAS)", 2.0, "Proof foundations", "Spaced Rep: Algebra Comprehensive Check"),
    ("2026-11-24", "Tuesday", "Unit 2: Geometry", "Triangles: Similarity theorems and scale factors", 2.0, "Ratio & proportion problems", "Spaced Rep: Triangles Congruence (Day +1)"),
    ("2026-11-25", "Wednesday", "Unit 2: Geometry", "Circles: Tangents, chords, and perpendicular bisectors", 2.0, "Theorem application sketches", "Spaced Rep: Triangles Similarity (Day +1)"),
    ("2026-11-26", "Thursday", "Unit 2: Geometry", "Circles: Arcs, central angles, and inscribed angles", 2.0, "Angle measure calculations", "Spaced Rep: Circle Tangents/Chords (Day +1)"),
    ("2026-11-27", "Friday", "Unit 2: Geometry", "Coordinate geometry: Distance and midpoint formulas", 2.0, "Connecting algebra and geometry", "Spaced Rep: Circle Arcs/Angles (Day +1)"),
    ("2026-11-28", "Saturday", "Unit 2: Geometry", "Coordinate geometry: Slope, parallel, and perpendicular lines", 4.0, "Graphing and equation derivation", "Spaced Rep: Triangles & Circles Review (Day +5)"),
    ("2026-11-29", "Sunday", "Unit 2: Geometry", "Geometry Unit Review & Mixed Practice", 3.5, "Self-assessment quiz", "Spaced Rep: Coordinate Geometry (Day +3)"),

    # Week 3: Statistics & Algebra Exam Prep
    ("2026-11-30", "Monday", "Unit 3: Stats & Prob", "Mean, median, mode, and weighted mean", 2.0, "Data set analysis", "Spaced Rep: Geometry Core Concepts (Day +3)"),
    ("2026-12-01", "Tuesday", "Unit 3: Stats & Prob", "Standard deviation, variance, and spread", 2.0, "Formula application & interpretation", "Spaced Rep: Stats Central Tendency (Day +1)"),
    ("2026-12-02", "Wednesday", "Unit 3: Stats & Prob", "Probability basics, sample spaces, and compound events", 2.0, "Tree diagrams & tables", "Spaced Rep: Standard Deviation (Day +1)"),
    ("2026-12-03", "Thursday", "Unit 3: Stats & Prob", "Permutations and combinations", 2.0, "Counting principle practice", "Spaced Rep: Probability Basics (Day +1)"),
    ("2026-12-04", "Friday", "Exam Prep / Algebra", "Algebra Targeted Exam Prep: Systems & Factoring", 2.0, "Past paper questions (Algebra)", "Spaced Rep: Permutations/Combinations (Day +1)"),
    ("2026-12-05", "Saturday", "Exam Prep / Algebra", "Algebra Full Practice Test & Timing Simulation", 4.0, "Timed 60-min exam mock", "Spaced Rep: Algebra Comprehensive Review"),
    ("2026-12-06", "Sunday", "Exam Prep / Algebra", "Algebra Error Correction & Advanced Problem Set", 3.5, "Targeted weak-point reinforcement", "Spaced Rep: Algebra Mistake Log Review"),

    # Week 4: Geometry Exam Prep & Algebra Final Polish
    ("2026-12-07", "Monday", "Exam Prep / Algebra", "Algebra Final Review & Formula Memorization", 2.0, "Quick-fire review cards", "Spaced Rep: Algebra Final Refresh"),
    ("2026-12-08", "Tuesday", "Exam Prep / Geometry", "Geometry Targeted Exam Prep: Proofs & Coordinate Math", 2.0, "Targeted geometry problems", "Spaced Rep: Geometry Proofs Refresh"),
    ("2026-12-09", "Wednesday", "Exam Prep / Algebra", "Algebra Final Mock Exam & Confidence Builder", 2.5, "Light review, rest well for tomorrow", "Spaced Rep: Algebra Last-Mile Review"),
    ("2026-12-10", "Thursday", "EXAM DAY", "ALGEBRA EXAM (Weight: 35%)", 3.0, "Exam Day: Focus & execution", "EXAM 1: ALGEBRA"),
    ("2026-12-11", "Friday", "Exam Prep / Geometry", "Geometry Full Practice Test & Timing Simulation", 3.0, "Timed geometry mock test", "Spaced Rep: Geometry Full Review"),
    ("2026-12-12", "Saturday", "Exam Prep / Geometry", "Geometry Error Analysis & Statistics Initial Review", 4.0, "Review geometry mock errors + intro stats refresher", "Spaced Rep: Geometry Mistake Log"),
    ("2026-12-13", "Sunday", "Exam Prep / Geometry", "Geometry Final Review & Formula Flashcards", 3.5, "Theorem & property mastery", "Spaced Rep: Geometry Final Polish"),

    # Week 5: Statistics Exam Prep & Final Exams
    ("2026-12-14", "Monday", "Exam Prep / Geometry", "Geometry Final Polish & Light Statistics Review", 2.5, "Final prep for Geometry exam", "Spaced Rep: Geometry Last-Mile Review"),
    ("2026-12-15", "Tuesday", "EXAM DAY", "GEOMETRY EXAM (Weight: 35%)", 3.0, "Exam Day: Focus & execution", "EXAM 2: GEOMETRY"),
    ("2026-12-16", "Wednesday", "Exam Prep / Stats", "Statistics & Probability Comprehensive Review & Practice", 3.0, "Review all stats & probability notes", "Spaced Rep: Stats Comprehensive Refresh"),
    ("2026-12-17", "Thursday", "Exam Prep / Stats", "Statistics Mock Exam & Final Formulas Check", 3.0, "Timed stats practice test", "Spaced Rep: Stats Final Mock Review"),
    ("2026-12-18", "Friday", "EXAM DAY", "STATISTICS EXAM (Weight: 30%)", 3.0, "Exam Day: Final exam of the series!", "EXAM 3: STATISTICS & PROBABILITY"),
]

print(f"Total scheduled days: {len(schedule)}")

# Write CSV
csv_filename = "study_plan.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Day of Week", "Subject / Unit", "Daily Topic", "Study Hours", "Notes / Activity", "Spaced Rep Slot"])
    for row in schedule:
        writer.writerow(row)

print(f"Generated {csv_filename}")

# Write Markdown
md_filename = "study_plan.md"
with open(md_filename, "w", encoding="utf-8") as f:
    f.write("# Comprehensive Study Plan: Grade 10 Mathematics\n\n")
    f.write("This study plan is meticulously designed for Grade 10 Mathematics, covering all units from `syllabus.md` and aligning with the exam dates and weights from `exams.csv`:\n\n")
    f.write("| Subject / Exam | Date | Weight |\n|---|---|---|\n")
    f.write("| Algebra | 2026-12-10 | 35% |\n")
    f.write("| Geometry | 2026-12-15 | 35% |\n")
    f.write("| Statistics & Probability | 2026-12-18 | 30% |\n\n")
    
    f.write("## Study Strategy & Methodology\n")
    f.write("- **Spaced Repetition:** Built-in review intervals (`Day +1`, `Day +3`, `Day +5`) ensure long-term retention of previously covered topics across units.\n")
    f.write("- **Hours Allocation:** Weekdays feature 2.0 to 2.5 hours of focused study; weekends and intensive exam prep days feature 3.5 to 4.0 hours.\n")
    f.write("- **Active Recall & Practice:** Each session includes specific activities such as problem sets, error log analysis, and full-length timed mock exams.\n\n")

    f.write("## Daily Schedule\n\n")
    f.write("| Date | Day | Unit / Phase | Daily Topic | Hours | Notes / Activity | Spaced Rep / Review Slot |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for row in schedule:
        f.write(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |\n")

    f.write("\n## Exam Week Summary & Guidelines\n")
    f.write("1. **Algebra Exam (Dec 10):** Focus on factoring speed, systems elimination/substitution accuracy, and linear graphing.\n")
    f.write("2. **Geometry Exam (Dec 15):** Focus on triangle congruence/similarity proofs, circle angle theorems, and coordinate geometry formulas.\n")
    f.write("3. **Statistics Exam (Dec 18):** Focus on standard deviation calculation steps, combinatorial counting formulas, and weighted mean problems.\n")

print(f"Generated {md_filename}")
