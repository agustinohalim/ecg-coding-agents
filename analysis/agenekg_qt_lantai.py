"""QT floor checks requested by JIKI panel 1 (22 Nov 2026), after all results; none is in the preregistration.

1. Agent minus constant answer: per-task difference in the share of quantities within tolerance (10, 20, 40 ms for
   QT; fixed 20 % frequency tolerance for HRV), mean over tasks with a 95 % bootstrap CI (10,000 resamples of tasks).
2. Continuous agreement on the QT tasks: per task, the median numeric answer over repeats against the reference;
   median absolute error, median signed error, Spearman rho, and Theil-Sen slope, each with a task-bootstrap CI;
   and, paired by task, the agent's absolute error minus the leave-one-out constant's (median, task-bootstrap CI).
3. A constant that uses no evaluated reference: the median QT, QTcB, and QTcF of the eligible QT Database records
   that are not among the 45 tasks (same longest-run rule as the task generator), scored on the 45 tasks.

    python -X utf8 agenekg_qt_lantai.py <analysis folder> <runs folder> <qtdb folder>
"""
import random
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy import stats

from agenekg_tambahan_jiki import BENIH, MODEL, Paket, baris_run, konstan

QT = ("qt_ms", "qtcb_ms", "qtcf_ms")
ULANG = 10_000


def ci(nilai_per_tugas, fungsi, rng):
    """Point estimate and 95 % percentile CI of fungsi over tasks resampled with replacement."""
    kunci = list(nilai_per_tugas)
    ulang = [fungsi([nilai_per_tugas[k] for k in rng.choices(kunci, k=len(kunci))]) for _ in range(ULANG)]
    return fungsi(list(nilai_per_tugas.values())), np.percentile(ulang, 2.5), np.percentile(ulang, 97.5)


def proporsi_per_tugas(baris, kolom):
    per = {}
    for b in baris:
        a, n = per.get(b["tugas"], (0, 0))
        per[b["tugas"]] = (a + sum(bool(x[kolom]) for x in b["besaran"]), n + len(b["besaran"]))
    return {t: a / n for t, (a, n) in per.items()}


def konstan_qt(rujukan):
    """Leave-one-out median rows for the QT tasks with the 10, 20, and 40 ms columns of Table 1."""
    qt = {t: r["nilai"] for t, r in rujukan.ruj.items() if r["jenis"] == "qt"}
    baris = []
    for t, nilai in qt.items():
        salah = [abs(statistics.median(v[q] for u, v in qt.items() if u != t) - nilai[q]) for q in QT]
        baris.append({"tugas": t, "jenis": "qt",
                      "besaran": [{"ketat": s <= 10, "benar": s <= 20, "longgar": s <= 40} for s in salah]})
    return baris


def selisih(data, konst, rng):
    """Rows (model, type, column, mean difference, CI low, CI high) for agent minus constant."""
    hasil = []
    for m, rows in data.items():
        for jenis, kolom_list in (("qt", ("ketat", "benar", "longgar")), ("hrv", ("benar",))):
            for kolom in kolom_list:
                a = proporsi_per_tugas([bt for _, _, bt in rows if bt["jenis"] == jenis], kolom)
                k = proporsi_per_tugas([r for r in konst if r["jenis"] == jenis], kolom)
                beda = {t: a[t] - k[t] for t in a}
                hasil.append((m, jenis, kolom, *ci(beda, statistics.fmean, rng)))
    return hasil


def kontinu(data, rujukan, rng):
    """Rows (model, quantity, tasks with an answer, MAE, bias, rho, slope), each a (point, low, high) tuple."""
    hasil = []
    for m, rows in list(data.items()) + [("constant (leave-one-out)", None)]:
        for q in QT:
            pasang = {}
            for t, r in rujukan.ruj.items():
                if r["jenis"] != "qt":
                    continue
                ref = r["nilai"][q]
                if rows is None:
                    jaw = [statistics.median(o["nilai"][q] for u, o in rujukan.ruj.items() if o["jenis"] == "qt" and u != t)]
                else:
                    jaw = [x["agen"] for _, b, _ in rows if b["tugas"] == t for x in b["besaran"]
                           if x["besaran"] == q and isinstance(x["agen"], (int, float)) and x["agen"] != 0]
                if jaw:
                    pasang[t] = (statistics.median(jaw), ref)
            if len(pasang) < 5:
                hasil.append((m, q, len(pasang), None, None, None, None))
                continue
            hasil.append((m, q, len(pasang),
                          ci(pasang, lambda p: statistics.median(abs(a - r) for a, r in p), rng),
                          ci(pasang, lambda p: statistics.median(a - r for a, r in p), rng),
                          ci(pasang, lambda p: stats.spearmanr([a for a, _ in p], [r for _, r in p])[0], rng),
                          ci(pasang, lambda p: stats.theilslopes([a for a, _ in p], [r for _, r in p])[0], rng)))
    return hasil


def lebih_dekat(data, rujukan, rng):
    """Per model and quantity: mean per-task (|agent - ref| - |constant - ref|) in ms with CI, and tasks closer."""
    qt = {t: r["nilai"] for t, r in rujukan.ruj.items() if r["jenis"] == "qt"}
    hasil = []
    for m, rows in data.items():
        for q in QT:
            beda = {}
            for t, nilai in qt.items():
                jaw = [x["agen"] for _, b, _ in rows if b["tugas"] == t for x in b["besaran"]
                       if x["besaran"] == q and isinstance(x["agen"], (int, float)) and x["agen"] != 0]
                if jaw:
                    c = statistics.median(v[q] for u, v in qt.items() if u != t)
                    beda[t] = abs(statistics.median(jaw) - nilai[q]) - abs(c - nilai[q])
            if len(beda) >= 20:
                hasil.append((m, q, len(beda), sum(d < 0 for d in beda.values()), ci(beda, statistics.median, rng)))
    return hasil


def konstan_luar(qtdb, rujukan):
    """Median QT, QTcB, QTcF over eligible QT Database records outside the 45 tasks, and their hit rates."""
    import agenekg_rujukan_qt as R
    import wfdb
    R.FOLDER = str(qtdb)
    dipakai = {r["id"][3:] for r in rujukan.ruj.values() if r["jenis"] == "qt"}
    pilot = {"sele0111", "sele0133", "sel48", "sel811", "sele0411"}
    luar = []
    for p in sorted(Path(qtdb).glob("*.q1c")):
        rek = p.stem
        if rek in dipakai or rek in pilot:
            continue
        fs = wfdb.rdheader(str(Path(qtdb) / rek)).fs
        d = sorted(R.denyut_qt(rek, "q1c"))
        ann = wfdb.rdann(str(Path(qtdb) / rek), "atr" if (Path(qtdb) / f"{rek}.atr").exists() else "pu0")
        semua = np.array([x for x, s in zip(ann.sample, ann.symbol) if s in R.DENYUT])
        runs = [[d[0]]] if d else []
        for a, c in zip(d, d[1:]):
            if np.sum((semua > a[0] + 10) & (semua < c[0] - 10)) == 0 and (c[0] - a[0]) / fs < 2.0:
                runs[-1].append(c)
            else:
                runs.append([c])
        best = max(runs, key=len) if runs else []
        a0, b0 = (best[0][0] - 10, best[-1][0] + 10) if best else (0, 0)
        if len(best) >= 10 and np.sum((semua >= a0) & (semua <= b0)) <= len(best):
            s = R.ringkas(best, fs)
            luar.append((s["qt"], s["qtcb"], s["qtcf"]))
    median = dict(zip(QT, np.median(np.array(luar), axis=0)))
    kena = {}
    for tol in (10, 20, 40):
        benar = [abs(median[q] - r["nilai"][q]) <= tol for r in rujukan.ruj.values() if r["jenis"] == "qt" for q in QT]
        kena[tol] = (sum(benar), len(benar))
    return len(luar), median, kena


def main():
    analisis, runs, qtdb = (Path(a) for a in sys.argv[1:4])
    pkg = Paket(analisis)
    from penilaian import skor
    pkg.skor = skor
    rujukan = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                               analisis / "agenekg_rujukan_hrv.json")
    data = {m: baris_run(runs / m, rujukan, pkg) for m in MODEL}
    rng = random.Random(BENIH)
    print("## 1. Agent minus constant answer, mean per-task difference in points (95 % task-bootstrap CI)\n")
    for m, j, kol, est, lo, hi in selisih(data, konstan_qt(rujukan) + [r for r in konstan(rujukan, pkg)["tetap"] if r["jenis"] == "hrv"], rng):
        print(f"- {m}, {j}, {kol}: {100 * est:+.1f} ({100 * lo:+.1f} to {100 * hi:+.1f})")
    print("\n## 2. Continuous agreement on QT tasks (per-task median answer vs reference; 95 % task-bootstrap CI)\n")
    print("| Model | Quantity | Tasks | Median abs error (ms) | Median signed error (ms) | Spearman rho | Theil-Sen slope |")
    print("|---|---|---|---|---|---|---|")
    for m, q, n, *met in kontinu(data, rujukan, rng):
        sel = ["—" if x is None else f"{x[0]:.2f} ({x[1]:.2f} to {x[2]:.2f})" for x in met]
        print(f"| {m} | {q} | {n} | " + " | ".join(sel) + " |")
    print("\nPaired: per-task |answer - ref| minus |constant - ref| (ms), median over tasks (95 % CI); tasks closer\n")
    for m, q, n, dekat, (est, lo, hi) in lebih_dekat(data, rujukan, rng):
        print(f"- {m}, {q}: {est:+.1f} ({lo:+.1f} to {hi:+.1f}); agent closer on {dekat}/{n} tasks")
    n, median, kena = konstan_luar(qtdb, rujukan)
    print(f"\n## 3. Constant from {n} eligible QT Database records outside the tasks\n")
    print("Median: " + ", ".join(f"{q} {v:.1f} ms" for q, v in median.items()))
    for tol, (a, b) in kena.items():
        print(f"- {tol} ms: {a}/{b} ({100 * a / b:.1f} %)")


if __name__ == "__main__":
    main()
