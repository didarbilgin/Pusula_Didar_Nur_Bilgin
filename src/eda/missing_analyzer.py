import pandas as pd
from pathlib import Path

class MissingAnalyzer:
    #kolon bazında eksik değerleri analiz eder
    def __init__(self, df: pd.DataFrame):
        #analiz edilecek dataframe
        self.df = df

    def summary(self) -> pd.DataFrame:
        #toplam satır sayısı
        n = len(self.df)

        #NaN değerlerin sayısı
        nan_cnt = self.df.isna().sum()

        #boş string veya sadece boşluk içeren hücre sayısı (sadece object kolonlar için)
        blank_cnt = pd.Series(0, index=self.df.columns, dtype="int64")
        obj_cols = self.df.select_dtypes(include=["object"]).columns
        if len(obj_cols) > 0:
            blank_cnt.loc[obj_cols] = (
                self.df[obj_cols]
                .apply(lambda s: s.astype(str).str.strip().eq("").sum())
            )

        #toplam eksik = nan + boş
        total_missing = (nan_cnt + blank_cnt).astype("int64")

        #çıktı tablosu
        out = pd.DataFrame({
            "nan_count": nan_cnt,
            "blank_count": blank_cnt,
            "missing_count": total_missing,
            "missing_ratio": total_missing / max(n, 1)
        })
        #en çok eksik olana göre sırala
        return out.sort_values("missing_count", ascending=False)

    def save(self, path: str) -> None:
        #çıktıyı verilen dosya yoluna kaydeder
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.summary().to_csv(path, index=True)
        print(f"[MissingAnalyzer] saved -> {path}")