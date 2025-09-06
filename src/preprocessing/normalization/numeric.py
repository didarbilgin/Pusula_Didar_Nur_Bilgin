import pandas as pd

class NumericNormalizer:
    #sayısal kolonları verilen alt-üst sınırlara göre normalize eder
    def __init__(self, rules):
        #rules dict biçiminde: {kolon: (min, max)}
        self.rules = rules or {}

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        #dataframe kopyası üstünde çalış
        df = df.copy()
        for column, bounds in self.rules.items():
            if column not in df.columns:
                continue
            lo, hi = bounds
            #sayısal değer dışındakileri NaN yap
            s = pd.to_numeric(df[column], errors="coerce")
            #alt sınır uygula
            if lo is not None:
                s = s.mask(s < lo)
            #üst sınır uygula
            if hi is not None:
                s = s.mask(s > hi)
            df[column] = s
        return df