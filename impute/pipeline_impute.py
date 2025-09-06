import pandas as pd
from impute.columns.impute_gender import ImputeGender
from impute.columns.impute_chronic import ImputeChronic
from impute.columns.impute_allergy import ImputeAllergy
from impute.columns.impute_diagnosis import ImputeDiagnosis
from impute.columns.impute_treatment import ImputeTreatment
from impute.columns.impute_sites import ImputeSites
from impute.columns.impute_department import ImputeDepartment
from impute.strategies.patient_majority_runner import PatientMajorityRunner

def run_imputation(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    print("== IMPUTE PIPELINE ==")

    #hasta bazlı context-majority doldurma
    df = PatientMajorityRunner().run(df)

    #kolon bazlı imputation adımları
    ImputeGender().run(df)
    ImputeChronic(use_knn=True).run(df)
    ImputeAllergy(use_knn=True).run(df)
    ImputeDiagnosis().run(df)
    ImputeTreatment().run(df)
    ImputeSites().run(df)
    ImputeDepartment(use_knn=True).run(df)

    print("== IMPUTE DONE ==")
    return df