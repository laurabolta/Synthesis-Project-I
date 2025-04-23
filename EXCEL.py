import pandas as pd
import os

# This file will just contain the way we found to fix the dataframe issues of excel files ALUMNES 2020, 2021 and 2022.
# So, if somebody else has again this problem can use this piece of code and solve the issue. 

input_file = " "  # Path to the input CSV file (replace "..." with the actual path)
output_file = " "  # Path to the output CSV file (replace "..." with the desired output path)

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: The file {input_file} does not exist. Please check the file path.")
else:
    try:
        # Read the CSV file using a semicolon (;) delimiter
        df = pd.read_csv(input_file, delimiter=";")  

        # Replace all commas with periods in string fields
        # The applymap function applies the lambda function to every cell in the DataFrame
        df = df.applymap(lambda x: x.replace(",", ".") if isinstance(x, str) else x)

        # Save the cleaned dataset to the output file
        df.to_csv(output_file, index=False)
        print(f"File cleaned and saved as {output_file} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")