"""Agreement between the recoder's codes and the automatic AgenEKG taxonomy codes.

Reads the filled-in `lembar.md` and `kunci.json` from `agenekg_kode_ulang_bahan.py`, then prints percent
agreement, Cohen's kappa, and the confusion matrix for all rows and for rows not coded E1 automatically (E1 is
checked mechanically from exit codes), followed by the list of disagreements.

Usage:
    python -X utf8 analysis/agenekg_kode_ulang_nilai.py --keluar <recoding folder>
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

KODE = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]


def baca_lembar(path):
    kode = {}
    for teks in Path(path).read_text(encoding="utf-8").splitlines():
        sel = [s.strip() for s in teks.strip().strip("|").split("|")]
        if len(sel) >= 2 and re.fullmatch(r"R\d{3}", sel[0]):
            kode[sel[0]] = sel[1].upper()
    return kode


def kappa(pasangan):
    n = len(pasangan)
    setuju = sum(a == b for a, b in pasangan) / n
    ca, cb = Counter(a for a, _ in pasangan), Counter(b for _, b in pasangan)
    harapan = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if harapan == 1 else (setuju - harapan) / (1 - harapan)


def cetak_kesepakatan(judul, pasangan):
    n = len(pasangan)
    if n == 0:
        print(f"## {judul}\n\n- Tidak ada baris.\n")
        return
    k = kappa(pasangan)
    setuju = sum(a == b for a, b in pasangan)
    print(f"## {judul}\n")
    print(f"- Baris: {n}; sepakat {setuju} ({100 * setuju / n:.1f} %); "
          f"kappa Cohen {'tak terdefinisi' if k is None else f'{k:.3f}'}\n")
    kolom = [c for c in KODE if any(c in p for p in pasangan)]
    print("| Otomatis \\ Pengguna | " + " | ".join(kolom) + " |")
    print("|---|" + "---|" * len(kolom))
    hitung = Counter(pasangan)
    for ko in kolom:
        print(f"| {ko} | " + " | ".join(str(hitung.get((ko, kp), 0)) for kp in kolom) + " |")
    print()


def nilai(folder):
    kunci = json.loads((folder / "kunci.json").read_text(encoding="utf-8"))
    pengguna = baca_lembar(folder / "lembar.md")
    kosong = [i for i in kunci if pengguna.get(i) not in KODE]
    if kosong:
        print(f"{len(kosong)} ID belum berisi kode E1–E8 yang sah: {', '.join(kosong[:20])}")
        return
    semua = [(kunci[i]["kode"], pengguna[i]) for i in kunci]
    cetak_kesepakatan("Semua baris", semua)
    cetak_kesepakatan("Di luar E1 otomatis", [p for p in semua if p[0] != "E1"])
    print("## Ketidaksepakatan\n")
    print("| ID | Model | Tugas-ulangan | Otomatis | Pengguna |")
    print("|---|---|---|---|---|")
    for i, k in kunci.items():
        if k["kode"] != pengguna[i]:
            print(f"| {i} | {k['model']} | {k['tugas']}_u{k['ulang']} | {k['kode']} {k['subkode'] or ''} | {pengguna[i]} |")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--keluar", required=True)
    nilai(Path(ap.parse_args().keluar))
