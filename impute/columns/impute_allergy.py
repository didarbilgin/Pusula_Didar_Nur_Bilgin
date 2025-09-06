import pandas as pd
from impute.strategies.patient_majority import PatientMajority
from impute.strategies.group_mode import GroupMode
from impute.strategies.knn_categorical import KNNCategorical

class ImputeAllergy:
    #alerji imputasyonu: hasta içi çoğunluk→opsiyonel knn→fallback
    def __init__(self, min_group_size=3, min_ratio=0.55, use_knn=True):
        #strateji nesneleri
        self.pm = PatientMajority()
        self.gm = GroupMode(min_group_size, min_ratio)
        #knn açık ise kur
        self.knn = KNNCategorical(k=7, min_support=4) if use_knn else None

    def run(self, df: pd.DataFrame) -> None:
        target = "Alerji"

        #hasta içi çoğunluk: aynı hastada en sık geçen alerjiyi eksiklere uygula
        self.pm.apply(df, target)

        #knn: yaş/tanı/tedavi/uygulama yeri/cinsiyet/uyruk/kronik/bölüm ile en yakın komşulardan etiketi al
        if self.knn:
            feats = ["Yas","Tanilar","TedaviAdi","UygulamaYerleri","Cinsiyet","Uyruk","KronikHastalik","Bolum"]
            self.knn.apply(df, target_col=target, feature_cols=feats)

        #fallback: hâlâ boş kalanlara 'yok' yaz
        miss = df[target].isna() | df[target].eq("")
        if miss.any():
            df.loc[miss, target] = "yok"
            print(f"[fallback] {target}: +{int(miss.sum())}")