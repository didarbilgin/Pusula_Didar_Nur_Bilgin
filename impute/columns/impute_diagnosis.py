import pandas as pd
from impute.strategies.patient_majority import PatientMajority
from impute.strategies.group_mode import GroupMode

class ImputeDiagnosis:
    #tanı imputasyonu: hasta içi çoğunluk→grup modu(tedaviadı, uygulamayerleri→tedaviadı)→fallback(belirtilmemiş)
    def __init__(self, min_group_size=3, min_ratio=0.55):
        #strateji nesneleri
        self.pm = PatientMajority()
        self.gm = GroupMode(min_group_size, min_ratio)

    def run(self, df: pd.DataFrame) -> None:
        target = "Tanilar"

        #hasta içi çoğunluk
        self.pm.apply(df, target)

        #grup modu: (tedaviadı, uygulamayerleri) bir arada
        self.gm.apply(df, target_col=target, group_by_cols=["TedaviAdi","UygulamaYerleri"])

        #grup modu: sadece tedaviadı
        self.gm.apply(df, target_col=target, group_by_cols=["TedaviAdi"])

        #fallback: boş kalanları 'belirtilmemiş' yap
        miss = df[target].isna() | df[target].eq("")
        if miss.any():
            df.loc[miss, target] = "belirtilmemiş"
            print(f"[fallback] {target}: +{int(miss.sum())}")