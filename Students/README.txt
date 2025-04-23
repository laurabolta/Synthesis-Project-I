Description of CSV Datasets (PSI_students_performance_GEI_GIA_v01.zip)

These datasets contain student performance and dropout information. Most column names are self-explanatory, but some require further clarification:

In file "Estudiants_èxit_accés_anònim.csv":

	"Taxa èxit" (Success Rate): This is the ratio of credits approved to credits enrolled.

In file "Estudiants_abandonament_anònim.csv": 

This file tracks student dropouts ("abandonaments"). Possible values are 1 (if they droped), and 0 (if not).

We have several columns depending on how we define dropout ("abandonament"). Consider that Dropout can be static or dynamic. We can consider if they drop out in the first year of study, the second, etc. In addition, dropout can be considered if they stop studying for a year, even if they return later, if we wait 2 years to consider it, etc. 

We have 4 columns to indicate: 

	Dropout (at any moment).
	Real dropout (if they return after 2 years is NOT considered dropout).
	Real 1-year criterion.
	Real (dropout in the first year) with 1-year criterion.
