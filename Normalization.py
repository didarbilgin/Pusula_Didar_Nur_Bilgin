import numpy as np
import pandas as pd

class Normalization:
    def __init__(self, data):
        self.data = data
        self.columnsToCheck()  
        self.normalize()  

    def columnsToCheck(self):
        # List of columns that are expected to contain string values
        self.stringValueColumns = ['Cinsiyet', 'Uyruk', 'Il', 'Ilac_Adi', 'Yan_Etki', 'Alerjilerim', 'Kronik Hastaliklarim', 
                                   'Baba Kronik Hastaliklari', 'Anne Kronik Hastaliklari', 'Kiz Kardes Kronik Hastaliklari', 
                                   'Erkek Kardes Kronik Hastaliklari', 'Kan Grubu']
        
        # List of columns that are expected to contain numeric values
        self.numericValueColumns = ['Kullanici_id','Kilo','Boy']
        
        
    def normalize(self):
        # Check that specified columns contain string values
        for strColumn in self.stringValueColumns:
            self.checkIfString(strColumn)
            
        # Validate numerical data in specified columns
        for numColumn in self.numericValueColumns:
            self.checkNumericalData(numColumn)
        
        return self.data
        
  
        
    def checkNumericalData(self,column):        
        # Mark negative user_id values as missing (NaN)
        self.data[column] = np.where(self.data[column] < 0, np.nan, self.data[column])
        
        # Mark unusually high weight values as missing
        self.data['Kilo'] = np.where(self.data['Kilo'] > 250, np.nan, self.data['Kilo'])
        
        # Mark unusually high height values as missing
        self.data['Boy'] = np.where(self.data['Boy'] > 300, np.nan, self.data['Boy'])
        
        return self.data
         
    def checkIfString(self, column):
        # Check if the values in the column are of type string
        if self.data[column].dtype != object:
            self.data[column] = np.where(self.data[column].apply(lambda x: not isinstance(x, str)), np.nan, self.data[column])
            
        return self.data