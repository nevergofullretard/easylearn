import csv

deutsch = []
italienisch = []

with open('unit_1.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    for line in csv_reader:
        deutsch.append(line[0])
        italienisch.append(line[1])

print(deutsch)
print(italienisch)
