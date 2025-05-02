import pandas as pd

# Load the first dataset (Course Details)
data1 = pd.read_csv('Attendance/ocupacio_aules_EE_24_25_v06.csv', sep=',')
print("Columns in first dataset:", data1.columns)

# Extract and clean 'Codi_Ass' from 'Codi_Ass + Assignatura'
data1['Codi_Ass'] = data1['Codi_Ass + Assignatura'].str.extract(r'(\d+)')  # Extract only the numeric part
data1['Codi_Ass'] = data1['Codi_Ass'].astype(str).str.strip()

# Select needed columns
data1_clean = data1[['start date', 'start time', 'end date', 'end time', 'class Id', 'Estudi', 'Codi_Ass']]

# Load second dataset (Professor Details), skip metadata rows
data2 = pd.read_csv('Profesors/IA_anònim_1.csv', sep=';', skiprows=4)
print("Columns in second dataset:", data2.columns)

# Clean up column names and Codi_Ass
data2.columns = data2.columns.str.strip()
data2['Codi_Ass'] = data2['Codi_Ass'].astype(str).str.strip()

# Select needed columns
data2_clean = data2[['Codi_Ass', 'Id Anònim PD']]

# Perform merge
merged_data = pd.merge(data1_clean, data2_clean, on='Codi_Ass', how='left')

# Inspect result
print(merged_data.head())

# Save merged output
merged_data.to_csv('CLASS_PROFESSOR_data.csv', index=False)
