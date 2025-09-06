[README.md](https://github.com/user-attachments/files/22190109/README.md)
# Pusula_Didar_Nur_Bilgin

**Name:** Didar Nur Bilgin  
**Email:** didarbillgin@gmail.com  

---

## Overview

This project was developed as part of the Talent Academy Case. The aim is to preprocess, analyze, and visualize medical dataset records. The pipeline handles data loading, normalization, imputation, missing value analysis, and visualization.

---

## Project Structure

```
Pusula_Didar_Nur_Bilgin/
├── data/                         
│   ├── Talent_Academy_Case_DT_2025.xlsx
│   └── output.xlsx
├── reports/                      
│   └── figures/
├── scripts/                     
│   └── run_viz.py
├── src/                        
│   ├── data/
│   │   └── load_data.py
│   ├── preprocessing/
│   │   ├── normalization/
│   │   │   ├── pipeline.py
│   │   │   ├── text.py
│   │   │   ├── multivalue.py
│   │   │   └── numeric.py
│   │   └── postprocess/
│   │       └── convert_numeric.py
│   ├── eda/
│   │   └── missing_analyzer.py
│   └── visualization/
│       └── data_viz.py
├── impute/
│   ├── pipeline_impute.py
│   ├── columns/
│   │   ├── impute_gender.py
│   │   ├── impute_chronic.py
│   │   ├── impute_allergy.py
│   │   ├── impute_diagnosis.py
│   │   ├── impute_treatment.py
│   │   ├── impute_sites.py
│   │   └── impute_department.py
│   └── strategies/
│       ├── patient_majority.py
│       ├── patient_majority_runner.py
│       ├── group_mode.py
│       ├── group_median.py
│       └── knn_categorical.py
├── main.py
├── requirements.txt
├── README.md
└── EDA_Report.txt
```

---

## Steps Implemented

1. **Data Loading**
   - Load Excel dataset from `data/`.
   - Convert empty strings to `NaN`.

2. **Normalization**
   - Clean text columns (lowercase, strip).
   - Normalize multi-value columns (comma-separated).
   - Apply numeric rules (bounds for valid ranges).

3. **Imputation**
   - Patient majority rule.
   - Group mode imputation.
   - KNN-based categorical imputation.
   - Fallback values for remaining missing data.

4. **EDA (Exploratory Data Analysis)**
   - Missing value summary (before and after imputation).
   - Exported as CSV under `reports/`.

5. **Visualization**
   - Age group × diagnosis count.
   - Gender × diagnosis distribution.
   - Diagnosis share pie chart.

6. **Postprocessing**
   - Convert treatment duration (`TedaviSuresi`) and application duration (`UygulamaSuresi`) to numeric fields with consistent units.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/didarbilgin/Pusula_Didar_Nur_Bilgin.git
   cd Pusula_Didar_Nur_Bilgin
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place the input file under `data/`:
   - Example: `data/Talent_Academy_Case_DT_2025.xlsx`

4. Run the main pipeline:
   ```bash
   python main.py
   ```

5. Run visualization separately (optional):
   ```bash
   python -m scripts.run_viz --input data/output.xlsx
   ```

---

## Output

- Cleaned dataset: `data/output.xlsx`  
- Missing reports: `reports/missing_before.csv`, `reports/missing_after.csv`  
- Visualizations: `reports/figures/`
  
---
## Documentation
- [Pusula_Didar_Nur_Bilgin.pdf](https://github.com/user-attachments/files/22190153/Pusula_Didar_Nur_Bilgin.pdf)


---

## Author

Didar Nur Bilgin  
didarbillgin@gmail.com  
