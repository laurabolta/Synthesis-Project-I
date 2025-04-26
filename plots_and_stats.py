import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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
