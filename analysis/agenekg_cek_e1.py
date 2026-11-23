"""Exploratory check after panel 1 (22 Nov 2026): what the FINAL answer held in runs coded E1.

E1 means no execution exited with status 0. A run can still end with numbers in FINAL; this script counts
those per model and asks whether each number was printed by any (failed) execution or appears nowhere in the
execution output. Reads the scoring package of the public repository and the unzipped main transcripts.

    python -X utf8 agenekg_cek_e1.py <analysis folder> <run folder> [<run folder> ...]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOLERANSI_RELATIF = 0.005
TOLERANSI_MUTLAK = 0.01


def isi_final(jawab, kunci, angka):
    if jawab is None:
        return "tanpa FINAL"
    if not isinstance(jawab, dict):
        return "FINAL rusak"
    if jawab.get("unanswerable") is True:
        return "menyerah"
    ada = [angka(jawab.get(k)) for k in kunci]
    if kunci and all(ada):
        return "angka lengkap"
    return "angka sebagian" if any(ada) else "tanpa angka"


def tercetak(nilai, keluaran):
    if nilai == 0:
        return False
    batas = max(TOLERANSI_RELATIF * abs(nilai), TOLERANSI_MUTLAK)
    return any(abs(float(x) - nilai) <= batas for x in re.findall(r"-?\d+(?:\.\d+)?", keluaran))


def asal_angka(nilai, keluaran):
    if all(v == 0 for v in nilai):
        return "semua nol"
    n = sum(tercetak(v, keluaran) for v in nilai)
    if n == len(nilai):
        return "semua tercetak eksekusi"
    return "sebagian tercetak" if n else "tak tercetak"


def periksa_run(log, rujukan, pkg):
    b = pkg.baris_tugas_ulangan(log, rujukan)
    if b["kode"] != "E1":
        return None
    kunci = [k for k in rujukan.ruj[log["tugas"]]["nilai"] if k != "unanswerable"]
    jawab = pkg.jawaban_final(log)
    isi = isi_final(jawab, kunci, pkg.angka)
    if isi not in ("angka lengkap", "angka sebagian"):
        return isi, None, b["jenis"]
    nilai = [float(jawab[k]) for k in kunci if pkg.angka(jawab.get(k))]
    keluaran = "\n".join((g.get("keluaran") or "") for g in pkg.eksekusi(log))
    return isi, asal_angka(nilai, keluaran), b["jenis"]


def ringkas(dir_run, rujukan, pkg):
    isi, asal, jenis = Counter(), Counter(), Counter()
    for f in sorted(Path(dir_run).rglob("*_u*.json")):
        hasil = periksa_run(json.loads(f.read_text(encoding="utf-8")), rujukan, pkg)
        if hasil is None:
            continue
        isi[hasil[0]] += 1
        if hasil[1]:
            asal[hasil[1]] += 1
            jenis[hasil[2]] += 1
    return isi, asal, jenis


def cetak(nama, isi, asal, jenis):
    print(f"\n### {nama}\n")
    print(f"- E1: {sum(isi.values())}; isi FINAL: " + "; ".join(f"{k} {n}" for k, n in isi.most_common()))
    print("- runs E1 dengan angka, asal angka: " + ("; ".join(f"{k} {n}" for k, n in asal.most_common()) or "-"))
    print("- runs E1 dengan angka, per jenis: " + ("; ".join(f"{k} {n}" for k, n in jenis.most_common()) or "-"))


class Paket:
    def __init__(self, folder):
        sys.path.insert(0, str(folder))
        from penilaian import log, skor
        self.baris_tugas_ulangan, self.muat_rujukan = skor.baris_tugas_ulangan, skor.muat_rujukan
        self.jawaban_final, self.eksekusi, self.angka = log.jawaban_final, log.eksekusi, log.angka


def main():
    analisis = Path(sys.argv[1])
    pkg = Paket(analisis)
    rujukan = pkg.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                               analisis / "agenekg_rujukan_hrv.json")
    for dir_run in sys.argv[2:]:
        cetak(Path(dir_run).name, *ringkas(dir_run, rujukan, pkg))


if __name__ == "__main__":
    main()
