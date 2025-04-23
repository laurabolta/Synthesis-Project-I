import pandas as pd

df = pd.read_csv("Students\ALUMNES_2020-21.csv", delimiter=";")  

# Replace all commas in every string field with periods
df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
df.to_csv("Alumnes_2020-21.csv", index=False)


df = pd.read_csv("Students\ALUMNES_2021-22.csv", delimiter=";")  
df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
df.to_csv("Alumnes_2021-22.csv", index=False)


df = pd.read_csv("Students\ALUMNES_2022-23.csv", delimiter=";")  
df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)
df.to_csv("Alumnes_2021-22.csv", index=False)