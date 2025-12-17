import pandas as pd
import os

def clean_employee_data(input_file=None, output_folder=None):

    #Variable to customize output name file
    mark="else"
    
    if input_file is None:
        input_file = os.path.join("data", "Table_salarie.xlsx")
    else:
        file=input("Write the name of the correct file ")
        input_file = os.path.join("data", file)
        mark="Nyet"
    if output_folder is None:
        output_folder = "cleaned_data"
    
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Reading employee data from: {input_file}")
    df = pd.read_excel(input_file)
    
    # COLUMNS TO REMOVE (for privacy and irrevelent for calculus)
    columns_to_remove = ["Prénom/Nom", "Telephone"]
    
    for column in columns_to_remove:
        if column in df.columns:
            df = df.drop(columns=column)
    
    categorical_columns = ["Etat Civil", "Sexe"]
    
    for column in categorical_columns:
        if column in df.columns:
            # Fill empty values with some text
            df[column] = df[column].fillna("Not specified")
            # Remove extra spaces
            df[column] = df[column].str.strip()
            
            unique_values = df[column].nunique()
    
    if mark== "Nyet":
        new_file=input("Write the cleaned data name ")
        output_file = os.path.join(output_folder, new_file)
        df.to_csv(output_file, index=False)
    else:
        output_file = os.path.join(output_folder, "cleaned_employee_data.csv")
        df.to_csv(output_file, index=False)
    
    print(f"Cleaned employee data saved to: {output_file}")
    return df
