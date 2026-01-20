import re
import html
import unicodedata
import numpy as np
import pandas as pd


def normalize_subject(subject: str) -> str:
    if not isinstance(subject, str):
        return ""

    subject = re.sub(r"\{\{.*?\}\}|\{%.*?%\}", " ", subject)
    subject = html.unescape(subject)
    subject = unicodedata.normalize("NFKC", subject)
    subject = subject.lower()
    subject = re.sub(r"\d+", " ", subject)
    subject = re.sub(r"[^\w\s]", " ", subject)
    subject = re.sub(r"_+", " ", subject)
    subject = re.sub(r"\s+", " ", subject).strip()

    return subject


def wilson_lower_bound(opens: int, sendings: int, z: float = 1.96) -> float:
    if sendings <= 0:
        return 0.0

    p = opens / sendings
    z2 = z * z
    denom = 1 + z2 / sendings
    center = p + z2 / (2 * sendings)
    margin = z * np.sqrt((p * (1 - p) + z2 / (4 * sendings)) / sendings)

    return (center - margin) / denom


def rank_subjects(
    df: pd.DataFrame,
    min_sendings: int = 50
) -> pd.DataFrame:
    required = {"subject", "sendings", "opens"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df = df[df["sendings"] >= min_sendings]

    df["subject_norm"] = df["subject"].apply(normalize_subject)

    df_sorted = df.sort_values(["subject_norm", "sendings"], ascending=[True, False])

    df_agg = (
        df_sorted
        .groupby("subject_norm", as_index=False)
        .agg(
            subject=("subject", "first"),
            total_sendings=("sendings", "sum"),
            total_opens=("opens", "sum"),
        )
    )

    df_agg["open_rate"] = df_agg["total_opens"] / df_agg["total_sendings"]

    df_agg["wilson_score"] = df_agg.apply(
        lambda r: wilson_lower_bound(r["total_opens"], r["total_sendings"]),
        axis=1
    )

    return df_agg.sort_values("wilson_score", ascending=False)
import re
import html
import unicodedata
import numpy as np
import pandas as pd


def normalize_subject(subject: str) -> str:
    if not isinstance(subject, str):
        return ""

    subject = re.sub(r"\{\{.*?\}\}|\{%.*?%\}", " ", subject)
    subject = html.unescape(subject)
    subject = unicodedata.normalize("NFKC", subject)
    subject = subject.lower()
    subject = re.sub(r"\d+", " ", subject)
    subject = re.sub(r"[^\w\s]", " ", subject)
    subject = re.sub(r"_+", " ", subject)
    subject = re.sub(r"\s+", " ", subject).strip()

    return subject


def wilson_lower_bound(opens: int, sendings: int, z: float = 1.96) -> float:
    if sendings <= 0:
        return 0.0

    p = opens / sendings
    z2 = z * z
    denom = 1 + z2 / sendings
    center = p + z2 / (2 * sendings)
    margin = z * np.sqrt((p * (1 - p) + z2 / (4 * sendings)) / sendings)

    return (center - margin) / denom


def rank_subjects(
    df: pd.DataFrame,
    min_sendings: int = 50
) -> pd.DataFrame:
    required = {"subject", "sendings", "opens"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df = df[df["sendings"] >= min_sendings]

    df["subject_norm"] = df["subject"].apply(normalize_subject)

    df_sorted = df.sort_values(["subject_norm", "sendings"], ascending=[True, False])

    df_agg = (
        df_sorted
        .groupby("subject_norm", as_index=False)
        .agg(
            subject=("subject", "first"),
            total_sendings=("sendings", "sum"),
            total_opens=("opens", "sum"),
        )
    )

    df_agg["open_rate"] = df_agg["total_opens"] / df_agg["total_sendings"]

    df_agg["wilson_score"] = df_agg.apply(
        lambda r: wilson_lower_bound(r["total_opens"], r["total_sendings"]),
        axis=1
    )

    return df_agg.sort_values("wilson_score", ascending=False)
