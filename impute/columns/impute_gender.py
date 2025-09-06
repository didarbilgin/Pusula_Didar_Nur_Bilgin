import pandas as pd
from impute.strategies.patient_majority import PatientMajority
from impute.strategies.group_mode import GroupMode

class ImputeGender:
    #cinsiyet imputasyonu: hasta içi çoğunluk→grup modu(tanı)→fallback(bilinmiyor)
    def __init__(self, min_group_size=3, min_ratio=0.55):
        #stratejileri hazırla
        self.pm = PatientMajority()
        self.gm = GroupMode(min_group_size, min_ratio)

    def run(self, df: pd.DataFrame) -> None:
        target = "Cinsiyet"

        #hasta içi çoğunluk
        self.pm.apply(df, target)

        #grup modu: aynı tanıya sahip kayıtlarda en sık cinsiyet
        self.gm.apply(df, target_col=target, group_by_cols=["Tanilar"])

        #fallback: boş kalanları 'bilinmiyor' yap
        miss = df[target].isna() | df[target].eq("")
        if miss.any():
            df.loc[miss, target] = "bilinmiyor"
            print(f"[fallback] {target}: +{int(miss.sum())}")