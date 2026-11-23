"""Exploratory check after panel 1 (22 Nov 2026): HRV comparisons with a fixed 20 % frequency tolerance.

The preregistered LF/HF/HF tolerance is max(20 %, 1.5 x the relative difference between the study's Welch
reference and NeuroKit2 hrv_frequency). Because the baseline calls hrv_frequency, this script rescores every
run with the widening removed (fixed 20 %), reports HRV accuracy and the paired tests against the baseline,
and counts how many records had a widened tolerance.

    python -X utf8 agenekg_hrv_toleransi_tetap.py <analysis folder> <flash runs> <dwt> <peak> <cwt>
"""
import json
import random
import sys
from pathlib import Path

BENIH = 20261107
AMBANG = 0.20
FAKTOR = 1.5
FREKUENSI = ("lf_ms2", "hf_ms2", "lf_hf")


class Paket:
    def __init__(self, folder):
        sys.path.insert(0, str(folder))
        from penilaian import skor, statistik
        self.skor, self.statistik = skor, statistik


def baris_hrv(dir_run, rujukan, pkg):
    berkas = sorted(Path(dir_run).rglob("*_u*.json")) or sorted(Path(dir_run).rglob("*.json"))
    hasil = [pkg.skor.baris_tugas_ulangan(json.loads(f.read_text(encoding="utf-8")), rujukan) for f in berkas]
    return [b for b in hasil if b["jenis"] == "hrv"]


def ringkas(nama, baris, pkg):
    k, n = pkg.statistik.proporsi(baris)
    frek = [x for b in baris for x in b["besaran"] if x["besaran"] in FREKUENSI]
    kf = sum(1 for x in frek if x["benar"])
    print(f"| {nama} | {k}/{n} ({100 * k / n:.1f} %) | {kf}/{len(frek)} ({100 * kf / len(frek):.1f} %) |")


def uji(flash, dasar, rng, pkg):
    pa, pb = pkg.statistik.per_tugas(flash), pkg.statistik.per_tugas(dasar)
    return pkg.statistik.uji_permutasi(pa, pb, rng)


def cetak_lebar(d_frek):
    lebar = {k: 0 for k in FREKUENSI}
    for per_rekaman in d_frek.values():
        for k, d in per_rekaman.items():
            lebar[k] += FAKTOR * d > AMBANG
    print(f"\nRekaman HRV: {len(d_frek)}; toleransi dilebarkan di atas 20 %: " +
          "; ".join(f"{k} {n}" for k, n in lebar.items()))


def bandingkan(label, rujukan, dirs, pkg):
    print(f"\n## {label}\n\n| Run | HRV semua besaran | HRV frekuensi |\n|---|---|---|")
    flash = baris_hrv(dirs[0], rujukan, pkg)
    ringkas("flash", flash, pkg)
    rng = random.Random(BENIH)
    for metode, d in zip(("dwt", "peak", "cwt"), dirs[1:]):
        dasar = baris_hrv(d, rujukan, pkg)
        ringkas(f"NeuroKit2 {metode}", dasar, pkg)
        obs, p, n = uji(flash, dasar, rng, pkg)
        print(f"|   flash - {metode}: {100 * obs:+.1f} poin, p = {p:.4f}, n = {n} | | |")


def main():
    analisis, dirs = Path(sys.argv[1]), sys.argv[2:6]
    pkg = Paket(analisis)
    rujukan = pkg.skor.muat_rujukan(analisis / "agenekg_rujukan.json", analisis / "agenekg_tugas.json",
                                    analisis / "agenekg_rujukan_hrv.json")
    cetak_lebar(rujukan.d_frek)
    bandingkan("Toleransi prareg (dilebarkan)", rujukan, dirs, pkg)
    tetap = pkg.skor.Rujukan(toleransi_tetap(rujukan.ruj), rujukan.tugas, {})
    bandingkan("Toleransi tetap 20 %", tetap, dirs, pkg)


def toleransi_tetap(ruj):
    """The widened frequency tolerances are stored per task in the reference file; reset them to 20 %."""
    baru = {}
    for i, r in ruj.items():
        tol = dict(r["tol"])
        for k in FREKUENSI:
            if k in tol:
                tol[k] = {"jenis": "relatif", "nilai": AMBANG}
        baru[i] = {**r, "tol": tol}
    return baru


if __name__ == "__main__":
    main()
