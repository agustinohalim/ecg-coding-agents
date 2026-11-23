"""Exploratory checks requested by panel 3 (22 Nov 2026), before the JIKI version; none is in the preregistration.

1. Constant-answer baseline: every core quantity answered with the median reference value of that quantity over
   the other core tasks (leave-one-out), scored with the main tolerance and with the fixed 20 % HRV tolerance,
   and compared task by task with each agent (paired sign-flip permutation test of the scoring package).
2. Provenance on every run: each non-zero number in FINAL on a core task is looked up in the execution output the
   agent saw (the harness keeps the last 4,000 characters; match within 0.5 % or 0.01, as in agenekg_cek_e1.py).
3. HRV split by domain (heart rate and time domain vs frequency domain), fixed 20 % frequency tolerance.

    python -X utf8 agenekg_tambahan_jiki.py <analysis folder> <runs folder>

<runs folder> holds main_<model>/ and baseline_nk_dwt/ unzipped from transcripts/ of ecg-coding-agents.
"""
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from agenekg_cek_e1 import Paket, tercetak
from agenekg_hrv_toleransi_tetap import toleransi_tetap

MODEL = ("main_qwen25coder7b", "main_qwen25coder3b", "main_llama31_8b", "main_deepseek-v4-flash", "baseline_nk_dwt")
INTI = ("qt", "hrv")
FREKUENSI = {"lf_ms2", "hf_ms2", "lf_hf"}
BENIH = 20261122


def baris_run(dir_run, rujukan, pkg):
    """(log, row with the main tolerance, row with the fixed 20 % frequency tolerance) for every core task run."""
    tetap = pkg.skor.Rujukan(toleransi_tetap(rujukan.ruj), rujukan.tugas, {})
    hasil = []
    for f in sorted(Path(dir_run).rglob("*_u*.json")):
        log = json.loads(f.read_text(encoding="utf-8"))
        b = pkg.skor.baris_tugas_ulangan(log, rujukan)
        if b["jenis"] in INTI:
            hasil.append((log, b, pkg.skor.baris_tugas_ulangan(log, tetap)))
    return hasil


def konstan(rujukan, pkg):
    """Rows in the scoring format for the leave-one-out median answer, under both tolerances."""
    nilai = defaultdict(dict)
    for tid, r in rujukan.ruj.items():
        if r["jenis"] in INTI and not r["nilai"].get("unanswerable"):
            for k, v in r["nilai"].items():
                nilai[k][tid] = v
    tetap = toleransi_tetap(rujukan.ruj)
    baris = {"utama": defaultdict(list), "tetap": defaultdict(list)}
    for k, per_tugas in nilai.items():
        for tid, ref in per_tugas.items():
            r = rujukan.ruj[tid]
            salah = abs(statistics.median(v for t, v in per_tugas.items() if t != tid) - ref)
            d = rujukan.d_frek.get(tid, {}).get(k, 0.0)
            baris["utama"][tid].append({"benar": salah <= pkg.skor.batas(r["tol"][k], ref, d)})
            baris["tetap"][tid].append({"benar": salah <= pkg.skor.batas(tetap[tid]["tol"][k], ref, 0.0)})
    return {t: [{"tugas": tid, "jenis": rujukan.ruj[tid]["jenis"], "besaran": bs} for tid, bs in per.items()]
            for t, per in baris.items()}


def asal(log, baris, pkg):
    """Counter of (printed?, correct?) over the non-zero numeric answers of one run."""
    keluaran = "\n".join((g.get("keluaran") or "") for g in pkg.eksekusi(log))
    hasil = Counter()
    for b in baris["besaran"]:
        if b["agen"] is not None and b["agen"] != 0:
            hasil[(tercetak(float(b["agen"]), keluaran), b["benar"])] += 1
    return hasil


def ringkas_model(runs, pkg):
    """Per-model counts for checks 2 and 3."""
    c = Counter()
    for log, b, bt in runs:
        e1, a = b["kode"] == "E1", asal(log, b, pkg)
        for (cetak, benar), n in a.items():
            c[(b["jenis"], "angka", cetak, benar, e1)] += n
        if b["jalan_tapi_salah"]:
            c[(b["jenis"], "rbw")] += 1
            c[(b["jenis"], "rbw_tak")] += any(not cetak for cetak, _ in a)
        for q in bt["besaran"]:
            ranah = "frekuensi" if q["besaran"] in FREKUENSI else "waktu"
            c[(b["jenis"], "benar")] += q["benar"]
            c[(b["jenis"], "n")] += 1
            c[(b["jenis"], "benar_bukan_e1")] += q["benar"] and not e1
            c[(b["jenis"], ranah, "benar")] += q["benar"]
            c[(b["jenis"], ranah, "n")] += 1
    return c


def jumlah(c, jenis, syarat):
    return sum(n for k, n in c.items() if len(k) == 5 and k[0] == jenis and k[1] == "angka" and syarat(*k[2:]))


def persen(a, n):
    return f"{a}/{n} ({100 * a / n:.1f} %)" if n else "—"


def cetak(konst, per_model, uji):
    print("## 1. Constant-answer baseline (leave-one-out median)\n")
    for t, rows in konst.items():
        for j in INTI:
            k = sum(x["benar"] for r in rows if r["jenis"] == j for x in r["besaran"])
            n = sum(len(r["besaran"]) for r in rows if r["jenis"] == j)
            print(f"- {t} tolerance, {j}: {persen(k, n)}")
    print("\nAgent minus constant baseline, per-task paired permutation test (fixed tolerance rows):\n")
    for m, (j, obs, p, n) in uji:
        print(f"- {m}, {j}: {100 * obs:+.1f} points, p = {p:.4f}, n = {n} tasks")
    print("\n## 2. Provenance of non-zero numbers in FINAL (printed = seen in execution output)\n")
    print("| Model | Type | not printed / all | correct: not printed / all correct | not printed, runs not E1 "
          "| run-but-wrong runs with a number not printed |\n|---|---|---|---|---|---|")
    for m, c in per_model.items():
        for j in INTI:
            semua, tak = jumlah(c, j, lambda *_: True), jumlah(c, j, lambda p, b, e: not p)
            print(f"| {m} | {j} | {persen(tak, semua)} | {persen(jumlah(c, j, lambda p, b, e: b and not p), jumlah(c, j, lambda p, b, e: b))} "
                  f"| {persen(jumlah(c, j, lambda p, b, e: not p and not e), jumlah(c, j, lambda p, b, e: not e))} "
                  f"| {persen(c[(j, 'rbw_tak')], c[(j, 'rbw')])} |")
    print("\n## 3. Fixed 20 % tolerance: accuracy and HRV by domain\n")
    print("| Model | QT | HRV | HRV, runs not E1 | HRV HR + time | HRV frequency |\n|---|---|---|---|---|---|")
    for m, c in per_model.items():
        print(f"| {m} | {persen(c[('qt', 'benar')], c[('qt', 'n')])} | {persen(c[('hrv', 'benar')], c[('hrv', 'n')])} "
              f"| {persen(c[('hrv', 'benar_bukan_e1')], c[('hrv', 'n')])} "
              f"| {persen(c[('hrv', 'waktu', 'benar')], c[('hrv', 'waktu', 'n')])} "
              f"| {persen(c[('hrv', 'frekuensi', 'benar')], c[('hrv', 'frekuensi', 'n')])} |")


def main():
    analisis, runs = Path(sys.argv[1]), Path(sys.argv[2])
    pkg = Paket(analisis)
    from penilaian import skor, statistik
    pkg.skor = skor
    rujukan = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                               analisis / "agenekg_rujukan_hrv.json")
    data = {m: baris_run(runs / m, rujukan, pkg) for m in MODEL}
    konst = konstan(rujukan, pkg)
    rng, uji = random.Random(BENIH), []
    for m, rows in data.items():
        for j in INTI:
            a = statistik.per_tugas([bt for _, _, bt in rows if bt["jenis"] == j])
            b = statistik.per_tugas([r for r in konst["tetap"] if r["jenis"] == j])
            uji.append((m, (j, *statistik.uji_permutasi(a, b, rng))))
    cetak(konst, {m: ringkas_model(rows, pkg) for m, rows in data.items()}, uji)


if __name__ == "__main__":
    main()
