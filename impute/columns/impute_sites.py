import pandas as pd
from impute.strategies.patient_majority import PatientMajority
from impute.strategies.group_mode import GroupMode

class ImputeSites:
    #uygulama yeri imputasyonu: hasta içi çoğunluk → grup modu → fallback
    def __init__(self, min_group_size=3, min_ratio=0.55):
        #patientMajority ve groupMode stratejilerini hazırla
        self.pm = PatientMajority()
        self.gm = GroupMode(min_group_size, min_ratio)

    def run(self, df: pd.DataFrame) -> None:
        target = "UygulamaYerleri"

        #hasta içi çoğunluk
        self.pm.apply(df, target)

        #grup modu: tanı+tedavi, sadece tanı, sadece tedavi
        self.gm.apply(df, target_col=target, group_by_cols=["Tanilar", "TedaviAdi"])
        self.gm.apply(df, target_col=target, group_by_cols=["Tanilar"])
        self.gm.apply(df, target_col=target, group_by_cols=["TedaviAdi"])

        #fallback: boşları 'belirtilmemiş' yap
        miss = df[target].isna() | df[target].eq("")
        if miss.any():
            df.loc[miss, target] = "belirtilmemiş"
            print(f"[fallback] {target}: +{int(miss.sum())}")