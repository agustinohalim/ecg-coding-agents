"""HRV reference values from the Fantasia 1.0.0 beat annotations (ODC-By 1.0); preregistration, sections 2-3.

Fantasia's `.ecg` annotations are corrected automatic detections, all with symbol `N`, so ectopic beats cannot
be removed by symbol. Window rule (fixed by the deviation of 7 November 2026):
  non-overlapping 5-minute windows from sample 0; the first window in which (1) every RR lies in 0.3-2.0 s and
  (2) every RR differs by <= 20 % from the previous RR. Records without such a window are excluded.
NN = differences between successive peaks that both lie inside the window.

Quantities: mean HR (60 / mean NN), SDNN (ddof 1), RMSSD, pNN50 (%), and LF (0.04-0.15 Hz), HF (0.15-0.40 Hz),
LF/HF from two implementations:
  (a) NeuroKit2 `hrv_frequency` with `normalize=False` (the default `True` gives normalised power, not ms^2;
      LF/HF is the same);
  (b) own: NN (ms) at beat times, cubic interpolation at 4 Hz, mean removed, Welch with a 256-point (64 s)
      Hann window and 50 % overlap, band power = trapezoidal integral (ms^2).
No agent or language model is involved. Run inside the `agenekg-py:1` container so that library versions match
the agent sandbox:

    docker run --rm -v <PhysioNet>/fantasia/data:/data:ro -v <repo>/analysis:/kode -w /kode \
        agenekg-py:1 python agenekg_rujukan_hrv.py /data/fantasia-database-1.0.0 > output.md

Output: a Markdown table on stdout; JSON per record to `agenekg_rujukan_hrv.json` in the working folder.
"""
import json
import os
import sys

import neurokit2 as nk
import numpy as np
import scipy
import wfdb
from scipy.interpolate import CubicSpline
from scipy.signal import welch

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "/data/fantasia-database-1.0.0"
JENDELA_S = 300
RR_MIN, RR_MAKS, LONCAT = 0.3, 2.0, 0.20
LF, HF = (0.04, 0.15), (0.15, 0.40)


def pilih_jendela(r, fs, n):
    """(window index, beat indices) of the first 5-minute window that passes the rule, else (None, None)."""
    lebar = JENDELA_S * fs
    for k in range(int(n // lebar)):
        a, b = k * lebar, (k + 1) * lebar
        idx = np.where((r >= a) & (r < b))[0]
        if len(idx) < 3:
            continue
        rr = np.diff(r[idx]) / fs
        if rr.min() < RR_MIN or rr.max() > RR_MAKS:
            continue
        if np.any(np.abs(np.diff(rr)) / rr[:-1] > LONCAT):
            continue
        return k, idx
    return None, None


def daya_sendiri(t_s, nn_ms):
    t4 = np.arange(t_s[0], t_s[-1], 0.25)
    x = CubicSpline(t_s, nn_ms)(t4)
    f, p = welch(x - x.mean(), fs=4.0, window="hann", nperseg=256, noverlap=128)
    pita = lambda lo, hi: float(np.trapezoid(p[(f >= lo) & (f < hi)], f[(f >= lo) & (f < hi)]))
    lf, hf = pita(*LF), pita(*HF)
    return lf, hf, lf / hf


def main():
    rekaman = sorted(open(os.path.join(FOLDER, "RECORDS")).read().split())
    hasil, dibuang = [], []
    for rek in rekaman:
        p = os.path.join(FOLDER, rek)
        h = wfdb.rdheader(p)
        fs = h.fs
        r = wfdb.rdann(p, "ecg").sample
        k, idx = pilih_jendela(r, fs, h.sig_len)
        if idx is None:
            dibuang.append(rek)
            continue
        pk = r[idx]
        nn = np.diff(pk) / fs * 1000.0
        a_lf = nk.hrv_frequency(pk - pk[0], sampling_rate=fs, normalize=False)  # the default normalize=True is not in ms²
        b_lf, b_hf, b_r = daya_sendiri(pk[1:] / fs, nn)
        hasil.append(dict(
            rekaman=rek, fs=fs, kanal_ekg=h.sig_name.index("ECG"), jendela=k,
            sampel_awal=int(k * JENDELA_S * fs), sampel_akhir=int((k + 1) * JENDELA_S * fs) - 1,
            n_denyut=int(len(pk)),
            hr_bpm=60000.0 / nn.mean(), sdnn_ms=float(nn.std(ddof=1)),
            rmssd_ms=float(np.sqrt(np.mean(np.diff(nn) ** 2))),
            pnn50_pct=float(np.mean(np.abs(np.diff(nn)) > 50) * 100),
            lf_a=float(a_lf["HRV_LF"].iloc[0]), hf_a=float(a_lf["HRV_HF"].iloc[0]),
            lfhf_a=float(a_lf["HRV_LFHF"].iloc[0]),
            lf_b=b_lf, hf_b=b_hf, lfhf_b=b_r))
    json.dump(hasil, open("agenekg_rujukan_hrv.json", "w"), indent=1)

    print(f"Versi: neurokit2 {nk.__version__}, wfdb {wfdb.__version__}, numpy {np.__version__}, "
          f"scipy {scipy.__version__}.\n")
    print(f"Rekaman: {len(rekaman)}; punya jendela lolos aturan: {len(hasil)}; dikeluarkan: {len(dibuang)} "
          f"({', '.join(dibuang) or '-'}).\n")
    print("| Rekaman | Jendela | Denyut | HR | SDNN | RMSSD | pNN50 | LF a | LF b | HF a | HF b | LF/HF a | LF/HF b |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for d in hasil:
        print(f"| {d['rekaman']} | {d['jendela']} | {d['n_denyut']} | {d['hr_bpm']:.1f} | {d['sdnn_ms']:.1f} | "
              f"{d['rmssd_ms']:.1f} | {d['pnn50_pct']:.1f} | {d['lf_a']:.4g} | {d['lf_b']:.4g} | {d['hf_a']:.4g} | "
              f"{d['hf_b']:.4g} | {d['lfhf_a']:.3f} | {d['lfhf_b']:.3f} |")
    print("\nBeda relatif implementasi |a − b| / b (median, maks):")
    for x in ["lf", "hf", "lfhf"]:
        v = np.array([abs(d[f"{x}_a"] - d[f"{x}_b"]) / d[f"{x}_b"] for d in hasil])
        print(f"- {x}: median {np.median(v):.3f}, maks {v.max():.3f}")
    print("\nJendela terpilih (indeks 5 menit): " + str(dict(zip(*np.unique([d['jendela'] for d in hasil],
                                                                         return_counts=True)))))


if __name__ == "__main__":
    main()
