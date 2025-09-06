import pandas as pd
from typing import List, Optional

class PatientMajority:
    #hasta bazlı çoğunluk ve bağlam-temelli konsensus doldurma
    def __init__(self, patient_col: str = "HastaNo", min_ratio: float = 0.55):
        #hasta kimlik kolonu ve çoğunluk oran eşiği
        self.patient_col = patient_col
        self.min_ratio = float(min_ratio)

    @staticmethod
    def _is_missing(s: pd.Series) -> pd.Series:
        #nan ya da boş string kontrolü
        return s.isna() | s.eq("")

    def apply(self, df: pd.DataFrame, col: str) -> int:
        #eski davranış: sadece hasta bazlı çoğunluk ile doldur
        if self.patient_col not in df.columns or col not in df.columns:
            print(f"[patient-majority] SKIP {col} (missing columns)")
            return 0

        miss = self._is_missing(df[col])
        if not miss.any():
            print(f"[patient-majority] SKIP {col} (no missing)")
            return 0

        #eksik olmayan satırlarda hasta bazında en sık değeri bul
        grouped = df.loc[~miss].groupby(self.patient_col)[col]
        maj = {}
        for pid, vals in grouped:
            vals = vals.dropna().astype(str)
            if vals.empty:
                continue
            vc = vals.value_counts()
            top_val, top_cnt = vc.index[0], int(vc.iloc[0])
            #yeterince baskınsa (oran eşiği) o değeri o hasta için seç
            if top_cnt >= max(2, self.min_ratio * len(vals)):
                maj[pid] = top_val

        #eksik satırlara çoğunluk değerini uygula
        filled = 0
        for i, row in df[miss].iterrows():
            pid = row[self.patient_col]
            if pid in maj:
                df.at[i, col] = maj[pid]
                filled += 1

        print(f"[patient-majority] {col}: +{filled}")
        return filled

    def apply_with_context(
        self,
        df: pd.DataFrame,
        col: str,
        same_as_cols: List[str],
        ignore_cols: Optional[List[str]] = None,
    ) -> int:
        #hasta+bağlam aynıysa ve grupta tek bir değer varsa eksikleri o değerle doldur
        if self.patient_col not in df.columns or col not in df.columns:
            print(f"[patient-majority ctx] SKIP {col} (missing columns)")
            return 0

        #bağlamdan hedef kolon ve ignore edilen kolonları çıkar
        ignore_cols = set(ignore_cols or [])
        ctx = [c for c in same_as_cols if c in df.columns and c != col and c not in ignore_cols]
        keys = [self.patient_col] + ctx
        if not ctx:
            print(f"[patient-majority ctx] SKIP {col} (no context after ignore)")
            return 0

        miss = self._is_missing(df[col])
        if not miss.any():
            print(f"[patient-majority ctx] SKIP {col} (no missing)")
            return 0

        #bağlam anahtarları dolu ve hedefi dolu satırlarla konsensus tablosu kur
        non_missing = df.loc[~miss, keys + [col]].copy()
        for k in keys:
            non_missing = non_missing[~(non_missing[k].isna() | non_missing[k].eq(""))]
        non_missing = non_missing[~(non_missing[col].isna() | non_missing[col].eq(""))]
        if non_missing.empty:
            print(f"[patient-majority ctx] {col}: no usable rows")
            return 0

        #grup içinde tek benzersiz değer şartını kontrol et
        nunique = non_missing.groupby(keys, dropna=False)[col].nunique()
        ok_idx = nunique[nunique == 1].index
        if len(ok_idx) == 0:
            print(f"[patient-majority ctx] {col}: no consensus groups")
            return 0

        #her konsensus grubunun değerini haritalandır
        value_map = (
            non_missing.groupby(keys, dropna=False)[col]
            .agg(lambda s: s.iloc[0])
            .to_dict()
        )

        #eksikleri doldur
        filled = 0
        for i, row in df[miss].iterrows():
            key = tuple(row.get(k) for k in keys)
            #anahtarın eksik veya boş olmamasını sağla
            if any(pd.isna(k) or (isinstance(k, str) and k == "") for k in key):
                continue
            if key in ok_idx and key in value_map:
                df.at[i, col] = value_map[key]
                filled += 1

        print(f"[patient-majority ctx] {col}: +{filled} via ({', '.join(keys)}) [consensus]")
        return filled