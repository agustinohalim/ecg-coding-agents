"""HRV against signal-free baselines that know the age cohort (JIKI panel 6, 23 Nov 2026; exploratory, post hoc).

Fantasia record names encode the cohort (f1o.. elderly, f1y.. young) and every task text gives the record name, so a
baseline that reads no waveform can still use it. Two leave-one-out baselines are scored on the six HRV quantities
other than heart rate, with the fixed 20 % tolerance, against each method task by task:
  cohort median   - median of the quantity over the other tasks of the same cohort;
  cohort + rate   - least squares on log mean RR with a cohort intercept (log-log; pNN50 linear, clipped at 0),
                    given the reference heart rate exactly, as the heart-rate model of agenekg_hrv_model_hr.py.

    python -X utf8 agenekg_hrv_umur.py <analysis dir> <runs dir>
"""
import math
import random
import statistics
import sys
from pathlib import Path

import numpy as np

from agenekg_hrv_model_hr import HRV_DIPREDIKSI, hrv_metode
from agenekg_hrv_toleransi_tetap import toleransi_tetap
from agenekg_qt_per_run import ci_tugas
from agenekg_tambahan_jiki import BENIH, MODEL, Paket, baris_run


def kohort(tid):
    return tid.split("_", 1)[1][2]


def median_kohort(ruj_hrv, tid, k):
    return statistics.median(ruj_hrv[t][k] for t in ruj_hrv if t != tid and kohort(t) == kohort(tid))


def kohort_dan_laju(ruj_hrv, tid, k):
    """Leave-one-out prediction of quantity k from log mean RR plus a cohort intercept."""
    fitur = lambda t: [1.0, math.log(60000.0 / ruj_hrv[t]["hr_bpm"]), 1.0 if kohort(t) == "o" else 0.0]
    lain = [t for t in ruj_hrv if t != tid and (k == "pnn50_pct" or ruj_hrv[t][k] > 0)]
    y = [ruj_hrv[t][k] if k == "pnn50_pct" else math.log(ruj_hrv[t][k]) for t in lain]
    koef = np.linalg.lstsq(np.array([fitur(t) for t in lain]), np.array(y), rcond=None)[0]
    tebak = float(np.dot(koef, fitur(tid)))
    return max(0.0, tebak) if k == "pnn50_pct" else math.exp(tebak)


def dasar_umur(rujukan, pkg):
    """Task -> share correct over HRV_DIPREDIKSI for the cohort median and the cohort + rate model."""
    ruj_hrv = {t: r["nilai"] for t, r in rujukan.ruj.items()
               if r["jenis"] == "hrv" and not r["nilai"].get("unanswerable")}
    tetap = toleransi_tetap(rujukan.ruj)
    hasil = {"cohort median": {}, "cohort + heart-rate model": {}}
    for tid, nilai in ruj_hrv.items():
        bts = {k: pkg.skor.batas(tetap[tid]["tol"][k], nilai[k], 0.0) for k in HRV_DIPREDIKSI}
        for nama, fungsi in (("cohort median", median_kohort), ("cohort + heart-rate model", kohort_dan_laju)):
            hasil[nama][tid] = statistics.fmean(abs(fungsi(ruj_hrv, tid, k) - nilai[k]) <= bts[k] for k in HRV_DIPREDIKSI)
    n = {c: sum(kohort(t) == c for t in ruj_hrv) for c in "oy"}
    print(f"- {len(ruj_hrv)} HRV tasks: {n['o']} elderly, {n['y']} young")
    return hasil


def cetak(data, dasar, pkg, rng):
    for nama, pembanding in dasar.items():
        print(f"- {nama}: {100 * statistics.fmean(pembanding.values()):.1f} % (heart rate excluded)")
    for m, rows in data.items():
        agen = hrv_metode(rows)
        for nama, pembanding in dasar.items():
            beda = {t: agen[t] - pembanding[t] for t in agen if t in pembanding}
            est, lo, hi = ci_tugas(beda, lambda d: statistics.fmean(d.values()), rng)
            _, p, n = pkg.statistik.uji_permutasi(agen, pembanding, rng)
            print(f"- {m} ({100 * statistics.fmean(agen.values()):.1f} %) minus {nama}: {100 * est:+.1f} points "
                  f"({100 * lo:+.1f} to {100 * hi:+.1f}), p = {p:.4f}, {n} tasks")


def main():
    analisis, runs = Path(sys.argv[1]), Path(sys.argv[2])
    pkg = Paket(analisis)
    from penilaian import skor, statistik
    pkg.skor, pkg.statistik = skor, statistik
    utama = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                             analisis / "agenekg_rujukan_hrv.json")
    print("## HRV against age-cohort signal-free baselines (fixed 20 % tolerance, heart rate excluded; 95 % interval)\n")
    cetak({m: baris_run(runs / m, utama, pkg) for m in MODEL}, dasar_umur(utama, pkg), pkg, random.Random(BENIH))


if __name__ == "__main__":
    main()
