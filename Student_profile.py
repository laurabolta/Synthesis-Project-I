import csv
from collections import defaultdict
import json

file1 = '.\Students\Estudiants_èxit_accés_anònim.csv'
file2 = '.\Students\Estudiants_notes_assignatures_anònim.csv'
file3 = '.\Students\Estudiants_abandonament_anònim.csv'

# Dictionary that will merge the info of every student matching the anonimus ID 
students = defaultdict(lambda: {'background': None, 'grades': defaultdict(list), 'abandonment': None})

# Load background data
with open(file1, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_id = row['Id Anonim']
        background_data = {
            'Estudi': row['Estudi'],
            'Curs acadèmic': row['Curs acadèmic'],
            'Sexe': row['Sexe'],
            'Curs acadèmic accés estudi': row['Curs acadèmic accés estudi'],
            'Via Accés Estudi': row['Via Accés Estudi'],
            'Nota d\'accés (preinscripció)': row['Nota d\'accés (preinscripció)'],
            'Dedicació de l\'estudiant': row['Dedicació de l\'estudiant'],
            'S/N Discapacitat': row['S/N Discapacitat'],
            'Beca Concedida?': row['Beca Concedida?'],
            'Estudis Mare': row['Estudis Mare'],
            'Estudis Pare': row['Estudis Pare'],
            'Taxa èxit': row['Taxa èxit'],
        }
        students[student_id]['background'] = background_data

# Loading grades
with open(file2, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_id = row['Alumne']
        academic_year = row['Curs acadèmic']
        grade_entry = {
            'Assignatura': row['Assignatura'],
            'Codi assignatura': row['Codi assignatura'],
            'Nota_assignatura': row['Nota_assignatura'],
        }
        students[student_id]['grades'][academic_year].append(grade_entry)

# Loading abandonment data 
with open(file3, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_id = row['Id Anonim']
        abandonment_data = {
            'Estudi': row['Estudi'],  #should we leave this in case the student is studying double carrers?
            'Curs acadèmic': row['Curs acadèmic'],
            'Nombre Abandonaments Universitat': row['Nombre Abandonaments Universitat'],
            'Nombre Abandonaments Universitat Reals': row['Nombre Abandonaments Universitat Reals'],
            'Nombre Abandonaments Universitat Reals criteri 1 any': row['Nombre Abandonaments Universitat Reals criteri 1 any'],
            'Nombre Abandonaments Universitat Reals 1r any criteri 1 any': row['Nombre Abandonaments Universitat Reals 1r any criteri 1 any'],
        }
        students[student_id]['abandonment'] = abandonment_data

# Converting defaultdict to regular dict
students = {
    k: {
        'background': v['background'],
        'grades': dict(v['grades']),
        'abandonment': v['abandonment']
    } for k, v in students.items()
}

# Example usage
student_id = '1DFB71F2B000D1421808D0B3F67B335E'

# Pretty-print the data
if student_id in students:
    print(json.dumps(students[student_id], indent=4, ensure_ascii=False))   #I WOULD LIKE TO CHANGE THIS PUT FOR NOW TO CHECK ITS OKEY :)
else:
    print(f"Student ID '{student_id}' not found.")


# --------------------- To see that everything its okey-------------------------
# Count unique student IDs from each dataset
def count_unique_ids(file_path, column_name):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return len(set(row[column_name] for row in reader))

# Adjust column names based on your data
count_file1 = count_unique_ids(file1, 'Id Anonim')
count_file2 = count_unique_ids(file2, 'Alumne')
count_file3 = count_unique_ids(file3, 'Id Anonim')
count_dict = len(students)

# Print results
print(f"Unique students in dataset 1: {count_file1}")
print(f"Unique students in dataset 2: {count_file2}")
print(f"Unique students in dataset 3: {count_file3}")
print(f"Total students in final dictionary: {count_dict}")

# Final check
if count_dict == count_file1 == count_file2 == count_file3:
    print("\nAll datasets have matching student IDs. Dictionary correctly initialized.")
else:
    print("\nMismatch detected.")

