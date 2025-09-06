import numpy as np
import pandas as pd

class TextNormalizer:
    #belirtilen kolonlarda string normalizasyonu yapar (trim + küçük harf + boşları NaN)
    def __init__(self, cols):
        self.cols = cols or []

    @staticmethod
    def _norm_str(x):
        #gelen değer string ise boşlukları kırpar ve küçük harfe çevirir
        if isinstance(x, str):
            x = x.strip().casefold()
            return x if x else np.nan
        return x

    def apply(self, df):
        #dataframe üzerinde çalışır ve kopyasını döner
        df = df.copy()
        for c in self.cols:
            if c in df.columns:
                s = df[c]
                #object olmayan tipleri string değilse NaN yap
                if s.dtype != "object":
                    s = s.where(s.apply(lambda v: isinstance(v, str)), np.nan)
                #string kolonları normalize et
                df[c] = s.astype("object").apply(self._norm_str)
        return df