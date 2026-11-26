import csv

def audit():
    policy = {
        'Travel': 500,
        'Meals': 50,
        'Supplies': None
    }
    
    violations = []
    total_expenses = 0
    total_violations_amount = 0
    
    with open('expenses.csv', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_expenses += 1
            category = row['category']
            amount = float(row['amount'])
            limit = policy.get(category)
            
            if limit is not None and amount > limit:
                violations.append({
                    'date': row['date'],
                    'vendor': row['vendor'],
                    'category': category,
                    'amount': row['amount'],
                    'limit': str(limit),
                    'excess': str(amount - limit)
                })
                total_violations_amount += (amount - limit)
                
    # Write violations.csv
    with open('violations.csv', mode='w', newline='') as f:
        fieldnames = ['date', 'vendor', 'category', 'amount', 'limit', 'excess']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for v in violations:
            writer.writerow(v)
            
    # Write audit.md
    md_content = f"""# Expense Audit Report

## Summary
- **Total Expenses Audited:** {total_expenses}
- **Total Violations Found:** {len(violations)}
- **Total Excess Amount:** ${total_violations_amount:.2f}

## Policy Rules
- **Travel:** Maximum $500 per trip
- **Meals:** Maximum $50
- **Supplies:** No limit

## Violation Details
"""
    if violations:
        md_content += "| Date | Vendor | Category | Amount | Limit | Excess |\n"
        md_content += "|---|---|---|---|---|---|\n"
        for v in violations:
            md_content += f"| {v['date']} | {v['vendor']} | {v['category']} | ${float(v['amount']):.2f} | ${float(v['limit']):.2f} | ${float(v['excess']):.2f} |\n"
    else:
        md_content += "No violations found.\n"
        
    with open('audit.md', mode='w') as f:
        f.write(md_content)

if __name__ == '__main__':
    audit()
