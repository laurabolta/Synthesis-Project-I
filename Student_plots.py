import csv
from collections import defaultdict
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from DATASET import merged_df

# PLOTS TO ANALYZE PATTERNS IN THE DATA -----------------------------------------------

# Histogram of assignment grades
plt.figure(figsize=(8, 6))
sns.histplot(merged_df['nota_assignatura'], kde=True, bins=20)
plt.title('Distribution of Assignment Grades')
plt.xlabel('Nota Assignatura')
plt.ylabel('Frequency')
plt.show()

"""
From the plot, we can see that there are many cases where students received a grade of 0. 
While the most common grades lie in the range between 4 and 10.

We should inspect where all these zeros come from, if they are really student's marks
or if they are related to other factors such as drop out.
"""

file1 = './Students/Estudiants_èxit_accés_anònim.csv'
file2 = './Students/Estudiants_notes_assignatures_anònim.csv'
file3 = './Students/Estudiants_abandonament_anònim.csv'

# --------------------- To see that everything is okey-------------------------
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

#Students background clustering vs grades clustering
# This code will cluster students based on their background data and grades, and then compare the clusters.
# We will use KMeans clustering to group students based on their background and grades.
# We will also visualize the clusters using PCA for dimensionality reduction.
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import seaborn as sns



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
]].dropna(subset=['Nota d\'accés (preinscripció)'])  # Ensure valid grades

# One-hot encode categorical variables
# Primero cargamos de nuevo el dataframe procesado
df = df_background_filtered.copy()

# ---------------
# Agrupamiento 1: Id Anonim vs Nota d'accés
# ---------------

# Usamos DBSCAN para agrupar notas iguales o muy cercanas
scaler_notes = StandardScaler()
notes_scaled = scaler_notes.fit_transform(df[['Nota d\'accés (preinscripció)']])

dbscan_notes = DBSCAN(eps=0.05, min_samples=1)  # eps pequeño para notas similares
clusters_notes = dbscan_notes.fit_predict(notes_scaled)

# Guardamos el cluster de notas
df['Cluster_same_grade'] = clusters_notes

# ---------------
# Agrupamiento 2: Id Anonim vs Características sociodemográficas
# ---------------

# Seleccionamos las características para agrupar
features = [
    'Beca Concedida?', 
    'Via Accés Estudi', 
    'Sexe',
    'Dedicació de l\'estudiant'
]

# Codificamos las variables categóricas
df_features_encoded = pd.get_dummies(df[features], drop_first=True)

# Escalamos
scaler_features = StandardScaler()
features_scaled = scaler_features.fit_transform(df_features_encoded)

# Clustering basado en similitudes sociodemográficas
dbscan_features = DBSCAN(eps=0.5, min_samples=1)
clusters_features = dbscan_features.fit_predict(features_scaled)

# Guardamos el cluster socio-demográfico
df['Cluster_profile'] = clusters_features

# ---------------
# Resultado
# ---------------

# Mostramos el dataframe final
print(df[['Id Anonim', 'Nota d\'accés (preinscripció)', 'Cluster_same_grade', 'Cluster_profile']])

df_unique = df.drop_duplicates(subset=['Id Anonim'])

sns.set(style="whitegrid")

# --------------------------
# Primer plot: Agrupación por Nota (sin duplicados)
# --------------------------
plt.figure(figsize=(12, 6))
sns.scatterplot(
    x=range(len(df_unique)),  # índice limpio
    y='Nota d\'accés (preinscripció)',
    hue='Cluster_same_grade',
    palette='tab10',
    data=df_unique,
    s=100
)
plt.title('Agrupación por Nota de Acceso (IDs únicos)', fontsize=16)
plt.xlabel('Caso (Índice)')
plt.ylabel('Nota de acceso')
plt.legend(title='Cluster (Notas)')
plt.tight_layout()
plt.show()

# --------------------------
# Segundo plot: Perfil Sociodemográfico (sin duplicados)
# --------------------------
plt.figure(figsize=(12, 6))
sns.scatterplot(
    x=range(len(df_unique)),  # índice limpio
    y='Cluster_profile',
    hue='Cluster_profile',
    palette='tab20',
    data=df_unique,
    s=100
)
plt.title('Agrupación por Perfil Sociodemográfico (IDs únicos)', fontsize=16)
plt.xlabel('Caso (Índice)')
plt.ylabel('Cluster de perfil')
plt.legend(title='Cluster (Perfil)')
plt.tight_layout()
plt.show()

# --------------------------
# CONVERT DICTIONARY INTO A DATAFRAME
# --------------------------

# Create a list to store each student's data
student_rows = []

for student_id, data in students.items():
    # Start with background and abandonment
    student_row = {
        'Id Anonim': student_id,
    }
    
    # Add background info
    if data['background']:
        student_row.update(data['background'])
    
    # Add abandonment info
    if data['abandonment']:
        student_row.update(data['abandonment'])
    
    # Add some grades info (example: number of subjects and average grade)
    grades = []
    for year, year_grades in data['grades'].items():
        for g in year_grades:
            if g['Nota_assignatura']:
                try:
                    grades.append(float(g['Nota_assignatura']))
                except ValueError:
                    pass  # In case of non-numeric grades

    if grades:
        student_row['Average_Grade'] = sum(grades) / len(grades)
        student_row['Number_of_Subjects'] = len(grades)
    else:
        student_row['Average_Grade'] = None
        student_row['Number_of_Subjects'] = 0

    student_rows.append(student_row)

# Create the DataFrame
df_students = pd.DataFrame(student_rows)

# See the result
print(df_students.head())
print(df_students.columns)

