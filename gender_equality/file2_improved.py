import pandas as pd
import os

def clean_salary_data(input_file=None, output_folder=None):

    #Variable to customize output name file
    mark="else"

    if input_file is None:
        input_file = os.path.join("data", "Table_remuneration.xlsx")
    else:
        file=input("Write the name of the correct file ")
        input_file = os.path.join("data", file)
        mark="Nyet"
    if output_folder is None:
        output_folder = "cleaned_data"
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Reading salary data from: {input_file}")
    df = pd.read_excel(input_file)
    
    #Use of 0 instead of 'NA' for numerical columns
    numerical_columns = ["Augmentation", "Promotion"]
    
    for column in numerical_columns:
        if column in df.columns:
            # Count missing values before cleaning
            missing_before = df[column].isna().sum()
            
            # Fill missing values with 0 (better for calculations)
            df[column] = df[column].fillna(0)
            
            # Convert to numeric type
            df[column] = pd.to_numeric(df[column], errors='coerce')
            
            missing_after = df[column].isna().sum()
    if mark== "Nyet":
        new_file=input("Write the cleaned data name ")
        output_file = os.path.join(output_folder, new_file)
        df.to_csv(output_file, index=False)
    else:
        output_file = os.path.join(output_folder, "cleaned_salary_data.csv")
        df.to_csv(output_file, index=False)
    
    print(f"Cleaned salary data saved to: {output_file}")
    return df
