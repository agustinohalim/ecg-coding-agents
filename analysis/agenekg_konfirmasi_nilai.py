"""Confirmatory QT analysis for AgenEKG, fixed in Prareg_AgenEKG_Konfirmasi.md (22 Nov 2026) before any new run.

Baselines are fitted on the 45 main QT tasks only and applied unchanged to the 31 confirmatory tasks:
- constant: median reference value of the 45 main tasks, per quantity;
- RR model: least-squares QT = a + b * RR over the 45 main tasks, applied to the confirmatory task's reference RR,
  then QTcB = QT / sqrt(RR), QTcF = QT / cbrt(RR).
Primary (QT only; 98.33 % task-bootstrap intervals, Bonferroni over three):
  H1 paired difference agent minus constant < 0;  H2 paired difference agent minus RR model < 0;
  H3 run-level Spearman rho > 0.
Paired difference per task = mean over runs of |agent - ref| - |baseline - ref|; summary = median over tasks.
Runs without a non-zero numeric answer leave the agreement measures and are counted; in hit rates they are wrong.

    python -X utf8 agenekg_konfirmasi_nilai.py <analysis folder> <confirmatory runs folder> [<NeuroKit2 runs folder>]
"""
import json
import random
import statistics
import sys
from pathlib import Path

import numpy as np

from agenekg_qt_per_run import QT, ci_tugas, pasangan, ukuran
from agenekg_tambahan_jiki import BENIH, Paket

SINI = Path(__file__).resolve().parent
ALFA = 0.05 / 3


def dasar_tetap(utama, konf):
    """Per confirmatory task and quantity: (constant, RR-model answer), both fitted on the 45 main tasks."""
    ref = [r["nilai"] for r in utama.ruj.values() if r["jenis"] == "qt"]
    rr = [(v["qt_ms"] / v["qtcb_ms"]) ** 2 for v in ref]
    b, a = np.polyfit(rr, [v["qt_ms"] for v in ref], 1)
    median = {q: statistics.median(v[q] for v in ref) for q in QT}
    hasil = {}
    for t, v in konf.items():
        x = (v["qt_ms"] / v["qtcb_ms"]) ** 2
        qt = a + b * x
        model = {"qt_ms": qt, "qtcb_ms": qt / x ** 0.5, "qtcf_ms": qt / x ** (1 / 3)}
        hasil[t] = {q: (median[q], model[q]) for q in QT}
    return hasil, (a, b), median


def baris(dir_run, rujukan, skor):
    """Scored rows of every run file in a folder."""
    return [(None, skor.baris_tugas_ulangan(json.loads(f.read_text(encoding="utf-8")), rujukan), None)
            for f in sorted(Path(dir_run).rglob("*_u*.json"))]


def ringkas(nama, per_q, banding, rng):
    """Agreement table rows and paired differences against both baselines, for one method."""
    kunci = ("mae", "bias", "loa_lo", "loa_hi", "rho", "slope", "in10", "in20", "in40")
    for q, per_tugas in per_q.items():
        f = lambda d: [ukuran([p for v in d.values() for p in v])[k] for k in kunci]
        est, lo, hi = ci_tugas(per_tugas, f, rng, ALFA)
        sel = " | ".join(f"{e:.2f} ({l:.2f} to {h:.2f})" for e, l, h in zip(est, lo, hi))
        print(f"| {nama} | {q} | {sum(map(len, per_tugas.values()))} pairs, {len(per_tugas)} tasks | {sel} |")
    for idx, dasar_nama in ((0, "constant"), (1, "RR model")):
        for q, per_tugas in per_q.items():
            beda = {t: statistics.fmean(abs(a - r) for a, r in v) - abs(banding[t][q][idx] - v[0][1])
                    for t, v in per_tugas.items()}
            est, lo, hi = ci_tugas(beda, lambda d: statistics.median(d.values()), rng, ALFA)
            dekat = sum(x < 0 for x in beda.values())
            print(f"- {nama} minus {dasar_nama}, {q}: {est:+.1f} ms ({lo:+.1f} to {hi:+.1f}); closer on {dekat}/{len(beda)}")


def main():
    analisis, runs = Path(sys.argv[1]), Path(sys.argv[2])
    pkg = Paket(analisis)
    from penilaian import skor
    pkg.skor = skor
    hrv = analisis / "agenekg_rujukan_hrv.json"
    utama = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json", hrv)
    konf = skor.muat_rujukan(SINI / "agenekg_rujukan_konfirmasi.json", SINI / "agenekg_tugas_konfirmasi.json", hrv)
    ref = {t: r["nilai"] for t, r in konf.ruj.items()}
    banding, (a, b), median = dasar_tetap(utama, ref)
    print(f"RR model QT = {a:.1f} + {b:.1f} * RR; constant {', '.join(f'{q} {v:.1f}' for q, v in median.items())}")
    rng = random.Random(BENIH)
    rows = baris(runs, konf, skor)
    jawab = sum(any(x["besaran"] in QT and isinstance(x["agen"], (int, float)) and x["agen"] != 0
                    for x in r["besaran"]) for _, r, _ in rows)
    print(f"runs {len(rows)}, with a numeric answer {jawab}, all correct {sum(r['semua_benar'] for _, r, _ in rows)}")
    print("| Method | Quantity | n | Median abs error | Bias | LoA low | LoA high | Spearman rho | Theil-Sen slope "
          "| Within 10 ms | Within 20 ms | Within 40 ms |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    ringkas("DeepSeek-V4-flash", pasangan(rows, ref), banding, rng)
    for nama, idx in (("constant", 0), ("RR model", 1)):
        d = {q: {t: [(banding[t][q][idx], ref[t][q])] for t in ref} for q in QT}
        print(f"{nama}: " + ", ".join(f"{q} within 10/20/40 ms "
              + "/".join(f"{ukuran([p for v in d[q].values() for p in v])[f'in{k}']:.3f}" for k in (10, 20, 40))
              for q in QT))
    if len(sys.argv) > 3:
        ringkas("NeuroKit2 DWT", pasangan(baris(sys.argv[3], konf, skor), ref), banding, rng)


if __name__ == "__main__":
    main()
