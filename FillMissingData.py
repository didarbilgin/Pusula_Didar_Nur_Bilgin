import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer

class FillMissingData:
    def __init__(self, data):
        self.data = data  
        self.fillMissingData()

    def fillMissingData(self):
        # Select only numeric columns
        numeric_data = self.data.select_dtypes(include=['float64', 'int64'])
        
        # Fill missing numeric data using KNNImputer
        imputer = KNNImputer(n_neighbors=10)
        data_filled_numeric = pd.DataFrame(imputer.fit_transform(numeric_data), columns=numeric_data.columns)

        # Fill missing categorical data using SimpleImputer
        categorical_data = self.data.select_dtypes(include=['object'])
        imputer = SimpleImputer(strategy='most_frequent')
        data_filled_categorical = pd.DataFrame(imputer.fit_transform(categorical_data), columns=categorical_data.columns)
        
        # Update the original DataFrame
        self.data[numeric_data.columns] = data_filled_numeric  # Reinsert numeric data
        self.data[categorical_data.columns] = data_filled_categorical  # Reinsert categorical data

        return self.data