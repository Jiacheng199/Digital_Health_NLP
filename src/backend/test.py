import csv
newrow = ['Review', 'Non-match', 'UIL']
with open('modify.csv', mode='r', newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)
    found = False
    for row in rows:
        print(row)
        if newrow[0] in row:
            row[1] = newrow[1]
            found = True
            break
    if not found:
        rows.append(newrow[0:2])
with open('modify.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(rows)