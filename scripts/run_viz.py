import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import pandas as pd
from typing import Optional
from src.visualization.data_viz import DataVisualization

def main(input_path: str, sheet: Optional[str] = None):
    #dosya uzantısına göre excel ya da csv oku
    if input_path.lower().endswith(".xlsx"):
        df = pd.read_excel(input_path, sheet_name=0 if sheet is None else sheet)
    else:
        df = pd.read_csv(input_path)

    #yüklenen verinin boyutunu yazdır
    print(f"data loaded: {df.shape[0]} rows, {df.shape[1]} cols")

    #visualization sınıfını çalıştır
    viz = DataVisualization(df, outdir="reports/figures")
    viz.run_requested()
    print("done. see reports/figures folder.")

if __name__ == "__main__":
    #argümanları tanımla
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--sheet", default=None)
    args = ap.parse_args()
    main(args.input, args.sheet)