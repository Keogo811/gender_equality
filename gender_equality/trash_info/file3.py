import pandas as pd

def file3():
    filepath3 = "/Users/sureyeahman/Downloads/projet3_datasets/projet3/Table_salarie.csv"
    
    df = pd.read_csv(filepath3)
    df = df.drop(columns= "Prénom/Nom")
    df = df.drop(columns= "Telephone")
    df["Etat Civil"] = df["Etat Civil"].replace(r'^\s*$',regex=True)
    df["Etat Civil"] = df["Etat Civil"].fillna('NA')
    
    output_file_path = "/Users/sureyeahman/Downloads/projet3_datasets/output_Project/cleaned_table_Salarie.csv"
    df.to_csv(output_file_path, index=False)
    
    print(df)
file3()    