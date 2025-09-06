import pandas as pd
from impute.strategies.patient_majority import PatientMajority

class PatientMajorityRunner:
    #tüm kolonlar için patient-majority stratejisini tek yerden yönet
    CONTEXT_MAP = {
        "Tanilar": ["TedaviAdi", "UygulamaYerleri"],
        "TedaviAdi": ["Tanilar", "UygulamaYerleri"],
        "UygulamaYerleri": ["Tanilar", "TedaviAdi"],
        "KronikHastalik": ["Tanilar"],
        "Alerji": ["KronikHastalik", "Tanilar"],
        "Bolum": ["Tanilar", "TedaviAdi", "UygulamaYerleri"],
        "Cinsiyet": ["Tanilar"],
    }

    def __init__(self, patient_col: str = "HastaNo"):
        self.pm = PatientMajority(patient_col=patient_col)
        self.ignore_cols = [
            "TedaviSuresi","UygulamaSuresi",
            "TedaviSuresi_seans","UygulamaSuresi_dakika",
            "tedavisuresi_num","uygulamasuresi_num"
        ]

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        #önce context ile majority denemeleri
        for target, context in self.CONTEXT_MAP.items():
            if hasattr(self.pm, "apply_with_context"):
                self.pm.apply_with_context(
                    df,
                    col=target,
                    same_as_cols=context,
                    ignore_cols=self.ignore_cols
                )
            else:
                self.pm.apply(df, col=target)

        #kan grubu için: hasta-içi majority dene
        if "KanGrubu" in df.columns:
            filled = self.pm.apply(df, col="KanGrubu")
            #hala eksik varsa bilinmiyor ile doldur
            miss = df["KanGrubu"].isna() | df["KanGrubu"].eq("")
            if miss.any():
                df.loc[miss, "KanGrubu"] = "bilinmiyor"
                print(f"[fallback] KanGrubu: +{int(miss.sum())} filled with 'bilinmiyor'")

        return df