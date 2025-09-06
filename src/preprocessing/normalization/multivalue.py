import numpy as np
import pandas as pd

class MultiValueNormalizer:
    #virgüllerle ayrılmış çoklu değer kolonlarını normalize eder
    def __init__(self, cols):
        #normalize edilecek kolon listesi
        self.cols = cols or []

    @staticmethod
    def _fix_multi(val):
        #string değilse dokunma
        if not isinstance(val, str):
            return val
        #virgül ile ayır, boşlukları temizle, küçük harfe çevir
        toks = [t.strip().casefold() for t in val.split(",") if t.strip()]
        if not toks:
            return np.nan
        #tekrarları kaldır, sıralamayı koru
        seen, out = set(), []
        for t in toks:
            if t not in seen:
                seen.add(t)
                out.append(t)
        #tekrarları kaldırılmış string döndür
        return ", ".join(out)

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        #dataframe kopyası üzerinde çalış
        df = df.copy()
        for c in self.cols:
            if c in df.columns:
                #her hücreye fix_multi uygula
                df[c] = df[c].apply(self._fix_multi)
        return df