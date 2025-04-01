import csv

with open('Estudiants_èxit_accés_anònim.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)
