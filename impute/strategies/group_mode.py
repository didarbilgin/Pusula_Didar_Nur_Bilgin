import pandas as pd

class GroupMode:
    #grup bazlı mod imputasyonu: belirli anahtarlara göre en sık görülen değeri eksiklere atar
    def __init__(self, min_group_size: int = 3, min_ratio: float = 0.55):
        #bir grubun dikkate alınması için gereken en az satır
        self.min_group_size = int(min_group_size)
        #grubun tepesindeki değerin baskınlığı
        self.min_ratio = float(min_ratio)

    @staticmethod
    def _is_missing(s: pd.Series) -> pd.Series:
        #eksik tanımı: NaN ya da boş string
        return s.isna() | s.eq("")

    def apply(self, df: pd.DataFrame, target_col: str, group_by_cols: list) -> int:
        #hedef kolonu kontrol et
        if target_col not in df.columns:
            print(f"[group-mode] SKIP {target_col} (missing column)")
            return 0

        #eksik maskesi
        miss = self._is_missing(df[target_col])
        if not miss.any():
            print(f"[group-mode] SKIP {target_col} (no missing)")
            return 0

        #gruplama anahtarlarını doğrula
        keys = [c for c in group_by_cols if c in df.columns]
        if not keys:
            print(f"[group-mode] SKIP {target_col} (no group keys)")
            return 0

        #grup istatistiği için sadece hedefi ve anahtarları dolu/boş olmayan satırlar
        non_missing = df.loc[~miss, [target_col] + keys].copy()
        for k in keys:
            non_missing = non_missing[~(non_missing[k].isna() | non_missing[k].eq(""))]
        non_missing = non_missing[~self._is_missing(non_missing[target_col])]
        if non_missing.empty:
            print(f"[group-mode] SKIP {target_col} (no rows)")
            return 0

        #her anahtar kombinasyonu için mod ve mod sayısı
        g = non_missing.groupby(keys)
        mode_val = g[target_col].agg(lambda s: s.value_counts().idxmax())
        mode_cnt = g[target_col].agg(lambda s: s.value_counts().iloc[0])
        g_sizes = g.size()

        #geçerli gruplar: hem örnek sayısı hem de baskınlık eşiğini aşmalı
        valid_mask = (g_sizes >= self.min_group_size) & ((mode_cnt / g_sizes) >= self.min_ratio)
        mapping = mode_val[valid_mask].to_dict()
        if not mapping:
            print(f"[group-mode] {target_col}: no valid groups")
            return 0

        #eksikleri doldur
        filled = 0
        for i, row in df[miss].iterrows():
            key = tuple(row.get(c) for c in keys)
            #anahtarların herhangi biri eksik/boşsa atla
            if any(pd.isna(k) or (isinstance(k, str) and k == "") for k in key):
                continue
            if key in mapping and (pd.isna(df.at[i, target_col]) or df.at[i, target_col] == ""):
                df.at[i, target_col] = mapping[key]
                filled += 1

        print(f"[group-mode] {target_col}: +{filled} (valid groups={int(valid_mask.sum())})")
        return filled