import pandas as pd

# Dataset d’ocupació
ocupacio_df = pd.read_csv('Attendance/ocupacio_aules_EE_24_25_v06.csv', sep=',')
ocupacio_df['Codi_Ass'] = ocupacio_df['Codi_Ass + Assignatura'].str.extract(r'(\d+)')
ocupacio_df['Codi_Ass'] = ocupacio_df['Codi_Ass'].astype(str).str.strip()

# Professors GEI
professors_df_EE = pd.read_csv('Profesors/GEI_anònim_2.csv', sep=',', on_bad_lines='skip')
professors_df_EE.columns = professors_df_EE.columns.str.strip()
professors_df_EE = professors_df_EE[professors_df_EE['Codi_Ass'].notnull()]
professors_df_EE['Codi_Ass'] = professors_df_EE['Codi_Ass'].astype('Int64').astype(str)

# Professors IA
professors_df_IA = pd.read_csv('Profesors/IA_anònim_1.csv', sep=';', skiprows=4, on_bad_lines='skip')
professors_df_IA.columns = professors_df_IA.columns.str.strip()
professors_df_IA = professors_df_IA[professors_df_IA['Codi_Ass'].notnull()]
professors_df_IA['Codi_Ass'] = professors_df_IA['Codi_Ass'].astype('Int64').astype(str)

# Combinar professors GEI + IA
professors_total = pd.concat([
    professors_df_EE[['Codi_Ass', 'Id Anònim PD']],
    professors_df_IA[['Codi_Ass', 'Id Anònim PD']]
], ignore_index=True).drop_duplicates(subset='Codi_Ass')

# Merge final
merged_df = pd.merge(ocupacio_df, professors_total, on='Codi_Ass', how='left')

# Exportar i mostrar
merged_df.to_csv('merged_occupacio_professors.csv', index=False)
print(merged_df[['Codi_Ass', 'Id Anònim PD']].drop_duplicates().head(10))



