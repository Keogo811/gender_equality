import pandas as pd
import os

def clean_professional_data(input_file=None, output_folder=None):
    """
    Cleans professional information data
    and adaptable to any file path
    """
    #Variable to customize output name file
    mark="else"

    # Path of the unclean data
    if input_file is None:
        input_file = os.path.join("data", "Table_Info_pro.xlsx")
    else:
        file=input("Write the name of the correct file ")
        input_file = os.path.join("data", file)
        mark="Nyet"
    if output_folder is None:
        output_folder = "cleaned_data"
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Read the data
    print(f"Reading data from: {input_file}")
    df = pd.read_excel(input_file)
    
    # Remove duplicate rows
    initial_count = len(df)
    df = df.drop_duplicates()
    final_count = len(df)
    duplicates_removed = initial_count - final_count
    
    # Save cleaned file in the right folder
    if mark== "Nyet":
        new_file=input("Write the cleaned data name ")
        output_file = os.path.join(output_folder, new_file)
        df.to_csv(output_file, index=False)
    else:
        output_file = os.path.join(output_folder, "cleaned_professional_data.csv")
        df.to_csv(output_file, index=False)
    
    print(f"Cleaned data saved to: {output_file}")
    return df
