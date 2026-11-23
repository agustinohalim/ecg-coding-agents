"""Run-level QT agreement requested by JIKI panel 2 (22 Nov 2026), after all results; none is in the preregistration.

Every numeric non-zero answer of every run is one pair (answer, reference); intervals come from 10,000 bootstrap
resamples of tasks (all runs of a task move together). Baselines, one answer per task:
- constant: leave-one-out median of the other tasks' reference, as in Hasil 16;
- RR model: leave-one-out least-squares fit QT = a + b * RR over the other tasks' references, applied to the task's
  reference RR (RR = (QT / QTcB)^2), then QTcB = QT / sqrt(RR) and QTcF = QT / cbrt(RR). It knows the heart rate
  exactly and nothing about wave boundaries.
Reported per method and quantity: median absolute error, Bland-Altman bias and 95 % limits of agreement, Spearman
rho, Theil-Sen slope (interval against 0 and 1), and the share within 10, 20, and 40 ms; and, paired by task, the
mean over runs of |agent - ref| - |baseline - ref|, as a median over tasks with its interval.

    python -X utf8 agenekg_qt_per_run.py <analysis folder> <runs folder>
"""
import random
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy import stats

from agenekg_tambahan_jiki import BENIH, Paket, baris_run

QT = ("qt_ms", "qtcb_ms", "qtcf_ms")
ULANG = 10_000


def dasar(rujukan):
    """Per task and quantity: (constant answer, RR-model answer)."""
    ref = {t: r["nilai"] for t, r in rujukan.ruj.items() if r["jenis"] == "qt"}
    rr = {t: (v["qt_ms"] / v["qtcb_ms"]) ** 2 for t, v in ref.items()}
    hasil = {}
    for t, v in ref.items():
        lain = [u for u in ref if u != t]
        b, a = np.polyfit([rr[u] for u in lain], [ref[u]["qt_ms"] for u in lain], 1)
        qt = a + b * rr[t]
        model = {"qt_ms": qt, "qtcb_ms": qt / rr[t] ** 0.5, "qtcf_ms": qt / rr[t] ** (1 / 3)}
        hasil[t] = {q: (statistics.median(ref[u][q] for u in lain), model[q]) for q in QT}
    return ref, hasil


def ukuran(pasang):
    """Metrics over a list of (answer, reference) pairs."""
    a, r = np.array([p[0] for p in pasang]), np.array([p[1] for p in pasang])
    d = a - r
    rho = stats.spearmanr(a, r)[0] if np.ptp(a) > 0 else np.nan
    return {"mae": float(np.median(abs(d))), "bias": float(d.mean()), "loa_lo": float(d.mean() - 1.96 * d.std(ddof=1)),
            "loa_hi": float(d.mean() + 1.96 * d.std(ddof=1)), "rho": float(rho),
            "slope": float(stats.theilslopes(a, r)[0]) if np.ptp(a) > 0 else np.nan,
            **{f"in{t}": float(np.mean(abs(d) <= t)) for t in (10, 20, 40)}}


def ci_tugas(per_tugas, fungsi, rng, alfa=0.05):
    """Point estimate and (1 - alfa) interval of fungsi(dict of task -> list) over tasks resampled with replacement."""
    kunci = list(per_tugas)
    ulang = []
    for _ in range(ULANG):
        pilih = rng.choices(kunci, k=len(kunci))
        ulang.append(fungsi({i: per_tugas[k] for i, k in enumerate(pilih)}))
    ulang = np.array(ulang, dtype=float)
    return fungsi(per_tugas), np.nanpercentile(ulang, 50 * alfa, axis=0), np.nanpercentile(ulang, 100 - 50 * alfa, axis=0)


def pasangan(rows, ref):
    """Per quantity: task -> list of (answer, reference) over runs with a non-zero numeric answer."""
    hasil = {q: {} for q in QT}
    for _, b, _ in rows:
        for x in b["besaran"]:
            if x["besaran"] in QT and isinstance(x["agen"], (int, float)) and x["agen"] != 0:
                hasil[x["besaran"]].setdefault(b["tugas"], []).append((float(x["agen"]), ref[b["tugas"]][x["besaran"]]))
    return hasil


def cetak_metode(nama, per_q, rng):
    for q, per_tugas in per_q.items():
        if len(per_tugas) < 20:
            print(f"| {nama} | {q} | {len(per_tugas)} tasks | — |")
            continue
        kunci = ("mae", "bias", "loa_lo", "loa_hi", "rho", "slope", "in10", "in20", "in40")
        f = lambda d: [ukuran([p for v in d.values() for p in v])[k] for k in kunci]
        est, lo, hi = ci_tugas(per_tugas, f, rng)
        sel = [f"{e:.2f} ({l:.2f} to {h:.2f})" for e, l, h in zip(est, lo, hi)]
        n = sum(len(v) for v in per_tugas.values())
        print(f"| {nama} | {q} | {n} pairs, {len(per_tugas)} tasks | " + " | ".join(sel) + " |")


def berpasangan(per_q, banding, idx, rng):
    """Per quantity: median over tasks of mean(|agent - ref|) - |baseline - ref|, interval, tasks closer."""
    for q, per_tugas in per_q.items():
        beda = {t: statistics.fmean(abs(a - r) for a, r in v) - abs(banding[t][q][idx] - v[0][1]) for t, v in per_tugas.items()}
        est, lo, hi = ci_tugas(beda, lambda d: statistics.median(d.values()), rng)
        print(f"- {q}: {est:+.1f} ms ({lo:+.1f} to {hi:+.1f}); agent closer on {sum(x < 0 for x in beda.values())}/{len(beda)} tasks")


def main():
    analisis, runs = Path(sys.argv[1]), Path(sys.argv[2])
    pkg = Paket(analisis)
    from penilaian import skor
    pkg.skor = skor
    rujukan = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                               analisis / "agenekg_rujukan_hrv.json")
    ref, banding = dasar(rujukan)
    rng = random.Random(BENIH)
    print("| Method | Quantity | n | Median abs error | Bias | LoA low | LoA high | Spearman rho | Theil-Sen slope "
          "| Within 10 ms | Within 20 ms | Within 40 ms |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    agen = pasangan(baris_run(runs / "main_deepseek-v4-flash", rujukan, pkg), ref)
    cetak_metode("DeepSeek-V4-flash (runs)", agen, rng)
    cetak_metode("NeuroKit2 DWT", pasangan(baris_run(runs / "baseline_nk_dwt", rujukan, pkg), ref), rng)
    for nama, idx in (("constant (leave-one-out)", 0), ("RR model (leave-one-out)", 1)):
        cetak_metode(nama, {q: {t: [(banding[t][q][idx], ref[t][q])] for t in ref} for q in QT}, rng)
    for nama, idx in (("constant", 0), ("RR model", 1)):
        print(f"\nPaired by task, DeepSeek runs minus {nama} (ms; negative = agent closer):\n")
        berpasangan(agen, banding, idx, rng)


if __name__ == "__main__":
    main()
