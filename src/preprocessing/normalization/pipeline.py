import pandas as pd
from .text import TextNormalizer
from .multivalue import MultiValueNormalizer
from .numeric import NumericNormalizer

class NormalizationPipeline:
    #metin, çoklu-değer ve sayısal normalizasyonu sırayla çalıştırır
    def __init__(self, text_cols=None, multivalue_cols=None, numeric_rules=None):
        #bileşenleri hazırla
        self.text_norm = TextNormalizer(text_cols or [])
        self.multi_norm = MultiValueNormalizer(multivalue_cols or [])
        self.num_norm = NumericNormalizer(numeric_rules or {})

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        #dataframe kopyası üstünde adım adım uygula
        df = self.text_norm.apply(df)
        df = self.multi_norm.apply(df)
        df = self.num_norm.apply(df)
        return df