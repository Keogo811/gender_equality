import pandas as pd

# defines a function
def file1():
    # assigns a variable to the file path
    file_path1 = "/Users/sureyeahman/Downloads/projet3_datasets/projet3/Table_Info_pro.csv"
    
    # reads data from the csv file
    df = pd.read_csv(file_path1)
    
    # deletes the whole row if all the data is repeated
    df = df.drop_duplicates()
    # prints the data to some limit in ide's terminal
    print(df)
    # assigns a variable to the new file path
    output_file_path = "/Users/sureyeahman/Downloads/projet3_datasets/output_Project/cleaned_table_Info_Pro.csv"
    
    # saves the file to the new file path
    df.to_csv(output_file_path)
file1()
