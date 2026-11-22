"""Library-only NeuroKit2 baseline for AgenEKG (exploratory; preregistration, deviation of 19 November 2026).

A fixed pipeline with no language model runs in the same `agenekg-py:1` container as the agents (neurokit2
0.3.0, no network) on every answerable task. Its output is written in the agent log format (`<task>_u1.json`,
one turn with exit code 0, FINAL = the JSON answer), so `agenekg_analisis.py` scores it with the same references
and tolerances.

  QT     per channel: ecg_clean + ecg_peaks + ecg_delineate(method); beats = first-channel R peaks in the
         window; QT = earliest QRS onset to latest T end over both channels (R peaks paired across channels
         when <= 50 ms apart); RR from the previous first-channel R peak; QTc skipped for the first beat.
  HRV    channel named in the task text; default ecg_clean + ecg_peaks; NN = peak-to-peak intervals in the
         window, no ectopic correction; SDNN (ddof 1), RMSSD, pNN50; LF/HF from hrv_frequency(normalize=False).

The in-container script `DALAM` is kept exactly as it ran.

Usage:
    python -X utf8 analysis/agenekg_dasar_nk.py --metode dwt --keluar <output folder>
"""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

DIR = Path(__file__).resolve().parent
GAMBAR = "agenekg-py:1"

DALAM = r'''
import json, re, sys, traceback
import numpy as np, wfdb, neurokit2 as nk

import os
metode = sys.argv[1]
ke, dari = (int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else "0/1").split("/"))
tugas = json.load(open("/work/tugas.json", encoding="utf-8"))
ruj = {r["id"]: r for r in json.load(open("/work/rujukan.json", encoding="utf-8"))}


def jendela(teks):
    m = re.search(r"between sample (\d+) and sample (\d+)", teks)
    return int(m.group(1)), int(m.group(2))


def puncak(x, fs):
    bersih = nk.ecg_clean(x, sampling_rate=fs)
    _, info = nk.ecg_peaks(bersih, sampling_rate=fs)
    return bersih, np.asarray(info["ECG_R_Peaks"], dtype=int)


def qt(rec, a, b):
    fs, sig = rec.fs, rec.p_signal
    per_kanal = []
    for ch in range(sig.shape[1]):
        bersih, r = puncak(sig[:, ch], fs)
        _, w = nk.ecg_delineate(bersih, r, sampling_rate=fs, method=metode)
        on = np.asarray(w.get("ECG_R_Onsets", w.get("ECG_Q_Peaks")), dtype=float)
        off = np.asarray(w["ECG_T_Offsets"], dtype=float)
        per_kanal.append((r, on, off))
    r0 = per_kanal[0][0]
    idx = np.where((r0 >= a) & (r0 <= b))[0]
    qts, qtcb, qtcf = [], [], []
    for j, i in enumerate(idx):
        ons, offs = [], []
        for r, on, off in per_kanal:
            k = int(np.argmin(np.abs(r - r0[i])))
            if abs(r[k] - r0[i]) <= 0.05 * fs:
                if k < len(on) and np.isfinite(on[k]):
                    ons.append(on[k])
                if k < len(off) and np.isfinite(off[k]):
                    offs.append(off[k])
        if not ons or not offs:
            continue
        q = (max(offs) - min(ons)) / fs * 1000.0
        if q <= 0:
            continue
        qts.append(q)
        if j > 0 and i > 0:
            rr = (r0[i] - r0[i - 1]) / fs
            if rr < 2.0:
                qtcb.append(q / np.sqrt(rr))
                qtcf.append(q / np.cbrt(rr))
    return {"qt_ms": float(np.mean(qts)), "qtcb_ms": float(np.mean(qtcb)), "qtcf_ms": float(np.mean(qtcf))}


def hrv(rec, a, b, nama, kunci):
    fs = rec.fs
    ch = rec.sig_name.index(nama)
    _, r = puncak(rec.p_signal[:, ch], fs)
    r = r[(r >= a) & (r <= b)]
    nn = np.diff(r) / fs * 1000.0
    d = np.diff(nn)
    nilai = {"hr_bpm": 60000.0 / nn.mean(), "sdnn_ms": nn.std(ddof=1), "rmssd_ms": np.sqrt(np.mean(d ** 2)),
             "pnn50_pct": 100.0 * np.mean(np.abs(d) > 50)}
    if "lf_ms2" in kunci:
        f = nk.hrv_frequency(r, sampling_rate=fs, normalize=False)
        nilai.update(lf_ms2=f["HRV_LF"].iloc[0], hf_ms2=f["HRV_HF"].iloc[0], lf_hf=f["HRV_LFHF"].iloc[0])
    nilai["sdnn_nn_ms"], nilai["rmssd_nn_ms"] = nilai["sdnn_ms"], nilai["rmssd_ms"]
    return {k: float(nilai[k]) for k in kunci}


for nomor, t in enumerate(tugas):
    r = ruj[t["id"]]
    if r["nilai"].get("unanswerable") or nomor % dari != ke or os.path.exists("/out/%s_u1.json" % t["id"]):
        continue
    giliran = {"model": "(pipa tetap NeuroKit2, metode %s)" % metode, "kode_keluar": "0", "keluaran": ""}
    final = None
    try:
        rec = wfdb.rdrecord("/data/" + t["berkas"][0][:-4])
        a, b = jendela(t["teks"])
        if r["jenis"] == "qt":
            jawab = qt(rec, a, b)
        else:
            nama = re.search(r"channel named `([^`]+)`", t["teks"]).group(1)
            jawab = hrv(rec, a, b, nama, list(r["nilai"]))
        final = json.dumps(jawab)
    except Exception:
        giliran.update(kode_keluar="1", keluaran=traceback.format_exc()[-4000:])
    log = {"tugas": t["id"], "model": "neurokit2-dasar-" + metode, "ulang": 1, "giliran": [giliran], "final": final}
    json.dump(log, open("/out/%s_u1.json" % t["id"], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(t["id"], "ok" if final else "GAGAL", flush=True)
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metode", default="dwt", choices=["dwt", "peak", "cwt"])
    ap.add_argument("--keluar", required=True)
    ap.add_argument("--bagian", default="0/1", help="i/n: run task k when k mod n = i (the pipeline is deterministic, "
                    "so the split does not change results); tasks with existing output are skipped")
    ap.add_argument("--data", default="C:/Data/PhysioNet")
    ap.add_argument("--tugas", default=str(DIR / "agenekg_tugas.json"))
    ap.add_argument("--rujukan", default=str(DIR / "agenekg_rujukan.json"))
    a = ap.parse_args()
    keluar = Path(a.keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as kerja:
        kerja = Path(kerja)
        (kerja / "dasar.py").write_text(DALAM, encoding="utf-8")
        shutil.copyfile(a.tugas, kerja / "tugas.json")
        shutil.copyfile(a.rujukan, kerja / "rujukan.json")
        perintah = ["docker", "run", "--rm", "--network", "none", "--memory", "4g", "--cpus", "2",
                    "-v", f"{kerja.resolve()}:/work:ro", "-v", f"{Path(a.data).resolve()}:/data:ro",
                    "-v", f"{keluar.resolve()}:/out", "-w", "/work", GAMBAR, "python", "dasar.py", a.metode, a.bagian]
        subprocess.run(perintah, check=True)


if __name__ == "__main__":
    main()
