# Synthesis-Project-I: AI mentor program

The goal of this project is to identify students who might be at risk of failing by using past academic data and machine learning. This helps schools to support students early, before problems happen. The project has two main parts: first, giving teachers useful information about their classes and students; second, sending alert messages to students at risk, with activities and exercises to help them succeed.

## Key Features
- Predict students who are at risk of academic failure.
- Send automated alerts to students and professors.
- Web integration.


![Alt text](Images/visualization.png)


## How to set up environment and dependencies

### Using Conda Environment

The environment is defined in the file `synthesis.yml`

To create the environment, run this command on your terminal:

```bash
conda env create -f synthesis.yml
```

To activate the environment, use:

```bash
conda activate synthesis
```

### Using pip Requirements

To install the Python packages listed in `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### Running the Alert Message Code
This project is a Streamlit web app for managing professor-related data and generating Excel files connected to Google Sheets.

Main Apps:
- app_profesors.py 
- app_students.py
To run the app, you first need to install the required Python packages (we recommend creating a conda environment for this project).

```bash
streamlit run app_profesors.py` or `streamlit run app_students.py
```

The files/ folder contains all the resources needed for the app to work:
- Exercises
- App background images
- CSV files used to search for information
- Files used to connect Google Sheets with the app

## Folder Structure

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

**Important files:**

- `DATASET.py` – Core script that generates a clean, unified dataset combining student and attendance. This dataset is used for both dropout and grade prediction models.

- `DropOutModels.ipynb` – Contains machine learning models (classifiers) used to predict which students are likely to drop out.

- `DropOut_Conclusions.ipynb` – Presents insights and reasoning based on the performance and results of the dropout models.

- `Models.ipynb` – Implements several regression models to predict students’ final grades using the cleaned dataset.

- `EarlyVsLate.ipynb` – Compares early and late fusion strategies in combining different types of features (e.g., attendance, sensors, academic) for grade prediction.

- `Student_plots.ipynb` – Explores the dataset visually, analyzing feature importance, correlations, and distributions.

- `Ensamble_trees_SUBJECTS.ipynb` – Serves as a baseline model using ensemble methods on individual subjects, used to compare against more general models. However, it was not included in the final version of the project because it takes too much time and computer power to run for all subjects.

- `main.py` – Entry point script that may serve for orchestration, integration, or running specific parts of the pipeline.


**Important Folders:**

* `Alert_Message` – Contains the Streamlit apps for professors (`app_profesors.py`) and students (`app_students.py`). These apps allow users to interact with the data, view predictions, and send alerts. They also generate personalized messages and attach exercises based on student risk levels. The apps use resources from the `files/` folder and are integrated with Google Sheets.

* `Sensors` – Contains scripts for handling classroom environmental data (mainly CO₂). Includes `ClassDataset.py` to build structured datasets and `CO2.py` to generate alerts when air quality may impact learning. This information is used to enrich the prediction models with environmental context.

* `Preparing_Data` – Contains data cleaning and preprocessing scripts. These scripts merge and prepare data from various sources (students, attendance, professors, sensors) and generate the final datasets used for machine learning model training. This step ensures data quality and consistency.

* `files` – Provides essential resources for the apps to work:

  * Exercises to be sent to students.
  * Background images and interface assets.
  * CSV files used for lookups or filtering.
  * Configuration files and credentials for Google Sheets connection.

* `Students/`, `Profesors/`, `Attendance/` – Contain the original and cleaned CSV datasets:

  * `Students/`: Academic records, subject performance, dropout status.
  * `Profesors/`: Courses taught, professor identifiers.
  * `Attendance/`: Attendance records by subject and academic year.
    These folders provide the raw inputs for both analysis and predictive modeling.


## Authors

- Anna Blanco | NIU: 1709582
- Laura Boltà | NIU: 1705130
- Sonia Espinilla | NIU: 1708919
- Agustina Lazzati | NIU: 1707964
- Queralt Salvadó | NIU: 1706789
