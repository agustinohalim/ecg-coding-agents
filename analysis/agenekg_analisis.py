"""AgenEKG analysis (preregistration, sections 7-8): scores, record-clustered bootstrap intervals, run-but-wrong
rate, error taxonomy E1-E8 (`penilaian/taksonomi.py`), repeat agreement, tolerance sensitivity, and paired
permutation tests between models. Exploratory addition (not preregistered): the type of the first failed
execution, to see how many E1 failures start at the library interface.

Usage:
    python -X utf8 analysis/agenekg_analisis.py --run qwen7b=<run folder> [--run qwen3b=...] \
        [--json output.json] [--sampel-kode-ulang file.md]
"""
import argparse
import json
import random
from pathlib import Path

from penilaian import (cetak_galat_pertama, cetak_hasil_tugas, cetak_kesepakatan, cetak_permutasi, cetak_taksonomi,
                       cetak_toleransi, muat, muat_rujukan, ringkasan_toleransi)

DIR = Path(__file__).resolve().parent
RUJUKAN = DIR / "agenekg_rujukan.json"
TUGAS = DIR / "agenekg_tugas.json"
RUJUKAN_HRV = DIR / "agenekg_rujukan_hrv.json"
BENIH = 20261107


def main():
    a = baca_argumen()
    rujukan = muat_rujukan(a.rujukan, a.tugas, a.rujukan_hrv)
    rng = random.Random(BENIH)
    model = {nama: muat(folder, rujukan) for nama, folder in (s.split("=", 1) for s in a.run)}
    ringkasan = ringkasan_toleransi(model, rng)
    cetak_toleransi(ringkasan)
    cetak_hasil_tugas(model)
    cetak_taksonomi(model)
    cetak_galat_pertama(model)
    cetak_kesepakatan(model)
    if len(model) > 1:
        cetak_permutasi(model, rng)
    if a.json:
        tulis_json(a.json, model, ringkasan)
    if a.sampel_kode_ulang:
        tulis_sampel_kode_ulang(a.sampel_kode_ulang, model)


def baca_argumen():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", required=True, help="name=run_folder")
    ap.add_argument("--rujukan", default=str(RUJUKAN))
    ap.add_argument("--tugas", default=str(TUGAS))
    ap.add_argument("--rujukan-hrv", default=str(RUJUKAN_HRV))
    ap.add_argument("--json", default=None)
    ap.add_argument("--sampel-kode-ulang", default=None, help="write a 10 %% sample of coded failures for recoding")
    return ap.parse_args()


def tulis_json(path, model, ringkasan):
    ringkas = {f"{s['nama']}|{s['jenis']}": dict(benar=s["benar"], n=s["n"], ci=s["ci"]) for s in ringkasan}
    Path(path).write_text(json.dumps({"model": model, "ringkas": ringkas}, ensure_ascii=False, indent=1),
                          encoding="utf-8")


def tulis_sampel_kode_ulang(path, model):
    r2 = random.Random(BENIH + 1)
    baris = []
    for nama, bb in model.items():
        gagal = [b for b in bb if b["kode"]]
        for b in r2.sample(gagal, max(1, round(0.1 * len(gagal)))):
            baris.append(f"| {nama} | {b['tugas']}_u{b['ulang']} | {b['kode']} | {b['subkode'] or ''} |  |  |")
    Path(path).write_text(
        f"# Kode ulang taksonomi AgenEKG (10 % sampel acak, benih {BENIH + 1})\n\n"
        + "Isi kolom **Kode pengguna** (E1–E8) tanpa melihat kolom kode otomatis bila bisa; transkrip ada di "
          "folder run model (`<tugas>_u<ulang>.json`).\n\n"
        + "| Model | Tugas-ulangan | Kode otomatis | Subjenis | Kode pengguna | Catatan |\n|---|---|---|---|---|---|\n"
        + "\n".join(baris) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
