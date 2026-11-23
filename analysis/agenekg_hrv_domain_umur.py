"""HRV signal-free baselines and the pipeline split by domain (JIKI panel 7, 23 Nov 2026; exploratory, post hoc).

Time domain: SDNN, RMSSD, pNN50; frequency domain: LF, HF, LF/HF; fixed 20 % tolerance, heart rate excluded.
Reports each baseline and method per domain, the commercial agent minus each signal-free baseline, and the agent
minus the NeuroKit2 DWT pipeline per domain (95 % task-bootstrap interval, paired permutation test).

    python -X utf8 agenekg_hrv_domain_umur.py <analysis dir> <runs dir>
"""
import random
import statistics
import sys
from pathlib import Path

from agenekg_hrv_model_hr import prediksi_hr
from agenekg_hrv_toleransi_tetap import toleransi_tetap
from agenekg_hrv_umur import kohort_dan_laju, median_kohort
from agenekg_qt_per_run import ci_tugas
from agenekg_tambahan_jiki import BENIH, Paket, baris_run

DOMAIN = {"time": ("sdnn_ms", "rmssd_ms", "pnn50_pct"), "frequency": ("lf_ms2", "hf_ms2", "lf_hf")}
AGEN, PIPELINE = "main_deepseek-v4-flash", "baseline_nk_dwt"


def median_lain(ruj_hrv, tid, k):
    return statistics.median(ruj_hrv[t][k] for t in ruj_hrv if t != tid)


PEMBANDING = {"constant": median_lain, "heart-rate model": prediksi_hr,
              "age-group median": median_kohort, "age-group + heart-rate model": kohort_dan_laju}


def dasar_domain(rujukan, pkg, besaran):
    """Baseline -> task -> share correct over the given quantities."""
    ruj_hrv = {t: r["nilai"] for t, r in rujukan.ruj.items()
               if r["jenis"] == "hrv" and not r["nilai"].get("unanswerable")}
    tetap = toleransi_tetap(rujukan.ruj)
    hasil = {nama: {} for nama in PEMBANDING}
    for tid, nilai in ruj_hrv.items():
        bts = {k: pkg.skor.batas(tetap[tid]["tol"][k], nilai[k], 0.0) for k in besaran}
        for nama, fungsi in PEMBANDING.items():
            hasil[nama][tid] = statistics.fmean(abs(fungsi(ruj_hrv, tid, k) - nilai[k]) <= bts[k] for k in besaran)
    return hasil


def metode_domain(rows, besaran):
    per = {}
    for _, _, bt in rows:
        if bt["jenis"] == "hrv":
            per.setdefault(bt["tugas"], []).extend(x["benar"] for x in bt["besaran"] if x["besaran"] in besaran)
    return {t: statistics.fmean(v) for t, v in per.items() if v}


def cetak_beda(agen, nama_pembanding, pembanding, konteks):
    pkg, rng = konteks
    beda = {t: agen[t] - pembanding[t] for t in agen if t in pembanding}
    est, lo, hi = ci_tugas(beda, lambda d: statistics.fmean(d.values()), rng)
    _, p, n = pkg.statistik.uji_permutasi(agen, pembanding, rng)
    print(f"  - agent minus {nama_pembanding}: {100 * est:+.1f} points ({100 * lo:+.1f} to {100 * hi:+.1f}), "
          f"p = {p:.4f}, {n} tasks")


def main():
    analisis, runs = Path(sys.argv[1]), Path(sys.argv[2])
    pkg = Paket(analisis)
    from penilaian import skor, statistik
    pkg.skor, pkg.statistik = skor, statistik
    utama = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                             analisis / "agenekg_rujukan_hrv.json")
    rows = {m: baris_run(runs / m, utama, pkg) for m in (AGEN, PIPELINE)}
    konteks = (pkg, random.Random(BENIH))
    print("## HRV by domain (fixed 20 % tolerance; 95 % task-bootstrap interval)\n")
    for domain, besaran in DOMAIN.items():
        dasar = dasar_domain(utama, pkg, besaran)
        agen, pipa = metode_domain(rows[AGEN], besaran), metode_domain(rows[PIPELINE], besaran)
        print(f"- {domain}: agent {100 * statistics.fmean(agen.values()):.1f} %, pipeline "
              f"{100 * statistics.fmean(pipa.values()):.1f} %, " +
              ", ".join(f"{n} {100 * statistics.fmean(d.values()):.1f} %" for n, d in dasar.items()))
        for nama, pembanding in {**dasar, "pipeline": pipa}.items():
            cetak_beda(agen, nama, pembanding, konteks)


if __name__ == "__main__":
    main()
