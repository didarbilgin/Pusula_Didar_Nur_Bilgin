import os
from pathlib import Path
import pandas as pd

from src.data.load_data import LoadData
from src.preprocessing.normalization.pipeline import NormalizationPipeline
from impute.pipeline_impute import run_imputation
from src.eda.missing_analyzer import MissingAnalyzer
from src.visualization.data_viz import DataVisualization
from src.preprocessing.postprocess.convert_numeric import convert_numeric

REPORTS_DIR = Path("reports")
FIG_DIR = REPORTS_DIR / "figures"
OUT_PATH = Path("data/output.xlsx")

def ensure_dirs():
    #rapor ve çıktı klasörleri
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def print_and_save_missing(df: pd.DataFrame, name: str):
    #eksik özeti
    rep = MissingAnalyzer(df).summary()
    #konsola yazdırma
    print(f"\n== Missing {name} ==")
    print(rep.head(20))
    #csv olarak kaydetme
    rep.to_csv(REPORTS_DIR / f"missing_{name}.csv", index=True)

def main():
    #klasörleri hazırlama
    ensure_dirs()

    #veri yükleme
    df = LoadData(input_path="data/Talent_Academy_Case_DT_2025.xlsx").load()
    print(f"Data loaded successfully. Shape: {df.shape}")

    #ham veride eksik durumunu yaz/kaydet
    print_and_save_missing(df, "before")

    #normalizasyon (metin+çoklu değer+sayısal kurallar)
    text_cols = [
        "Cinsiyet","Uyruk","KanGrubu",
        "KronikHastalik","Alerji",
        "Tanilar","TedaviAdi","UygulamaYerleri","Bolum",
    ]
    multivalue_cols = ["UygulamaYerleri", "Alerji", "KronikHastalik"]
    numeric_rules = {
        "Yas": (0, 120),
        "uygulamasuresi_num": (1, 600),
    }
    df = NormalizationPipeline(text_cols, multivalue_cols, numeric_rules).run(df)
    print("Data normalization completed.")

    #impute pipeline uygulama
    df = run_imputation(df)
    print("Imputation pipeline has been successfully applied.")

    #metin olan süre kolonlarını sonda sayısala çevir
    df = convert_numeric(
        df,
        col_sessions="TedaviSuresi",
        col_minutes="UygulamaSuresi",
        out_sessions="TedaviSuresi_seans",
        out_minutes="UygulamaSuresi_dakika"
    )
    print("Duration columns converted and renamed (TedaviSuresi_seans, UygulamaSuresi_dk)")
    
    #eksik verileri doldurma sonrası eksik durumunu yaz/kaydet
    print_and_save_missing(df, "after")

    #görselleştirme 
    viz = DataVisualization(df, outdir=str(FIG_DIR))
    viz.run_requested()
    print("Visualizations have been created under reports/figures.")

    #çıktıyı kaydet
    df.to_excel(OUT_PATH, index=False)
    print(f"Output file has been created at: {OUT_PATH.resolve()}")

if __name__ == "__main__":
    main()