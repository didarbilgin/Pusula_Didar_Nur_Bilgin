import pandas as pd

class GroupMedian:
    #grup bazlı medyan imputasyonu: anahtarlara göre hedef sayısal kolonu medyan ile doldurur
    def __init__(self, min_group_size: int = 3):
        #min_group_size: bir grubun medyanının kullanılabilmesi için gereken en az örnek sayısı
        self.min_group_size = int(min_group_size)

    def apply(self, df: pd.DataFrame, target_col: str, group_by_cols: list) -> int:
        #hedef kolonu kontrol et
        if target_col not in df.columns:
            print(f"[group-median] SKIP {target_col} (missing column)")
            return 0

        #yalnızca sayısal hedeflerde çalışmak güvenli
        if not pd.api.types.is_numeric_dtype(df[target_col]):
            print(f"[group-median] SKIP {target_col} (non-numeric target)")
            return 0

        #eksik maskesi
        miss = df[target_col].isna()
        if not miss.any():
            print(f"[group-median] SKIP {target_col} (no missing)")
            return 0

        #gruplama anahtarlarını doğrula
        keys = [c for c in group_by_cols if c in df.columns]
        if not keys:
            print(f"[group-median] SKIP {target_col} (no group keys)")
            return 0

        #grup istatistiği için anahtarları boş olmayan ve hedefi dolu satırlar
        non_missing = df.loc[~miss, [target_col] + keys].copy()
        for k in keys:
            non_missing = non_missing[~(non_missing[k].isna() | non_missing[k].eq(""))]
        non_missing = non_missing.dropna(subset=[target_col])
        if non_missing.empty:
            print(f"[group-median] SKIP {target_col} (no rows)")
            return 0

        #grup medyanı ve grup büyüklüğü
        g = non_missing.groupby(keys)
        med = g[target_col].median()
        cnt = g.size()

        #yeterli destekli gruplar
        valid_idx = cnt[cnt >= self.min_group_size].index
        med = med.loc[med.index.isin(valid_idx)]
        mapping = med.to_dict()
        if not mapping:
            print(f"[group-median] {target_col}: no valid groups")
            return 0

        #eksikleri doldur
        filled = 0
        for i, row in df[miss].iterrows():
            key = tuple(row.get(c) for c in keys)
            #anahtarların herhangi biri eksik/boşsa atla
            if any(pd.isna(k) or (isinstance(k, str) and k == "") for k in key):
                continue
            if key in mapping:
                df.at[i, target_col] = mapping[key]
                filled += 1

        print(f"[group-median] {target_col}: +{filled} (valid groups={len(valid_idx)})")
        return filled