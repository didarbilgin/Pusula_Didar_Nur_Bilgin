import pandas as pd
from impute.strategies.patient_majority import PatientMajority
from impute.strategies.group_mode import GroupMode
from impute.strategies.knn_categorical import KNNCategorical

class ImputeDepartment:
    #bölüm imputasyonu: hasta içi çoğunluk→grup modu→opsiyonel knn→fallback
    def __init__(self, min_group_size=3, min_ratio=0.55, use_knn=True):
        #strateji nesneleri
        self.pm = PatientMajority()
        self.gm = GroupMode(min_group_size, min_ratio)
        #knn istenirse hazırla (k=7, komşularda en az 4 aynı sınıf şartı)
        self.knn = KNNCategorical(k=7, min_support=4) if use_knn else None

    def run(self, df: pd.DataFrame) -> None:
        target = "Bolum"

        #hasta içi çoğunluk
        self.pm.apply(df, target)

        #grup modu: tanı+tedavi ile en sık bölüm
        self.gm.apply(df, target_col=target, group_by_cols=["Tanilar", "TedaviAdi"])

        #knn ile doldurma (varsa)
        if self.knn:
            #özellikler: yaş(sayısal) + tanı/tedavi/uygulama yeri/cinsiyet/uyruk(kategorik)
            feats = ["Yas", "Tanilar", "TedaviAdi", "UygulamaYerleri", "Cinsiyet", "Uyruk"]
            self.knn.apply(df, target_col=target, feature_cols=feats)

        #fallback: kalan boşları 'belirtilmemiş' yap
        miss = df[target].isna() | df[target].eq("")
        if miss.any():
            df.loc[miss, target] = "belirtilmemiş"
            print(f"[fallback] {target}: +{int(miss.sum())}")