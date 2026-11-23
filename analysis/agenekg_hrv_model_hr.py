"""HRV against a heart-rate model, for agenekg_cek_panel3.py (JIKI panel 3, 23 Nov 2026; exploratory).

Every HRV quantity except heart rate is predicted from the reference mean RR by a leave-one-out least-squares fit
(log-log; pNN50 linear, clipped at 0), scored with the fixed 20 % tolerance, and compared task by task with each
method on the same quantities; heart rate is excluded on both sides, since the model is given it exactly.
"""
import math
import statistics

import numpy as np

from agenekg_hrv_toleransi_tetap import toleransi_tetap
from agenekg_qt_per_run import ci_tugas

HRV_DIPREDIKSI = ("sdnn_ms", "rmssd_ms", "pnn50_pct", "lf_ms2", "hf_ms2", "lf_hf")


def prediksi_hr(ruj_hrv, tid, k):
    """Leave-one-out prediction of quantity k for task tid from the reference mean RR."""
    rr = lambda t: 60000.0 / ruj_hrv[t]["hr_bpm"]
    lain = [t for t in ruj_hrv if t != tid]
    if k == "pnn50_pct":
        b, a = np.polyfit([rr(t) for t in lain], [ruj_hrv[t][k] for t in lain], 1)
        return max(0.0, a + b * rr(tid))
    pakai = [t for t in lain if ruj_hrv[t][k] > 0]
    b, a = np.polyfit([math.log(rr(t)) for t in pakai], [math.log(ruj_hrv[t][k]) for t in pakai], 1)
    return math.exp(a + b * math.log(rr(tid)))


def hrv_dasar(rujukan, pkg):
    """Task -> share correct over HRV_DIPREDIKSI for the heart-rate model and the constant, fixed 20 % tolerance."""
    ruj_hrv = {t: r["nilai"] for t, r in rujukan.ruj.items()
               if r["jenis"] == "hrv" and not r["nilai"].get("unanswerable")}
    tetap = toleransi_tetap(rujukan.ruj)
    model, konst = {}, {}
    for tid, nilai in ruj_hrv.items():
        benar_m, benar_k = [], []
        for k in HRV_DIPREDIKSI:
            bts = pkg.skor.batas(tetap[tid]["tol"][k], nilai[k], 0.0)
            median = statistics.median(ruj_hrv[t][k] for t in ruj_hrv if t != tid)
            benar_m.append(abs(prediksi_hr(ruj_hrv, tid, k) - nilai[k]) <= bts)
            benar_k.append(abs(median - nilai[k]) <= bts)
        model[tid], konst[tid] = statistics.fmean(benar_m), statistics.fmean(benar_k)
    return model, konst


def hrv_metode(rows):
    """Task -> share correct over HRV_DIPREDIKSI across a method's runs, fixed 20 % tolerance rows."""
    per = {}
    for _, _, bt in rows:
        if bt["jenis"] == "hrv":
            per.setdefault(bt["tugas"], []).extend(x["benar"] for x in bt["besaran"] if x["besaran"] in HRV_DIPREDIKSI)
    return {t: statistics.fmean(v) for t, v in per.items() if v}


def cetak_hrv(data, dasar_hrv, pkg, rng):
    model, konst = dasar_hrv
    print(f"- heart-rate model {100 * statistics.fmean(model.values()):.1f} %, "
          f"constant {100 * statistics.fmean(konst.values()):.1f} % ({len(model)} tasks, heart rate excluded)")
    for m, rows in data.items():
        agen = hrv_metode(rows)
        for nama, pembanding in (("heart-rate model", model), ("constant", konst)):
            beda = {t: agen[t] - pembanding[t] for t in agen if t in pembanding}
            est, lo, hi = ci_tugas(beda, lambda d: statistics.fmean(d.values()), rng)
            _, p, n = pkg.statistik.uji_permutasi(agen, pembanding, rng)
            print(f"- {m} ({100 * statistics.fmean(agen.values()):.1f} %) minus {nama}: {100 * est:+.1f} points "
                  f"({100 * lo:+.1f} to {100 * hi:+.1f}), p = {p:.4f}, {n} tasks")
