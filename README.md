# Synthesis-Project-I: AI mentor program
The goal of this project is to identify students who might be at risk of failing by using past academic data and machine learning. This helps schools to support students early, before problems happen. The project has two main parts: first, giving teachers useful information about their classes and students; second, sending alert messages to students at risk, with activities and exercises to help them succeed.

### Key Features
- Predict students who are at risk of academic failure.
- Send automated alerts to students and professors.
- Web integration.


![Alt text](Images/visualization.png)


### How to set up environment and dependencies

#### Using Conda Environment
The environment is defined in the file `synthesis.yml`

To create the environment, run this command on your terminal:
`conda env create -f synthesis.yml`

To activate the environment, use:
`conda activate synthesis`

#### Using pip Requirements

To install the Python packages listed in `requirements.txt`, run:

`pip install -r requirements.txt`

#### Running the Alert Message Code
streamlit.md (nombre del archivo, crealo porfa en Alert Message)

Base inicial.csv tiene lo que le va a aparecer en el excel de la pagina web

App_profesors.py es donde esta la app de streamlit, para darle a run tenemos que descargar todos los paquetes importados (estaria bien crear un environment para todas - con el nombre de project o algo asi). Codigo de run
""
streamlit run app_profesors.py
""

Carpeta professors es de donde cojemos la data.

credenciales_google.json sirve para conectar lo que hacemos con una google sheet (online, que esta en la nube)
Creamos una google sheet para cada professors, porque crear diferentes hojas para cada professor iria mucho mas lento.

### Folder Structure

Here we provide a partial view of the project structure, highlighting the most relevant files. We've omitted unimportant/generated files for clarity.

```bash
Synthesis-Project-I/
├── Alert_Message/                  # Necessary files for alert message implementation
│   ├── app_profesors.py
│   └── app_students.py
├── Attendance/                     # Attendance datasets converted to CSV files
├── Images/                         # Images of the final web page  
├── Preparing_Data/                 # Data preprocessing scripts and resources
├── Profesors/                      # Professors datasets converted to CSV files
├── Sensors/
│   ├── ClassDataset.py             # Sensor dataset handling code
│   └── CO2.py                   
├── Students/                       # Students datasets converted to CSV files
├── synthesis/
├── DATASET.py                      # Script to generate clean datasets for training dropout and final mark prediction models
├── DropOutModels.ipynb             # Dropout prediction models implementation
├── DropOut_Conclusions.ipynb       # Analysis and conclusions on dropout prediction results
├── EarlyVsLate.ipynb               # Early vs Late fusion models for final mark prediction
├── Ensamble_trees_SUBJECTS.ipynb   # Ensemble trees model focused on a single subject 
├── main.py 
├── Models.ipynb                    # Regression models for predicting students' final marks
├── Student_plots.ipynb             # Data analysis: correlations and feature importance visualization
```

### Authors

- Anna Blanco | NIU:
- Laura Boltà | NIU:
- Sonia Espinilla | NIU:
- Agustina Lazzati | NIU:
- Queralt Salvadó | NIU: 1706789
