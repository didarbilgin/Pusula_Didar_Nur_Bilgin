import re
import pandas as pd
import numpy as np

#metni dakika cinsine çevirir (mesela "1:30"→90, "2 saat"→120, "45 dk"→45)
def _to_minutes(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().casefold()

    #saat:dakika veya saat:dakika:saniye formatları
    if ":" in s:
        parts = s.split(":")
        try:
            if len(parts) == 2:
                h, m = int(parts[0]), int(parts[1])
                return h*60 + m
            elif len(parts) == 3:
                h, m, _ = int(parts[0]), int(parts[1]), int(parts[2])
                return h*60 + m
        except Exception:
            return np.nan

    #"saat/hour/hr/h" içerirse sayıyı dakika yap
    if any(k in s for k in ["saat","hour","hr","h "]) or s.endswith("h"):
        m = re.search(r"(\d+)", s)
        return int(m.group(1))*60 if m else np.nan

    #"dk/dakika/min/m" içerirse sayıyı dakika kabul et
    if any(k in s for k in ["dk","dakika","min","m "]) or s.endswith("m"):
        m = re.search(r"(\d+)", s)
        return int(m.group(1)) if m else np.nan

    #sadece sayı varsa olduğu gibi dakika kabul et
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else np.nan

#metinden seans sayısını yakalar (örn: "10 seans"→10)
def _to_sessions(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip().casefold()
    m = re.search(r"(\d+)", s)
    return int(m.group(1)) if m else np.nan

#TedaviSuresi ve UygulamaSuresi kolonlarını sayısala çevirir ve yeni isimlerle ekler
def convert_numeric(df: pd.DataFrame,
                    col_sessions="TedaviSuresi",
                    col_minutes="UygulamaSuresi",
                    out_sessions="TedaviSuresi_seans",
                    out_minutes="UygulamaSuresi_dk",
                    sessions_bounds=(1,200),
                    minutes_bounds=(1,600)) -> pd.DataFrame:
    #orijinali bozmamak için kopya al
    out = df.copy()

    #tedavi süresi→seans(Int64)
    if col_sessions in out.columns:
        ses = out[col_sessions].apply(_to_sessions)
        ses = ses.mask((ses < sessions_bounds[0]) | (ses > sessions_bounds[1]))
        out[out_sessions] = ses.astype("Int64")

    #uygulama süresi→dakika(Int64)
    if col_minutes in out.columns:
        mins = out[col_minutes].apply(_to_minutes)
        mins = mins.mask((mins < minutes_bounds[0]) | (mins > minutes_bounds[1]))
        out[out_minutes] = mins.astype("Int64")

    return out