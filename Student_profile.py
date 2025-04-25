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

# ---------------------------------------------------
#Students background clustering vs grades clustering
# --------------------------------------------------
# This code will cluster students based on their background data and grades, and then compare the clusters.
# We will use KMeans clustering to group students based on their background and grades.
# We will also visualize the clusters using PCA for dimensionality reduction.
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# --------------------------
# Load & Preprocess Background Data
# --------------------------
df_background = pd.read_csv(file1)

# Select and preprocess relevant features
df_background_filtered = df_background[[  
    'Id Anonim',
    'Sexe',
    'Via Accés Estudi',
    'Nota d\'accés (preinscripció)',
    'Dedicació de l\'estudiant',
    'Beca Concedida?',
    'Estudis Mare',
    'Estudis Pare'
]].dropna(subset=['Nota d\'accés (preinscripció)'])  # Ensure valid grades

# One-hot encode categorical variables
df_background_encoded = pd.get_dummies(
    df_background_filtered.drop(columns=['Id Anonim']),
    drop_first=True
)

# Scale the background features
scaler = StandardScaler()
background_scaled = scaler.fit_transform(df_background_encoded)

# Clustering background data
k = 3
kmeans_background = KMeans(n_clusters=k, random_state=42)
clusters_background = kmeans_background.fit_predict(background_scaled)

# Store background clusters
df_background_filtered['Cluster_background'] = clusters_background

# PCA for visualization (1D)
pca_background = PCA(n_components=1)
background_1d = pca_background.fit_transform(background_scaled)

# --------------------------
# GRADES-ONLY CLUSTERING
# --------------------------
# Normalize grade column
grade_scaled = StandardScaler().fit_transform(
    df_background_filtered[['Nota d\'accés (preinscripció)']]
)

# PCA (optional with 1 feature)
pca_grade = PCA(n_components=1)
grade_1d = pca_grade.fit_transform(grade_scaled)

# Clustering based on grades only
kmeans_grades = KMeans(n_clusters=3, random_state=42)
clusters_grades = kmeans_grades.fit_predict(grade_1d)

# Store grade clusters
df_background_filtered['Cluster_admission'] = clusters_grades

# --------------------------
# PLOT: Side-by-side 1D Clustering Comparison
# --------------------------
fig, axs = plt.subplots(2, 1, figsize=(12, 4), sharex=True)

# Access grade-only clustering
axs[0].scatter(
    grade_1d,
    [0] * len(grade_1d),
    c=clusters_grades,
    cmap='viridis',
    edgecolors='k',
    s=60,
    alpha=0.7
)
axs[0].set_title('Clustering basat en la Nota d\'accés (1D)')
axs[0].set_yticks([])

# Background PCA clustering
axs[1].scatter(
    background_1d,
    [0] * len(background_1d),
    c=clusters_background,
    cmap='viridis',
    edgecolors='k',
    s=60,
    alpha=0.7
)
axs[1].set_title('Clustering basat en Característiques de Fons (PCA 1D)')
axs[1].set_yticks([])

plt.xlabel('PCA Component 1 / Nota Normalitzada')
plt.tight_layout()
plt.grid(True)
plt.show()


