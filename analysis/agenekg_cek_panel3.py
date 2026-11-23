"""Exploratory checks requested by JIKI panel 3 (23 Nov 2026), after the confirmatory test; none is preregistered.

1. Within 20 ms, paired by task: share of a task's runs (no numeric answer = miss) minus the baseline's 0/1 hit,
   mean over tasks with a 95 % task-bootstrap interval, for the 45 main tasks (leave-one-out baselines) and the
   31 confirmatory tasks (baselines fitted on the 45 main tasks).
2. Runs without a numeric answer in the paired absolute-error statistic of H1/H2: dropped (as reported), scored
   as a tie with the baseline, or scored with the agent's largest error on that quantity.
3. Limits of agreement for replicated runs (Bland and Altman 2007, true value constant within a task, unequal
   replicates), and proportional bias as the least-squares slope of (agent - reference) on the reference.
4. HRV against a heart-rate model (agenekg_hrv_model_hr.py).

    python -X utf8 agenekg_cek_panel3.py <analysis folder> <runs folder> <confirmatory runs folder>
"""
import math
import random
import statistics
import sys
from pathlib import Path

import numpy as np

from agenekg_hrv_model_hr import cetak_hrv, hrv_dasar
from agenekg_konfirmasi_nilai import baris, dasar_tetap
from agenekg_qt_per_run import QT, ci_tugas, dasar
from agenekg_tambahan_jiki import BENIH, MODEL, Paket, baris_run

SINI = Path(__file__).resolve().parent
TOL_QT = 20.0


def jawaban_per_tugas(rows, ref, q):
    """Task -> list over runs of the numeric non-zero answer, or None for a run without one."""
    hasil = {t: [] for t in ref}
    for _, b, _ in rows:
        if b["tugas"] not in hasil:
            continue
        x = next((x for x in b["besaran"] if x["besaran"] == q), None)
        ok = x is not None and isinstance(x["agen"], (int, float)) and x["agen"] != 0
        hasil[b["tugas"]].append(float(x["agen"]) if ok else None)
    return hasil


def tepat_berpasangan(jawab, ref, banding, rng):
    """Per quantity and baseline: mean over tasks of (agent share within 20 ms) - (baseline within 20 ms)."""
    for q in QT:
        for idx, nama in ((0, "constant"), (1, "RR model")):
            kena = {t: abs(banding[t][q][idx] - ref[t][q]) <= TOL_QT for t in jawab[q]}
            agen = {t: statistics.fmean(a is not None and abs(a - ref[t][q]) <= TOL_QT for a in run)
                    for t, run in jawab[q].items()}
            beda = {t: agen[t] - kena[t] for t in agen}
            est, lo, hi = ci_tugas(beda, lambda d: statistics.fmean(d.values()), rng)
            print(f"- {q}, agent minus {nama}: {100 * est:+.1f} points ({100 * lo:+.1f} to {100 * hi:+.1f}); "
                  f"agent {100 * statistics.fmean(agen.values()):.1f} %, {nama} {100 * statistics.fmean(kena.values()):.1f} %, "
                  f"{sum(v > 0 for v in beda.values())} tasks agent ahead, {sum(v < 0 for v in beda.values())} behind")


def galat_terisi(run, r, isian):
    """Absolute errors of a task's runs, a run without an answer replaced by isian (None drops it)."""
    galat = [abs(a - r) if a is not None else isian for a in run]
    return [g for g in galat if g is not None]


def kepekaan_kosong(jawab, ref, banding, rng_alfa):
    """H1/H2 statistic under three treatments of runs without an answer."""
    rng, alfa = rng_alfa
    for q in QT:
        terburuk = max(abs(a - ref[t][q]) for t, run in jawab[q].items() for a in run if a is not None)
        kosong = sum(a is None for run in jawab[q].values() for a in run)
        for idx, nama in ((0, "constant"), (1, "RR model")):
            for label in ("dropped", "tie", "largest error"):
                beda = {}
                for t, run in jawab[q].items():
                    dasar_galat = abs(banding[t][q][idx] - ref[t][q])
                    isian = {"dropped": None, "tie": dasar_galat, "largest error": terburuk}[label]
                    galat = galat_terisi(run, ref[t][q], isian)
                    if galat:
                        beda[t] = statistics.fmean(galat) - dasar_galat
                est, lo, hi = ci_tugas(beda, lambda d: statistics.median(d.values()), rng, alfa)
                print(f"- {q}, minus {nama}, no-answer runs {label} ({kosong} runs): "
                      f"{est:+.1f} ms ({lo:+.1f} to {hi:+.1f}), {len(beda)} tasks")


def loa_ulangan(per_tugas):
    """[bias, lower, upper, slope of difference on reference] for task -> list of (answer, reference)."""
    d = {t: [a - r for a, r in v] for t, v in per_tugas.items() if v}
    semua = [x for v in d.values() for x in v]
    n_obs, n_tugas = len(semua), len(d)
    ss_w = sum((x - statistics.fmean(v)) ** 2 for v in d.values() for x in v)
    var_w = ss_w / (n_obs - n_tugas) if n_obs > n_tugas else 0.0
    var_rata = statistics.variance([statistics.fmean(v) for v in d.values()])
    sd = math.sqrt(var_rata + var_w * (1 - statistics.fmean(1 / len(v) for v in d.values())))
    bias = statistics.fmean(semua)
    slope = float(np.polyfit([r for v in per_tugas.values() for _, r in v], semua, 1)[0])
    return [bias, bias - 1.96 * sd, bias + 1.96 * sd, slope]


def cetak_loa(jawab, ref, rng):
    for q in QT:
        per = {t: [(a, ref[t][q]) for a in run if a is not None] for t, run in jawab[q].items()}
        per = {t: v for t, v in per.items() if v}
        est, lo, hi = ci_tugas(per, loa_ulangan, rng)
        sel = " | ".join(f"{e:.1f} ({l:.1f} to {h:.1f})" for e, l, h in zip(est, lo, hi))
        print(f"| DeepSeek-V4-flash | {q} | {sum(map(len, per.values()))} answers, {len(per)} tasks | {sel} |")


def bagian_qt(judul, jawab, ref_banding, rng_alfa):
    ref, banding = ref_banding
    rng, alfa = rng_alfa
    print(f"\n## {judul}\n\n### 1. Within 20 ms, paired by task (95 % interval)\n")
    tepat_berpasangan(jawab, ref, banding, rng)
    print(f"\n### 2. Runs without an answer, paired absolute error ({100 * (1 - alfa):.2f} % interval)\n")
    kepekaan_kosong(jawab, ref, banding, (rng, alfa))
    print("\n### 3. Limits of agreement for replicated runs (95 % interval)\n\n"
          "| Method | Quantity | n | Bias | LoA low | LoA high | Slope of difference on reference |\n|---|---|---|---|---|---|---|")
    cetak_loa(jawab, ref, rng)


def main():
    analisis, runs, konf_runs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pkg = Paket(analisis)
    from penilaian import skor, statistik
    pkg.skor, pkg.statistik = skor, statistik
    hrv = analisis / "agenekg_rujukan_hrv.json"
    utama = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json", hrv)
    rng = random.Random(BENIH)
    ref, banding = dasar(utama)
    rows = baris_run(runs / "main_deepseek-v4-flash", utama, pkg)
    bagian_qt("Main tasks (45, leave-one-out baselines)", {q: jawaban_per_tugas(rows, ref, q) for q in QT},
              (ref, banding), (rng, 0.05))
    konf = skor.muat_rujukan(SINI / "agenekg_rujukan_konfirmasi.json", SINI / "agenekg_tugas_konfirmasi.json", hrv)
    ref_k = {t: r["nilai"] for t, r in konf.ruj.items()}
    rows_k = baris(konf_runs, konf, skor)
    bagian_qt("Confirmatory tasks (31, baselines fitted on the main tasks)",
              {q: jawaban_per_tugas(rows_k, ref_k, q) for q in QT}, (ref_k, dasar_tetap(utama, ref_k)[0]), (rng, 0.05 / 3))
    print("\n## 4. HRV against a heart-rate model (fixed 20 % tolerance, heart rate excluded; 95 % interval)\n")
    cetak_hrv({m: baris_run(runs / m, utama, pkg) for m in MODEL}, hrv_dasar(utama, pkg), pkg, rng)


if __name__ == "__main__":
    main()
