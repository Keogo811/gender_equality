import pandas as pd

# defines a function
def file2():
    # assigns a variable to the file path
    filepath2 = "/Users/sureyeahman/Downloads/projet3_datasets/projet3/Table_remuneration.csv"
    # reads data from the csv file
    df = pd.read_csv(filepath2)
    # replaces any whitespace or multiple whitespace with a single whitespace 
    df["Augmentation"] = df["Augmentation"].replace(r'^\s*$', 'NA', regex=True)
    
    # replaces single whitespace to Na 
    df["Augmentation"] = df['Augmentation'].fillna('NA')
    df["Promotion"] = df["Promotion"].replace(r'^\s*$', 'NA', regex=True)
    df["Promotion"] = df['Promotion'].fillna('NA')
    
    output_file_path = "/Users/sureyeahman/Downloads/projet3_datasets/output_Project/cleaned_table_Remuneration.csv"
    df.to_csv(output_file_path, index=False)
    print(df)
file2()    