from main import ensemble_pipeline
from DATASET import clean_df
import numpy as np

# ------------
# Load dataset
# ------------
df = clean_df.copy()
df = df.dropna(subset=['nota_assignatura'])

# Separate current year data (to predict)
df_train = df[df['curs_academic'] != '2023/24'].copy()
df_pred_target = df[df['curs_academic'] == '2023/24'].copy()

#Define target variable (Nota_assignatura) and input features (droping target from features)
X_train = df_train.drop(columns=['nota_assignatura'])
y_train = df_train['nota_assignatura']

X_pred = df_pred_target.drop(columns=['nota_assignatura'])
y_pred = df_pred_target['nota_assignatura']   # Ground truth for 2023/24

ensemble_pipeline.fit(X_train, y_train)

df_pred_target['predicted_nota_assignatura'] = ensemble_pipeline.predict(X_pred)

#---------------
#Predictions 
#--------------

id_alumne_random = np.random.choice(df_pred_target['id_anonim'].unique())
df_alumne_random = df_pred_target[df_pred_target['id_anonim'] == id_alumne_random]
df_alumne_random_resultados = df_alumne_random[['id_anonim', 'assignatura', 'curs_academic', 'predicted_nota_assignatura', 'nota_assignatura']]

# Imprimir los resultados
print(f"Resultados para el alumno con id_anonim {id_alumne_random}:")
print(df_alumne_random_resultados)