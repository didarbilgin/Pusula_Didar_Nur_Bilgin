import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
from collections import Counter

class KNNCategorical:
    #kategorik hedefi komşuluk oylamasıyla doldurur (k-nn + çoğunluk)
    def __init__(self, k: int = 7, min_support: int = 4):
        #k: komşu sayısı, min_support: oylamada atanacak sınıfın en az kaç oy alması gerektiği
        self.k = int(k)
        self.min_support = int(min_support)

    def apply(self, df: pd.DataFrame, target_col: str, feature_cols: list[str]) -> int:
        #hedef kolonu ve eksik maskesini hazırla
        if target_col not in df.columns:
            print(f"[knn] SKIP {target_col} (missing column)")
            return 0
        miss = df[target_col].isna() | df[target_col].eq("")
        if not miss.any():
            print(f"[knn] SKIP {target_col} (no missing)")
            return 0

        #özellikleri doğrula (hedefi hariç tut)
        feats = [c for c in feature_cols if c in df.columns and c != target_col]
        if not feats:
            print(f"[knn] SKIP {target_col} (no features)")
            return 0

        #eğitim kümesi: hedefi dolu satırlar
        train = df.loc[~miss, feats + [target_col]].copy()
        if train.empty:
            print(f"[knn] SKIP {target_col} (no training rows)")
            return 0

        #özellikleri sayısal/kategorik ayır
        num = [c for c in feats if pd.api.types.is_numeric_dtype(df[c])]
        cat = [c for c in feats if c not in num]

        #kategorikleri one-hot encode et
        ohe = OneHotEncoder(handle_unknown="ignore", sparse=False)
        X_cat_tr = ohe.fit_transform(train[cat]) if cat else np.empty((len(train), 0))
        #sayısalları ölçekle
        scaler = StandardScaler()
        X_num_tr = scaler.fit_transform(train[num]) if num else np.empty((len(train), 0))

        #eğitim matrisi ve etiket
        X_tr = np.hstack([X_num_tr, X_cat_tr])
        y_tr = train[target_col].astype(str).values

        #komşu sayısını mevcut örnek sayısına göre ayarla
        k = self.k if len(X_tr) >= self.k else max(1, len(X_tr))
        knn = NearestNeighbors(n_neighbors=k, metric="euclidean")
        knn.fit(X_tr)

        #test kümesi: hedefi eksik satırlar
        test = df.loc[miss, feats].copy()
        X_cat_te = ohe.transform(test[cat]) if cat else np.empty((len(test), 0))
        X_num_te = scaler.transform(test[num]) if num else np.empty((len(test), 0))
        X_te = np.hstack([X_num_te, X_cat_te])

        #komşuları bul ve çoğunluk oylaması yap
        idxs = knn.kneighbors(X_te, return_distance=False)
        filled = 0
        for row_idx, neigh_idx in zip(test.index, idxs):
            vals = y_tr[neigh_idx]
            top_val, top_cnt = Counter(vals).most_common(1)[0]
            if top_cnt >= self.min_support:
                df.at[row_idx, target_col] = top_val
                filled += 1

        print(f"[knn] {target_col}: +{filled} (k={k}, min_support={self.min_support})")
        return filled