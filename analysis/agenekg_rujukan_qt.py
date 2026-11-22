"""QT/QTc reference values from the manual annotations of the QT Database (qtdb 1.0.0, ODC-By 1.0).

For each record: the beats annotated in `.q1c` (annotator 1, second pass) give QT per beat = end of T minus
QRS onset. RR = distance to the previous annotated beat's peak when < 2 s (consecutive beats).
Bazett QTc = QT / sqrt(RR), Fridericia = QT / RR^(1/3), RR in seconds.

Also the inter-annotator spread (`.q1c` vs `.q2c`, 11 records): the difference in mean QT per record, used
as the lower bound of the tolerance in the preregistration. No agent or language model is involved.

Usage:
    python -X utf8 analysis/agenekg_rujukan_qt.py [qtdb folder] > output.md
"""
import glob
import os
import sys

import numpy as np
import wfdb

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "C:/Data/PhysioNet/qtdb/data/qt-database-1.0.0"
DENYUT = set("NVSAFLRjJaEe/Q")


def denyut_qt(rek, ekst):
    """(peak, qrs_onset, t_end) for every beat annotated with all three."""
    a = wfdb.rdann(os.path.join(FOLDER, rek), ekst)
    s, x = a.symbol, a.sample
    hasil = []
    for i, sim in enumerate(s):
        if sim not in DENYUT:
            continue
        awal = x[i - 1] if i > 0 and s[i - 1] == "(" else None
        akhir = None
        for j in range(i + 1, len(s)):
            if s[j] in DENYUT:
                break
            if s[j] == "t":
                if j + 1 < len(s) and s[j + 1] == ")":
                    akhir = x[j + 1]
                break
        if awal is not None and akhir is not None:
            hasil.append((int(x[i]), int(awal), int(akhir)))
    return hasil


def ringkas(d, fs):
    qt = np.array([(t - q) / fs for _, q, t in d])
    puncak = np.array([p for p, _, _ in d])
    rr = np.full(len(d), np.nan)
    rr[1:] = np.diff(puncak) / fs
    rr[rr >= 2.0] = np.nan
    ok = ~np.isnan(rr)
    return dict(
        n=len(d), n_rr=int(ok.sum()),
        qt=1000 * qt.mean(),
        qtcb=1000 * np.mean(qt[ok] / np.sqrt(rr[ok])) if ok.any() else np.nan,
        qtcf=1000 * np.mean(qt[ok] / np.cbrt(rr[ok])) if ok.any() else np.nan,
        awal=int(puncak.min()), akhir=int(puncak.max()),
    )


def main():
    rek = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(FOLDER, "*.q1c")))
    baris = []
    for r in rek:
        fs = wfdb.rdheader(os.path.join(FOLDER, r)).fs
        d = denyut_qt(r, "q1c")
        baris.append((r, fs, ringkas(d, fs) if len(d) >= 2 else None))
    layak = [b for b in baris if b[2] and b[2]["n_rr"] >= 5]
    print("## 1. Rujukan QT/QTc per rekaman (annotator 1, `.q1c`)\n")
    print(f"Rekaman dengan `.q1c`: {len(baris)}; layak (≥ 5 denyut dengan RR beruntun): {len(layak)}.\n")
    qts = np.array([b[2]["qt"] for b in layak])
    print(f"QT rata-rata per rekaman (ms): median {np.median(qts):.0f}, rentang {qts.min():.0f}–{qts.max():.0f}. "
          f"Denyut per rekaman layak: median {np.median([b[2]['n'] for b in layak]):.0f}.\n")
    print("| Rekaman | fs | denyut | denyut ber-RR | jendela sampel | QT (ms) | QTcB (ms) | QTcF (ms) |")
    print("|---|---|---|---|---|---|---|---|")
    for r, fs, s in baris:
        if s is None:
            print(f"| {r} | {fs} | <2 | – | – | – | – | – |")
            continue
        print(f"| {r} | {fs:g} | {s['n']} | {s['n_rr']} | {s['awal']}–{s['akhir']} | {s['qt']:.1f} | "
              f"{s['qtcb']:.1f} | {s['qtcf']:.1f} |")

    print("\n## 2. Sebaran antar-annotator (`.q1c` vs `.q2c`)\n")
    print("| Rekaman | denyut cocok | QT a1 (ms) | QT a2 (ms) | |beda| rata-rata (ms) | |beda| per denyut, median (ms) |")
    print("|---|---|---|---|---|---|")
    beda = []
    for p in sorted(glob.glob(os.path.join(FOLDER, "*.q2c"))):
        r = os.path.basename(p)[:-4]
        fs = wfdb.rdheader(os.path.join(FOLDER, r)).fs
        d1 = {pk: (q, t) for pk, q, t in denyut_qt(r, "q1c")}
        d2 = denyut_qt(r, "q2c")
        pas = []
        for pk, q, t in d2:
            k = min(d1, key=lambda z: abs(z - pk), default=None)
            if k is not None and abs(k - pk) <= 0.04 * fs:
                pas.append(((d1[k][1] - d1[k][0]) / fs, (t - q) / fs))
        if not pas:
            print(f"| {r} | 0 | – | – | – | – |")
            continue
        a = 1000 * np.array(pas)
        dm = abs(a[:, 0].mean() - a[:, 1].mean())
        if len(a) >= 5:
            beda.append(dm)
        print(f"| {r} | {len(a)} | {a[:, 0].mean():.1f} | {a[:, 1].mean():.1f} | {dm:.1f} | "
              f"{np.median(abs(a[:, 0] - a[:, 1])):.1f} |")
    b = np.array(beda)
    print(f"\n|beda| QT rata-rata per rekaman (hanya rekaman dengan ≥ 5 denyut cocok): median {np.median(b):.1f} ms, maks {b.max():.1f} ms "
          f"(n = {len(b)} rekaman).")


if __name__ == "__main__":
    main()
