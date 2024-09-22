# Pusula_Didar_Nur_Bilgin

Didar Nur Bilgin - didarbillgin@gmail.com

## Overview
This project aims to preprocess and analyze data related to side effects of medications. It utilizes various data processing techniques to ensure data quality and provides visual insights through graphical representations.

## Technologies Used
- Python
- Pandas
- Matplotlib
- Seaborn
- scikit-learn
- OpenPyXL (for Excel file handling)

## Installation
To run this project, you need to have Python installed on your system. You can install the necessary libraries using pip. Run the following command in your terminal:

```bash
pip install pandas matplotlib seaborn scikit-learn openpyxl
```

## Installation Instructions

### Step-by-Step Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/didarbilgin/Pusula_Didar_Nur_Bilgin.git
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
      
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install the required libraries**:

    ```bash
    pip install pandas matplotlib seaborn scikit-learn openpyxl
    ```

5. **Run the project**:

    ```bash
    python Main.py
    ```

### Output

After running the project, an Excel file will be generated with the processed data in the project folder and various graphs such as histograms, scatter plots, heatmaps, and pie charts will be displayed on the screen.

## Findings
[steps_and_findings.txt](https://github.com/user-attachments/files/17090482/steps_and_findings.txt)
Didar Nur Bilgin - didarbillgin@gmail.com


Data Exploration and Preprocessing Summary

	1.	Research and Familiarization: The individual conducted a thorough exploration of the Pandas, Matplotlib, and Seaborn libraries. This included understanding their functionalities, strengths, and how they could be applied effectively in data processing and visualization tasks.
	2.	Data Processing Plan: A structured plan was developed to manage the data preprocessing workflow. This plan outlined the steps required to ensure the data was handled systematically and efficiently throughout the analysis.
	3.	Data Acquisition: Using the Pandas library, the individual successfully read the provided Excel dataset, extracting the relevant data for further analysis.
	4.	Model Class Development: To facilitate the analysis, a model class was created, which included defining appropriate variables that corresponded to the dataset’s structure and requirements.
	5.	Data Normalization: The individual examined the dataset to identify necessary normalization procedures. This involved establishing acceptable value ranges and applying standardization techniques to ensure data consistency.
	6.	Handling Missing Values: The analysis revealed the presence of missing values within the dataset. To address this, KNNImputer was utilized to fill in missing numerical data, while SimpleImputer was employed for categorical variables. This dual approach ensured comprehensive treatment of missing values.
	7.	Output Verification: A new Excel file was generated containing the filled data. This step allowed for ongoing verification and tracking of changes throughout the preprocessing phase.
	8.	Data Mapping: The cleaned and updated data was assigned to the predefined model variables, ensuring alignment between the dataset and the analytical framework.
	9.	Data Visualization: Finally, the individual enhanced the understanding of the dataset by visualizing the data through various graphical representations, including histograms, scatter plots, heatmaps, and pie charts. These visualizations served to reinforce the findings and provide clear insights into the data’s structure and relationships.

