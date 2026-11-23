"""Provenance and spectral-method checks requested by JIKI panel 1 (22 Nov 2026), after all results.

1. Each non-zero number in FINAL on a core task is classed, first match wins: printed (as in Hasil 16, within
   0.5 % or 0.01 of a number in the execution output the agent saw); unit (printed in seconds or milliseconds the
   other way round, or QT in samples at 250 Hz); derived (QTcB or QTcF from the agent's own QT answer and an RR,
   NN, or heart rate printed in the output; heart rate as 60000 / a printed NN in ms; LF/HF as the ratio of the
   agent's own LF and HF answers); or none. Control: the same rules against the output of another run of the
   same model and task type drawn at random, which estimates chance matches.
2. Audit sample: 30 DeepSeek QT numbers of class "none", seed 20261122, written with the end of the output the
   agent saw to <out>/audit_asal.md for reading.
3. Spectral method in the DeepSeek HRV code (last execution naming one): NeuroKit2 hrv/hrv_frequency, Welch,
   Lomb-Scargle, FFT/periodogram, or none; frequency-domain quantities within the fixed 20 % tolerance by method.

    python -X utf8 agenekg_asal_ulang.py <analysis folder> <runs folder> <out folder>
"""
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from agenekg_tambahan_jiki import BENIH, FREKUENSI, Paket, baris_run, persen

MODEL = ("main_llama31_8b", "main_deepseek-v4-flash")
METODE = (("neurokit2", r"hrv_frequency|nk\.hrv\(|neurokit2\.hrv\("), ("welch", r"welch"),
          ("lomb-scargle", r"lomb|LombScargle"), ("fft/periodogram", r"periodogram|np\.fft|scipy\.fft|rfft"))


def kelas(nilai, besaran, jawab, keluaran):
    """Provenance class of one non-zero number given the agent's own answers and the output it saw."""
    angka = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", keluaran)]
    dekat = lambda a, b: abs(a - b) <= max(0.005 * abs(b), 0.01)
    if any(dekat(x, nilai) for x in angka):
        return "printed"
    if any(dekat(x * s, nilai) for x in angka for s in (1000, 0.001, 4.0)):
        return "unit"
    rr = [x for x in angka if 0.3 <= x <= 2.0] + [x / 1000 for x in angka if 300 <= x <= 2000] + \
         [60 / x for x in angka if 30 <= x <= 200]
    qt = jawab.get("qt_ms")
    if besaran == "qtcb_ms" and isinstance(qt, (int, float)) and any(dekat(qt / r ** 0.5, nilai) for r in rr):
        return "derived"
    if besaran == "qtcf_ms" and isinstance(qt, (int, float)) and any(dekat(qt / r ** (1 / 3), nilai) for r in rr):
        return "derived"
    if besaran.startswith("hr") and any(dekat(60000 / x, nilai) for x in angka if 300 <= x <= 2000):
        return "derived"
    lf, hf = jawab.get("lf_ms2"), jawab.get("hf_ms2")
    if besaran == "lf_hf" and isinstance(lf, (int, float)) and isinstance(hf, (int, float)) and hf and dekat(lf / hf, nilai):
        return "derived"
    return "none"


def nomor(log, baris, pkg):
    """(quantity, value, correct, answers, output) for every non-zero numeric answer of one run."""
    jawab = pkg.jawaban_final(log)
    jawab = jawab if isinstance(jawab, dict) else {}
    keluaran = "\n".join((g.get("keluaran") or "") for g in pkg.eksekusi(log))
    return [(x["besaran"], float(x["agen"]), x["benar"], jawab, keluaran) for x in baris["besaran"]
            if isinstance(x["agen"], (int, float)) and x["agen"] != 0]


def provenans(rows, pkg, rng):
    """Counters of (type, class, correct) for the runs and for the random-run control, and the 'none' QT list."""
    nyata, kontrol, tanpa = Counter(), Counter(), []
    per_jenis = defaultdict(list)
    for log, b, _ in rows:
        per_jenis[b["jenis"]].append(log)
    for log, b, _ in rows:
        lain = rng.choice([x for x in per_jenis[b["jenis"]] if x is not log])
        keluaran_lain = "\n".join((g.get("keluaran") or "") for g in pkg.eksekusi(lain))
        for q, v, benar, jawab, keluaran in nomor(log, b, pkg):
            k = kelas(v, q, jawab, keluaran)
            nyata[(b["jenis"], k, benar)] += 1
            kontrol[(b["jenis"], kelas(v, q, jawab, keluaran_lain), benar)] += 1
            if k == "none" and b["jenis"] == "qt":
                tanpa.append((log, q, v, benar))
    return nyata, kontrol, tanpa


def metode(kode_per_giliran):
    """Spectral method named in the last execution that names one."""
    for kode in reversed(kode_per_giliran):
        for nama, pola in METODE:
            if re.search(pola, kode):
                return nama
    return "none found"


def spektral(rows, pkg):
    """Counter of (method, 'runs' | 'correct' | 'n') for frequency-domain quantities, fixed 20 % tolerance."""
    c = Counter()
    for log, b, bt in rows:
        if b["jenis"] != "hrv":
            continue
        kode = [re.search(r"```(?:python)?\s*\n(.*?)```", g.get("model") or "", re.S) for g in pkg.eksekusi(log)]
        m = metode([k.group(1) for k in kode if k])
        c[(m, "runs")] += 1
        for x in bt["besaran"]:
            if x["besaran"] in FREKUENSI:
                c[(m, "correct")] += x["benar"]
                c[(m, "n")] += 1
    return c


def tulis_audit(tanpa, rujukan, out, rng):
    """Writes 30 sampled 'none' QT numbers with the task text, answer, reference, and output tail."""
    teks = ["# Audit sample: DeepSeek QT numbers with no provenance match\n"]
    for i, (log, q, v, benar) in enumerate(rng.sample(tanpa, min(30, len(tanpa))), 1):
        ref = rujukan.ruj[log["tugas"]]["nilai"][q]
        keluaran = "\n".join((g.get("keluaran") or "") for g in log["giliran"] if g.get("keluaran"))
        teks.append(f"## A{i}. {log['tugas']} u{log['ulang']} {q} = {v} (ref {ref}; {'correct' if benar else 'wrong'})\n")
        teks.append(f"FINAL: {log.get('final')}\n\nLast reply (end):\n```\n{(log['giliran'][-1].get('model') or '')[-1500:]}\n```\n")
        teks.append(f"Output seen (end):\n```\n{keluaran[-2500:]}\n```\n")
    Path(out).mkdir(parents=True, exist_ok=True)
    (Path(out) / "audit_asal.md").write_text("\n".join(teks), encoding="utf-8")


def main():
    analisis, runs, out = (Path(a) for a in sys.argv[1:4])
    pkg = Paket(analisis)
    from penilaian import skor
    pkg.skor = skor
    rujukan = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                               analisis / "agenekg_rujukan_hrv.json")
    rng = random.Random(BENIH)
    for m in MODEL:
        rows = baris_run(runs / m, rujukan, pkg)
        nyata, kontrol, tanpa = provenans(rows, pkg, rng)
        print(f"## {m}\n\n| Type | Class | Numbers | Correct | Control (random other run) |\n|---|---|---|---|---|")
        for j in ("qt", "hrv"):
            semua = sum(n for k, n in nyata.items() if k[0] == j)
            for kl in ("printed", "unit", "derived", "none"):
                n = nyata[(j, kl, True)] + nyata[(j, kl, False)]
                print(f"| {j} | {kl} | {persen(n, semua)} | {persen(nyata[(j, kl, True)], n)} "
                      f"| {persen(kontrol[(j, kl, True)] + kontrol[(j, kl, False)], semua)} |")
        if m == "main_deepseek-v4-flash":
            tulis_audit(tanpa, rujukan, out, rng)
            c = spektral(rows, pkg)
            print("\nSpectral method in HRV code (fixed 20 % tolerance, LF, HF, LF/HF):\n")
            for nama in [n for n, _ in METODE] + ["none found"]:
                print(f"- {nama}: {c[(nama, 'runs')]} runs; frequency quantities correct {persen(c[(nama, 'correct')], c[(nama, 'n')])}")
        print()


if __name__ == "__main__":
    main()
