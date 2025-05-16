streamlit.md (nombre del archivo, crealo porfa en Alert Message)

Base inicial.csv tiene lo que le va a aparecer en el excel de la pagina web

App_profesors.py es donde esta la app de streamlit, para darle a run tenemos que descargar todos los paquetes importados (estaria bien crear un environment para todas - con el nombre de project o algo asi). Codigo de run
""
streamlit run app_profesors.py
""

Carpeta professors es de donde cojemos la data.

credenciales_google.json sirve para conectar lo que hacemos con una google sheet (online, que esta en la nube)
Creamos una google sheet para cada professors, porque crear diferentes hojas para cada professor iria mucho mas lento.