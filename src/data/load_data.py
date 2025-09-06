import pandas as pd
import os

class LoadData:
    def __init__(self, input_path: str = "data/Talent_Academy_Case_DT_2025.xlsx"):
        #veri dosyasının yolunu kaydet
        self.input_path = input_path

    def load(self) -> pd.DataFrame:
        #dosya yolunu kontrol et
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"dosya bulunamadı: {self.input_path}")

        #excel dosyasını oku
        df = pd.read_excel(self.input_path)

        #boş stringleri nan yap
        df = df.applymap(lambda x: x if not (isinstance(x, str) and x.strip() == "") else pd.NA)

        return df