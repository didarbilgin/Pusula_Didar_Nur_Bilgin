from LoadData import LoadData
from FillMissingData import FillMissingData
import DataModel as model  
from Normalization import Normalization
from DataMapper import DataMapper
from DataVisualization import DataVisualization
import os

class Main:
    def __init__(self):
        self.load_data()  
        self.normalize()  
        self.fill_data()  
        self.map()  
        self.visualize()  
        self.output()     

    # Load the data that has been given
    def load_data(self):
        self.data_loader = LoadData()
        self.data = self.data_loader.load()  
        self.original_data = self.data.copy() 
        print("Data loaded successfully.")
   
    # Normalize the data
    def normalize(self):
        normalizer = Normalization(self.data)
        self.data = normalizer.normalize()
        print("Data normalization completed.")
        
    # Fill missing data    
    def fill_data(self):
        self.data_filler = FillMissingData(self.data)  
        self.data = self.data_filler.fillMissingData()
        print("Missing values have been successfully filled.")

    # Map the updated data to model variables
    def map(self):
        DataMapper(self.data) 
        print("Data mapping completed.")
            
    # Create visual graphs from the data
    def visualize(self):
        DataVisualization(self.data)
        print("Visualizations have been created.")
        
    # Display the updated data with an Excel file
    def output(self):
        output_path = os.path.join(os.getcwd(), 'output.xlsx') 
        self.data.to_excel(output_path, index=False)         
        print("Output file has been created.")
        
if __name__ == "__main__":
    app = Main()