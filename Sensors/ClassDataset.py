import pandas as pd

# Load ocupacio data
ocupacio_df = pd.read_csv('Attendance/ocupacio_aules_EE_24_25_v06.csv', sep=',')
ocupacio_df['Codi_Ass'] = ocupacio_df['Codi_Ass + Assignatura'].str.extract(r'(\d+)')
ocupacio_df['Codi_Ass'] = ocupacio_df['Codi_Ass'].astype(str).str.strip()

# Load professors GEI
professors_df_EE = pd.read_csv('Profesors/GEI_anònim_2.csv', sep=',', on_bad_lines='skip')
professors_df_EE.columns = professors_df_EE.columns.str.strip()
professors_df_EE = professors_df_EE[professors_df_EE['Codi_Ass'].notnull()]
professors_df_EE['Codi_Ass'] = professors_df_EE['Codi_Ass'].astype('Int64').astype(str)

# Load professors IA
professors_df_IA = pd.read_csv('Profesors/IA_anònim_1.csv', sep=';', skiprows=4, on_bad_lines='skip')
professors_df_IA.columns = professors_df_IA.columns.str.strip()
professors_df_IA = professors_df_IA[professors_df_IA['Codi_Ass'].notnull()]
professors_df_IA['Codi_Ass'] = professors_df_IA['Codi_Ass'].astype('Int64').astype(str)

# Combine and group professor data
professors_total = pd.concat([
    professors_df_EE[['Codi_Ass','Assignatura', 'Id Anònim PD']],
    professors_df_IA[['Codi_Ass','Assignatura', 'Id Anònim PD']]
], ignore_index=True)


# Keep the first Assignatura per Codi_Ass 
assignatures_grouped = professors_total.groupby('Codi_Ass')['Assignatura'].first().reset_index()

# Aggregate multiple professors per Codi_Ass
professors_grouped = professors_total.groupby('Codi_Ass')['Id Anònim PD'].agg(
    lambda x: ', '.join(sorted(set(x)))
).reset_index()

professors_grouped = pd.merge(professors_grouped, assignatures_grouped, on='Codi_Ass', how='left')

# Merge with ocupacio data
merged_df = pd.merge(ocupacio_df, professors_grouped, on='Codi_Ass', how='left')

# Final output selection
final_data = merged_df[['start date', 'start time', 'end date', 'end time', 'class Id', 'Codi_Ass', 'Assignatura', 'Id Anònim PD']]

# Export to CSV
final_data.to_csv('Sensors/merged_occupacio_professors.csv', index=False)

# Preview
print(final_data[['Codi_Ass', 'Id Anònim PD']].drop_duplicates().head(10))
