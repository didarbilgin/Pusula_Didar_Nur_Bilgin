import pandas as pd
from impute.strategies.patient_majority import PatientMajority
from impute.strategies.group_mode import GroupMode

class ImputeTreatment:
    #tedavi adı imputasyonu: hasta içi çoğunluk → grup modu → fallback
    def __init__(self, min_group_size=3, min_ratio=0.55):
        #patientMajority ve groupMode stratejilerini hazırla
        self.pm = PatientMajority()
        self.gm = GroupMode(min_group_size, min_ratio)

    def run(self, df: pd.DataFrame) -> None:
        #hedef kolon
        target = "TedaviAdi"

        #hasta içi çoğunluk: aynı hastanın tekrarlarında tek baskın değer varsa onu doldur
        self.pm.apply(df, target)

        #grup modu: sızıntı olmaması için tedavi süresini anahtar yapma
        #tanı+uygulama yeri → mod
        self.gm.apply(df, target_col=target, group_by_cols=["Tanilar", "UygulamaYerleri"])
        #sadece tanı → mod
        self.gm.apply(df, target_col=target, group_by_cols=["Tanilar"])
        #sadece uygulama yeri → mod
        self.gm.apply(df, target_col=target, group_by_cols=["UygulamaYerleri"])

        #fallback: hala boş kalanları 'belirtilmemiş' yap
        miss = df[target].isna() | df[target].eq("")
        if miss.any():
            df.loc[miss, target] = "belirtilmemiş"
            print(f"[fallback] {target}: +{int(miss.sum())}")