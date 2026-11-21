"""Ringkasan API untuk lengan eksploratif "dokumentasi API" AgenEKG (Prareg_AgenEKG.md, penyimpangan 21 Nov 2026).

Dijalankan di dalam kontainer `agenekg-py:1` agar tanda tangan dan docstring berasal dari versi pustaka yang
benar-benar terpasang (neurokit2 0.3.0, wfdb 4.3.1, scipy 1.16.3), bukan dari ingatan:

    docker run --rm --network none -v "<folder>:/out" -v "<repo>/Riset/EKG:/src:ro" agenekg-py:1 \
        python /src/agenekg_api_ringkas.py /out/agenekg_api_ringkas.txt
"""
import importlib
import inspect
import sys

FUNGSI = [
    ("wfdb", "rdrecord"),
    ("wfdb", "rdheader"),
    ("neurokit2", "ecg_clean"),
    ("neurokit2", "ecg_peaks"),
    ("neurokit2", "ecg_delineate"),
    ("neurokit2", "ecg_rate"),
    ("neurokit2", "hrv_time"),
    ("neurokit2", "hrv_frequency"),
    ("neurokit2", "intervals_to_peaks"),
    ("scipy.signal", "find_peaks"),
    ("scipy.signal", "welch"),
]
ALIAS = {"neurokit2": "nk"}
BARIS_KEMBALI = 14
ATRIBUT_RECORD = ["p_signal", "fs", "sig_name", "units", "sig_len", "n_sig"]


def ringkasan_docstring(fungsi):
    teks = inspect.getdoc(fungsi) or ""
    paragraf = teks.split("\n\n")
    ringkas = paragraf[0].replace("\n", " ").strip() if paragraf else ""
    return ringkas, bagian_kembali(teks)


def judul_bagian(baris, i):
    return i + 1 < len(baris) and baris[i].strip() and set(baris[i + 1].strip()) == {"-"}


def bagian_kembali(teks):
    baris = teks.splitlines()
    for i, isi in enumerate(baris):
        if isi.strip() == "Returns" and judul_bagian(baris, i):
            isi_bagian = []
            for j in range(i + 2, len(baris)):
                if judul_bagian(baris, j):
                    break
                if baris[j].strip():
                    isi_bagian.append(baris[j])
            return isi_bagian[:BARIS_KEMBALI]
    return []


def entri(modul, nama):
    pustaka = importlib.import_module(modul)
    fungsi = getattr(pustaka, nama, None)
    awalan = ALIAS.get(modul, modul)
    if fungsi is None:
        return None
    ringkas, kembali = ringkasan_docstring(fungsi)
    baris = [f"{awalan}.{nama}{inspect.signature(fungsi)}", f"    {ringkas}"]
    if kembali:
        baris.append("    Returns:")
        baris.extend(f"      {b.strip()}" for b in kembali)
    return "\n".join(baris)


def versi():
    nama = ["neurokit2", "wfdb", "scipy", "numpy"]
    return ", ".join(f"{n} {importlib.import_module(n).__version__}" for n in nama)


def atribut_record():
    wfdb = importlib.import_module("wfdb")
    ada = vars(wfdb.Record())
    return ", ".join(a for a in ATRIBUT_RECORD if a in ada)


def main(tujuan):
    kepala = [
        f"Installed library reference ({versi()}). `import neurokit2 as nk`.",
        "Call only functions listed here, or check a name with dir() or help() before using it.",
        f"A wfdb Record has the attributes {atribut_record()}.",
    ]
    isi = [e for e in (entri(m, n) for m, n in FUNGSI) if e]
    with open(tujuan, "w", encoding="utf-8") as f:
        f.write("\n".join(kepala) + "\n\n" + "\n\n".join(isi) + "\n")
    hilang = [f"{m}.{n}" for m, n in FUNGSI if getattr(importlib.import_module(m), n, None) is None]
    print(f"{len(isi)} fungsi ditulis; tidak ada: {hilang or '-'}")


if __name__ == "__main__":
    main(sys.argv[1])
