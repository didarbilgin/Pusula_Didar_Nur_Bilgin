import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DataVisualization:
    def __init__(
        self,
        df: pd.DataFrame,
        outdir: str = "reports/figures",
    ):
        #girdi dataframe ve çıktı klasörünü kaydet
        self.df = df
        self.outdir = Path(outdir)
        #çıktı klasörünü oluştur
        self.outdir.mkdir(parents=True, exist_ok=True)


    def _save(self, name: str):
        #figürü diske kaydet
        fp = self.outdir / name
        plt.tight_layout()
        plt.savefig(fp, dpi=150, bbox_inches="tight")
        plt.close()
        return fp

    def _safe(self, s: str) -> str:
        #dosya adı için güvenli metin üret
        return s.replace("/", "-").replace(" ", "_")


    def age_group_vs_diagnosis_count(self):
        #amaç: hangi yaş grubunda daha fazla tanı var grafiği
        #kontrol: gerekli kolonlar var mı
        if "Yas" not in self.df.columns or "Tanilar" not in self.df.columns:
            return

        #tanısı boş olmayan kayıtları al
        df = self.df.copy()
        df = df[df["Tanilar"].notna() & (df["Tanilar"].astype(str).str.strip() != "")]
        if df.empty:
            return

        #yaş gruplarını oluştur
        bins = [0, 18, 30, 40, 50, 60, 70, 80, 120]
        labels = ["0-18","19-30","31-40","41-50","51-60","61-70","71-80","81+"]
        df["Yas_group"] = pd.cut(pd.to_numeric(df["Yas"], errors="coerce"), bins=bins, labels=labels, right=True)

        #grup bazında sayım yap
        grp = df.groupby("Yas_group").size().reindex(labels)
        grp = grp.fillna(0).astype(int)

        #bar grafik çiz
        plt.figure(figsize=(8,5))
        sns.barplot(x=grp.index.astype(str), y=grp.values)
        plt.title("Yaş Grubu × Tanı Sayısı")
        plt.xlabel("Yaş Grubu"); plt.ylabel("Kayıt Sayısı")
        self._save("age_group__diagnosis_count.png")

    def gender_by_top_diagnoses(self, topn: int = 10, min_count: int = 10, normalize_within_diag: bool = True):
        #amaç: cinsiyet × tanı (top-n tanı) yığılmış sütun grafiği
        #kontrol: gerekli kolonlar var mı
        need = {"Cinsiyet","Tanilar"}
        if not need.issubset(set(self.df.columns)):
            return

        #eksikleri temizle
        df = self.df.copy()
        df = df[
            df["Tanilar"].notna() & (df["Tanilar"].astype(str).str.strip() != "") &
            df["Cinsiyet"].notna() & (df["Cinsiyet"].astype(str).str.strip() != "")
        ]
        if df.empty:
            return

        #en sık görülen tanıları seç
        vc = df["Tanilar"].value_counts()
        vc = vc[vc >= min_count].head(topn)
        top_labels = list(vc.index)
        df = df[df["Tanilar"].isin(top_labels)]

        #pivot tabloyu hazırla
        value_col = "HastaNo" if "HastaNo" in df.columns else "Tanilar"
        pt = pd.pivot_table(df, index="Tanilar", columns="Cinsiyet", values=value_col, aggfunc="count", fill_value=0)

        #her tanıda yüzdeye çevir
        if normalize_within_diag:
            pt = pt.div(pt.sum(axis=1), axis=0) * 100.0

        #yığılmış bar grafiği çiz
        plt.figure(figsize=(10,6))
        bottom = None
        for i, col in enumerate(pt.columns):
            vals = pt[col].values
            plt.bar(pt.index, vals, bottom=bottom, label=str(col))
            bottom = vals if bottom is None else bottom + vals

        plt.title("Cinsiyet × Tanı (Top-{})".format(len(pt.index)))
        plt.xlabel("Tanı")
        plt.ylabel("%" if normalize_within_diag else "Sayı")
        plt.xticks(rotation=30, ha="right")
        plt.legend(title="Cinsiyet")
        self._save("gender_by_top_diagnoses.png")

    def diagnoses_pie(self, topn: int = 10, min_count: int = 10):
        #amaç: tanıların paylarını pie chart ile göstermek
        #kontrol: gerekli kolon var mı
        if "Tanilar" not in self.df.columns:
            return

        #boş olmayan tanıları al
        s = self.df["Tanilar"].dropna().astype(str).str.strip()
        s = s[s != ""]
        if s.empty:
            return

        #top-n tanıyı al ve kalanı diğer olarak topla
        vc = s.value_counts()
        top = vc[vc >= min_count].head(topn)
        others = vc.drop(top.index).sum()
        plot = top.copy()
        if others > 0:
            plot.loc["diğer"] = others

        #pie grafiği çiz
        plt.figure(figsize=(7,7))
        plot.sort_values(ascending=False).plot.pie(autopct="%1.1f%%", startangle=90)
        plt.ylabel("")
        plt.title("Tanı Dağılımı (Top-{} + diğer)".format(len(top)))
        self._save("diagnoses_pie.png")

    def hist_numeric_excluding_patient_id(self, bins: int = 30):
        num = self.df.select_dtypes(include=[np.number]).copy()
        if "HastaNo" in num.columns:
            num = num.drop(columns=["HastaNo"])
        for col in num.columns:
            s = num[col].dropna()
            if s.empty:
                continue
            plt.figure(figsize=(6,4))
            sns.histplot(s, bins=bins, kde=True, stat="density", alpha=0.6)
            plt.title(f"{col} | Histogram")
            plt.xlabel(col); plt.ylabel("Density")
            self._save(f"hist__{self._safe(col)}.png")

    def run_requested(self):
        self.age_group_vs_diagnosis_count()
        self.gender_by_top_diagnoses(topn=10, min_count=10, normalize_within_diag=True)
        self.diagnoses_pie(topn=10, min_count=10)