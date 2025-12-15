import os
import file1_improved
import file2_improved  
import file3_improved

def clean_all_data():
    """
    Clean all data files with one command
    """
    try:
        choice=input("Default uncleaned data name file or not? Y/N ")
        if choice == "Y":
            # Default name files
            #Cleaning professional data
            professional_data = file1_improved.clean_professional_data()
        
            #Cleaning salary data
            salary_data = file2_improved.clean_salary_data()
        
            #Cleaning employee data
            employee_data = file3_improved.clean_employee_data()

        else:
            # Customized data name files
            professional_data = file1_improved.clean_professional_data(input_file="else", output_folder=None)
        
            salary_data = file2_improved.clean_salary_data(input_file="else", output_folder=None)
        
            employee_data = file3_improved.clean_employee_data(input_file="else", output_folder=None)

        print("Results saved to 'cleaned_data' folder")
        return professional_data, salary_data, employee_data
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("Please verify that:")
        print(" - openpyxl is installed")
        print(" - Excel files are not corrupted")
        print(" - Excel files are not currently open")
        print(" - Excel files names are well written")
        return None, None, None

if __name__ == "__main__":
    clean_all_data()



