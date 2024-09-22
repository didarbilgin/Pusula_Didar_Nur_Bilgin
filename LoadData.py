import pandas as pd
import os

class LoadData:
    def __init__(self):
        # Define the file path for the Excel file to be loaded
        self.file_path = os.path.join(os.path.dirname(__file__), 'data', 'side_effect_data 1.xlsx')
        self.data = None
        
    # Load the data from the specified Excel file    
    def load(self):
        self.data = pd.read_excel(self.file_path)
        return self.data   # Return the loaded data

