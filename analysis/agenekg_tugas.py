"""Generates the full AgenEKG task list (preregistration, sections 2 and 5; deviation of 7 November 2026).

Output (script folder): `agenekg_tugas.json` (text + files, for the agent) and `agenekg_rujukan.json` (values +
tolerances, never copied into the sandbox). Derived records (resampled or with channels swapped) are written to
`<data>/agenekg_turunan/` under neutral names `trNN` so that file names do not reveal the trap.

Task types (seed 20261107 for every random draw):
- QT (45): QT Database, excluding the 5 pilot records. Per record: the longest run of consecutive `.q1c` beats
  (no other beat in between according to `.atr`, or `.pu0` when there is no `.atr`; RR < 2 s), at least
  10 beats long. Multi-lead QT: earliest QRS onset to latest T end over both channels.
- HRV (34): Fantasia, one task per record with a window that passes the rule (`agenekg_rujukan_hrv.json`).
- Traps (20): MIT-BIH ectopic (NN vs RR, 6; the first 5-minute window per record with underlying sinus
  rhythm `(N`, bigeminy `(B` or trigeminy `(T`, no artefact marks `| ! x [ ]`, beats only N/V/A/F, 10-80
  ectopic beats, SDNN of all RR >= 1.3 x SDNN of NN), other sampling rate (5), channel order swapped (4),
  unanswerable (5: missing lead 3, window beyond the record 2).

Usage (from the repository root): python -I -X utf8 analysis/agenekg_tugas.py
"""
import json
import os
import random
import sys
from collections import Counter

import numpy as np
import wfdb
from scipy.signal import resample_poly

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agenekg_rujukan_qt as R  # noqa: E402

DATA = "C:/Data/PhysioNet"
QT_REL = "qtdb/data/qt-database-1.0.0"
FAN_REL = "fantasia/data/fantasia-database-1.0.0"
MIT_REL = "mitdb/data/mit-bih-arrhythmia-database-1.0.0"
TUR_REL = "agenekg_turunan"
SINI = os.path.dirname(os.path.abspath(__file__))
BENIH = 20261107
PILOT = {"sele0111", "sele0133", "sel48", "sel811", "sele0411"}
DENYUT = set("NVSAFLRjJaEe/Q")

ABS = lambda v: {"jenis": "mutlak", "nilai": v}
REL = lambda v: {"jenis": "relatif", "nilai": v}
TOL_QT = {"qt_ms": ABS(20.0), "qtcb_ms": ABS(20.0), "qtcf_ms": ABS(20.0)}
TOL_WAKTU = {"hr_bpm": ABS(2.0), "sdnn_ms": REL(0.10), "rmssd_ms": REL(0.10)}

TEKS_QT = (
    "Record `{r}` (WFDB format: {r}.hea, {r}.dat; two ECG channels). Consider only the beats whose R peak lies "
    "between sample {a} and sample {b} (inclusive, 0-based sample index). For each such beat, QT is measured as "
    "in multi-lead manual measurement: from the earliest QRS onset to the latest end of the T wave, taking both "
    "channels into account. RR = interval from the previous beat's R peak to this beat's R peak, in seconds; "
    "skip QTc for the first beat in the window. Report the mean QT in milliseconds over these beats, the mean "
    "Bazett-corrected QTc (QT / sqrt(RR)) and the mean Fridericia-corrected QTc (QT / cbrt(RR)), both in "
    "milliseconds. Answer as FINAL: {{\"qt_ms\": <number>, \"qtcb_ms\": <number>, \"qtcf_ms\": <number>}}.")
TEKS_HRV = (
    "Record `{r}` (WFDB format: {r}.hea, {r}.dat). Use the channel named `{kanal}`. Consider only the beats "
    "whose R peak lies between sample {a} and sample {b} (inclusive, 0-based sample index); NN intervals are "
    "the intervals between successive such beats. Report: mean heart rate in beats per minute (60000 / mean NN "
    "in ms); SDNN in ms (sample standard deviation of NN); RMSSD in ms; pNN50 in percent (share of successive "
    "NN differences greater than 50 ms); LF power (0.04-0.15 Hz) and HF power (0.15-0.40 Hz) of the NN series, "
    "both in ms^2; and LF/HF. Answer as FINAL: {{\"hr_bpm\": <number>, \"sdnn_ms\": <number>, \"rmssd_ms\": "
    "<number>, \"pnn50_pct\": <number>, \"lf_ms2\": <number>, \"hf_ms2\": <number>, \"lf_hf\": <number>}}.")
TEKS_WAKTU = (
    "Record `{r}` (WFDB format: {r}.hea, {r}.dat). Use the channel named `{kanal}`. Consider only the beats "
    "whose R peak lies between sample {a} and sample {b} (inclusive, 0-based sample index); NN intervals are "
    "the intervals between successive such beats. Report mean heart rate in beats per minute (60000 / mean NN "
    "in ms), SDNN in ms (sample standard deviation of NN) and RMSSD in ms. Answer as FINAL: {{\"hr_bpm\": "
    "<number>, \"sdnn_ms\": <number>, \"rmssd_ms\": <number>}}.")
TEKS_EKTOPIK = (
    "Record `{r}` (WFDB format: {r}.hea, {r}.dat). Use the channel named `MLII`. Consider only the beats whose "
    "R peak lies between sample {a} and sample {b} (inclusive, 0-based sample index). Report: mean heart rate "
    "in beats per minute over all beats (60000 / mean of all successive R-R intervals in ms); and SDNN and "
    "RMSSD in ms computed on NN intervals only, i.e. intervals between two successive beats that are both "
    "normal sinus beats (exclude every interval that starts or ends at an ectopic beat). Answer as FINAL: "
    "{{\"hr_bpm\": <number>, \"sdnn_nn_ms\": <number>, \"rmssd_nn_ms\": <number>}}.")


def berkas(rel, r):
    return [f"{rel}/{r}.hea", f"{rel}/{r}.dat"]


def tugas_qt(rng):
    F = os.path.join(DATA, QT_REL)
    calon = []
    for r in sorted(os.path.basename(p)[:-4] for p in os.listdir(F) if p.endswith(".q1c")):
        if r in PILOT:
            continue
        fs = wfdb.rdheader(os.path.join(F, r)).fs
        d = sorted(R.denyut_qt(r, "q1c"))
        if len(d) < 2:
            continue
        ext = "atr" if os.path.exists(os.path.join(F, r + ".atr")) else "pu0"
        ann = wfdb.rdann(os.path.join(F, r), ext)
        semua = np.array([x for x, s in zip(ann.sample, ann.symbol) if s in DENYUT])
        runs = [[d[0]]]
        for p, c in zip(d, d[1:]):
            lain = np.sum((semua > p[0] + 10) & (semua < c[0] - 10))
            if lain == 0 and (c[0] - p[0]) / fs < 2.0:
                runs[-1].append(c)
            else:
                runs.append([c])
        best = max(runs, key=len)
        a, b = best[0][0] - 10, best[-1][0] + 10
        if len(best) >= 10 and np.sum((semua >= a) & (semua <= b)) <= len(best):
            calon.append((r, fs, best))
    pilih = sorted(rng.sample(calon, 45), key=lambda x: x[0])
    T, J = [], []
    for r, fs, best in pilih:
        s = R.ringkas(best, fs)
        a, b = best[0][0] - 10, best[-1][0] + 10
        i = f"qt_{r}"
        T.append({"id": i, "berkas": berkas(QT_REL, r), "teks": TEKS_QT.format(r=r, a=a, b=b)})
        J.append({"id": i, "jenis": "qt", "nilai": {"qt_ms": round(s["qt"], 2), "qtcb_ms": round(s["qtcb"], 2),
                  "qtcf_ms": round(s["qtcf"], 2)}, "tol": TOL_QT, "denyut": s["n"]})
    return T, J, len(calon)


def tugas_hrv(H):
    T, J = [], []
    for d in H:
        r = d["rekaman"]
        i = f"hrv_{r}"
        T.append({"id": i, "berkas": berkas(FAN_REL, r),
                  "teks": TEKS_HRV.format(r=r, kanal="ECG", a=d["sampel_awal"], b=d["sampel_akhir"])})
        tol = dict(TOL_WAKTU, pnn50_pct=ABS(5.0))
        for k, kk in [("lf", "lf_ms2"), ("hf", "hf_ms2"), ("lfhf", "lf_hf")]:
            tol[kk] = REL(round(max(0.20, 1.5 * abs(d[f"{k}_a"] - d[f"{k}_b"]) / d[f"{k}_b"]), 4))
        J.append({"id": i, "jenis": "hrv", "nilai": {
            "hr_bpm": round(d["hr_bpm"], 3), "sdnn_ms": round(d["sdnn_ms"], 3), "rmssd_ms": round(d["rmssd_ms"], 3),
            "pnn50_pct": round(d["pnn50_pct"], 3), "lf_ms2": round(d["lf_b"], 3), "hf_ms2": round(d["hf_b"], 3),
            "lf_hf": round(d["lfhf_b"], 4)}, "tol": tol, "denyut": d["n_denyut"]})
    return T, J


def turunan(d, nama, fs_baru=None, tukar=False):
    """Cuts a Fantasia record to its window ±60 s; optionally resamples it or moves the ECG channel to index 0."""
    r, fs = d["rekaman"], d["fs"]
    a0 = max(0, d["sampel_awal"] - 60 * fs)
    rec = wfdb.rdrecord(os.path.join(DATA, FAN_REL, r), sampfrom=a0, sampto=d["sampel_akhir"] + 1 + 60 * fs)
    sig, nama_k, unit = rec.p_signal, list(rec.sig_name), list(rec.units)
    a, b = d["sampel_awal"] - a0, d["sampel_akhir"] - a0
    fs_tulis = fs
    if fs_baru:
        from math import gcd
        g = gcd(int(fs_baru), int(fs))
        sig = resample_poly(sig, int(fs_baru) // g, int(fs) // g, axis=0)
        a, b = int(round(a * fs_baru / fs)), int(round((b + 1) * fs_baru / fs)) - 1
        fs_tulis = fs_baru
    if tukar:
        k = nama_k.index("ECG")
        urut = [k] + [j for j in range(len(nama_k)) if j != k]
        sig, nama_k, unit = sig[:, urut], [nama_k[j] for j in urut], [unit[j] for j in urut]
    out = os.path.join(DATA, TUR_REL)
    os.makedirs(out, exist_ok=True)
    wfdb.wrsamp(nama, fs=fs_tulis, units=unit, sig_name=nama_k, p_signal=sig, fmt=["16"] * len(nama_k),
                write_dir=out)
    return a, b, fs_tulis, nama_k


def tugas_ektopik(rng):
    F = os.path.join(DATA, MIT_REL)
    calon = []
    for r in sorted(open(os.path.join(F, "RECORDS")).read().split()):
        h = wfdb.rdheader(os.path.join(F, r))
        if "MLII" not in h.sig_name:
            continue
        ann = wfdb.rdann(os.path.join(F, r), "atr")
        fs, lebar = h.fs, 300 * h.fs
        ritme, ritme_di = "(N", []
        for x, s, aux in zip(ann.sample, ann.symbol, ann.aux_note):
            if s == "+":
                ritme = aux.strip("\x00")
            ritme_di.append(ritme)
        for k in range(int(h.sig_len // lebar)):
            m = [(x, s, rt) for x, s, rt in zip(ann.sample, ann.symbol, ritme_di) if k * lebar <= x < (k + 1) * lebar]
            if any(rt not in ("(N", "(B", "(T") for _, _, rt in m) or any(s in "|!x[]" for _, s, _ in m):
                continue
            bt = [(x, s) for x, s, _ in m if s in DENYUT]
            sim = Counter(s for _, s in bt)
            if set(sim) - {"N", "V", "A", "F"} or not (10 <= sim["V"] + sim["A"] + sim["F"] <= 80):
                continue
            x = np.array([b[0] for b in bt])
            s = [b[1] for b in bt]
            rr = np.diff(x) / fs * 1000
            nn = np.array([rr[i] for i in range(len(rr)) if s[i] == "N" and s[i + 1] == "N"])
            nn_suk = [rr[i + 1] - rr[i] for i in range(len(rr) - 1)
                      if s[i] == "N" and s[i + 1] == "N" and s[i + 2] == "N"]
            if np.std(rr, ddof=1) / np.std(nn, ddof=1) < 1.3:
                continue
            calon.append(dict(r=r, a=int(x[0]) - 10, b=int(x[-1]) + 10, n=len(bt), ektopik=sim["V"] + sim["A"] + sim["F"],
                              hr=60000 / rr.mean(), sdnn_nn=float(np.std(nn, ddof=1)),
                              rmssd_nn=float(np.sqrt(np.mean(np.square(nn_suk)))),
                              sdnn_rr=float(np.std(rr, ddof=1))))
            break
    pilih = sorted(rng.sample(calon, 6), key=lambda c: c["r"])
    T, J = [], []
    for c in pilih:
        i = f"jebak_ektopik_{c['r']}"
        T.append({"id": i, "berkas": berkas(MIT_REL, c["r"]), "teks": TEKS_EKTOPIK.format(r=c["r"], a=c["a"], b=c["b"])})
        J.append({"id": i, "jenis": "jebakan_ektopik", "nilai": {"hr_bpm": round(c["hr"], 3),
                  "sdnn_nn_ms": round(c["sdnn_nn"], 3), "rmssd_nn_ms": round(c["rmssd_nn"], 3)},
                  "tol": {"hr_bpm": ABS(2.0), "sdnn_nn_ms": REL(0.10), "rmssd_nn_ms": REL(0.10)},
                  "denyut": c["n"], "ektopik": c["ektopik"], "sdnn_rr_ms": round(c["sdnn_rr"], 3)})
    return T, J, len(calon)


def main():
    rng = random.Random(BENIH)
    H = json.load(open(os.path.join(SINI, "agenekg_rujukan_hrv.json"), encoding="utf-8"))
    T, J, n_qt = tugas_qt(rng)
    t, j = tugas_hrv(H)
    T += t
    J += j
    t, j, n_mit = tugas_ektopik(rng)
    T += t
    J += j
    t, j = tugas_turunan(rng, H)
    T += t
    J += j
    t, j = tugas_takterjawab(rng, H, {x["id"][3:] for x in J if x["jenis"] == "qt"})
    T += t
    J += j
    periksa_berkas(T)
    json.dump(T, open(os.path.join(SINI, "agenekg_tugas.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(J, open(os.path.join(SINI, "agenekg_rujukan.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    cetak_ringkasan(J, n_qt, n_mit)


def tugas_turunan(rng, H):
    """Other sampling rate (5) and swapped channels (4), each from a different Fantasia record, named tr01..tr09."""
    T, J = [], []
    for n, d in enumerate(rng.sample(H, 9), 1):
        nama = f"tr{n:02d}"
        if n <= 5:
            fs_baru = 500 if n <= 3 else 360
            a, b, fs_t, _ = turunan(d, nama, fs_baru=fs_baru)
            i, jenis = f"jebak_laju_{nama}", "jebakan_laju"
        else:
            a, b, fs_t, _ = turunan(d, nama, tukar=True)
            i, jenis = f"jebak_kanal_{nama}", "jebakan_kanal"
        T.append({"id": i, "berkas": berkas(TUR_REL, nama), "teks": TEKS_WAKTU.format(r=nama, kanal="ECG", a=a, b=b)})
        J.append({"id": i, "jenis": jenis, "asal": d["rekaman"], "fs": fs_t, "nilai": {
            "hr_bpm": round(d["hr_bpm"], 3), "sdnn_ms": round(d["sdnn_ms"], 3), "rmssd_ms": round(d["rmssd_ms"], 3)},
            "tol": TOL_WAKTU, "denyut": d["n_denyut"]})
    return T, J


def tugas_takterjawab(rng, H, qt_dipakai):
    """Lead V5, absent from Fantasia (3), and a window beyond the end of an unused QTDB record (2)."""
    T, J = [], []
    for d in rng.sample(H, 3):
        r = d["rekaman"]
        i = f"jebak_takada_{r}"
        T.append({"id": i, "berkas": berkas(FAN_REL, r),
                  "teks": TEKS_WAKTU.format(r=r, kanal="V5", a=d["sampel_awal"], b=d["sampel_akhir"])})
        J.append({"id": i, "jenis": "jebakan_takterjawab", "nilai": {"unanswerable": True}, "tol": {}})
    sisa = sorted(os.path.basename(p)[:-4] for p in os.listdir(os.path.join(DATA, QT_REL))
                  if p.endswith(".q1c") and os.path.basename(p)[:-4] not in PILOT | qt_dipakai)
    for r in rng.sample(sisa, 2):
        n = wfdb.rdheader(os.path.join(DATA, QT_REL, r)).sig_len
        i = f"jebak_takada_{r}"
        T.append({"id": i, "berkas": berkas(QT_REL, r), "teks": TEKS_QT.format(r=r, a=n + 5000, b=n + 15000)})
        J.append({"id": i, "jenis": "jebakan_takterjawab", "nilai": {"unanswerable": True}, "tol": {}})
    return T, J


def periksa_berkas(T):
    assert len({t["id"] for t in T}) == len(T)
    for t in T:
        for f in t["berkas"]:
            assert os.path.exists(os.path.join(DATA, f)), f


def cetak_ringkasan(J, n_qt, n_mit):
    print(f"Calon QT (rangkaian bersih ≥ 10 denyut, di luar pilot): {n_qt}; calon jendela ektopik MIT-BIH: {n_mit}.\n")
    print("| Jenis | Tugas |\n|---|---|")
    for k, v in sorted(Counter(j["jenis"] for j in J).items()):
        print(f"| {k} | {v} |")
    print(f"| **jumlah** | **{len(J)}** |\n")
    print("Jebakan ektopik: " + "; ".join(f"{j['id'][14:]} ektopik {j['ektopik']}, SDNN NN {j['nilai']['sdnn_nn_ms']:.1f} "
                                          f"vs RR {j['sdnn_rr_ms']:.1f} ms" for j in J if j["jenis"] == "jebakan_ektopik"))
    print("Turunan: " + "; ".join(f"{j['id'].split('_')[-1]} = {j['asal']} ({j['jenis'][8:]}, {j['fs']} Hz)"
                                  for j in J if "asal" in j))
    print("Tak terjawab: " + ", ".join(j["id"][13:] for j in J if j["jenis"] == "jebakan_takterjawab"))
    qt = [j for j in J if j["jenis"] == "qt"]
    print(f"QT: denyut per tugas median {np.median([j['denyut'] for j in qt]):.0f} "
          f"(rentang {min(j['denyut'] for j in qt)}–{max(j['denyut'] for j in qt)}); QT rujukan median "
          f"{np.median([j['nilai']['qt_ms'] for j in qt]):.0f} ms.")


if __name__ == "__main__":
    main()
