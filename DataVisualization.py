import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    def __init__(self, data):
        self.data = data
        self.histogram()
        self.numeric_columns()  
        self.categoric_columns()  
        self.heatmap()  
        
    # Create a histogram for each numeric column
    def histogram(self):
        plt.figure(figsize=(10, 8))
        for column in self.data.select_dtypes(include=['float64', 'int64']).columns:
            sns.histplot(self.data[column], bins=30, kde=True, label=column, stat="density", alpha=0.5)
        
        # Set the title and labels for the histogram
        plt.title('Distributions of Numeric Variables')
        plt.xlabel('Values')
        plt.ylabel('Density')
        plt.legend()
        plt.show()
        
    # Get numeric columns for scatterplot generation
    def numeric_columns(self):  
        numeric_columns = self.data.select_dtypes(include=['float64', 'int64']).columns
        for i in range(len(numeric_columns)):
            for j in range(i + 1, len(numeric_columns)):
                # Create a scatterplot for each pair of numeric columns
                self.scatterplot(numeric_columns[i], numeric_columns[j])
                
    # Get categorical columns for pie chart generation
    def categoric_columns(self):
        categoric_columns = self.data.select_dtypes(include=['object']).columns
        for column in categoric_columns:
            # Create a pie chart for each categorical column
            self.pie_chart(column)
            
    # Generate a scatterplot to show the relationship between two numeric columns
    def scatterplot(self, x, y):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=self.data[x], y=self.data[y])
        plt.title(f'Relationship between {x} and {y}')
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    # Create a heatmap to visualize the correlation matrix of numeric columns
    def heatmap(self):
        plt.figure(figsize=(12, 8))
        numeric_data = self.data.select_dtypes(include=['float64', 'int64'])  # Only get numeric data
        correlation_matrix = numeric_data.corr()  # Get the correlation matrix
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Heatmap')
        plt.show()
       
    # Generate a pie chart for a given categorical column 
    def pie_chart(self, column):
        plt.figure(figsize=(8, 8))
        self.data[column].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
        plt.title(f'{column} Pie Chart')
        plt.ylabel('')  
        plt.show()