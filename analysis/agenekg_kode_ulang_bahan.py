"""Blinded material for recoding the AgenEKG taxonomy.

The 145-run sample is drawn by `agenekg_analisis.py --sampel-kode-ulang` (seed 20261108) and is not redrawn
here. The script writes three files to the output folder:

  lembar.md   random IDs R001-R145 with columns for the code and a note; no model and no automatic code
  bahan.md    per ID: task text, references and tolerances, FINAL, exit code of each turn, executed code
  kunci.json  ID -> model, task run, automatic code (not to be opened before the sheet is complete)

Agreement is computed afterwards by `agenekg_kode_ulang_nilai.py`. The Markdown text stays in Indonesian.

Usage:
    python -X utf8 analysis/agenekg_kode_ulang_bahan.py --sampel <sampel_kode_ulang.md> --keluar <folder>
"""
import argparse
import json
import random
import re
from pathlib import Path

import agenekg_analisis as an
from penilaian import laju_asli, muat, muat_rujukan

FOLDER_RUN = {
    "qwen7b": "utama_qwen25coder7b",
    "qwen3b": "utama_qwen25coder3b",
    "llama8b": "utama_llama31_8b",
}
BENIH_URUT = an.BENIH + 2
BARIS_KELUARAN = 4

PETUNJUK = """# Bahan kode ulang AgenEKG

Isi `lembar.md`, satu kode per ID. Tetapkan kode pertama yang cocok, diperiksa berurutan dari E1 sampai E8.
Pakai penilaian Anda atas definisi di bawah; tidak perlu menghitung ulang aturan regex skrip.

| Kode | Kategori | Definisi |
|---|---|---|
| E1 | Kode tidak pernah jalan | Tidak ada satu pun eksekusi yang selesai dengan kode keluar 0 |
| E2 | Tidak ada jawaban yang bisa dinilai | Tanpa FINAL, FINAL bukan objek JSON, besaran yang diminta bukan angka, atau "unanswerable" pada tugas yang bisa dijawab |
| E3 | Laju sampel atau satuan | Nilai salah karena faktor 10^±3 / 10^±6, atau karena laju sampel yang diasumsikan berbeda dari laju rekaman (laju itu tampak di kode) |
| E4 | Sadapan atau jendela | Kode tidak memakai jendela sampel atau kanal bernama dari teks tugas; atau tugas tak terjawab dijawab dengan angka |
| E5 | Deteksi | QT salah (batas gelombang), atau HR salah pada tugas HRV/jebakan (deteksi R) |
| E6 | RR dipakai sebagai NN | Jebakan ektopik: SDNN agen lebih dekat ke SDNN semua RR daripada ke SDNN NN |
| E7 | API pustaka | Eksekusi terakhir sebelum FINAL gagal dengan AttributeError/TypeError/ImportError/ModuleNotFoundError dari wfdb atau neurokit2 |
| E8 | Lainnya | Tidak satu pun di atas, mis. HR, SDNN, RMSSD benar tetapi LF/HF salah |

Setiap ID di bawah ini tidak seluruhnya benar. Kolom "Dalam toleransi" dihitung oleh penilai.
"""


def baca_sampel(path):
    """Reads the table written by agenekg_analisis.py --sampel-kode-ulang."""
    baris = []
    for teks in Path(path).read_text(encoding="utf-8").splitlines():
        sel = [s.strip() for s in teks.strip().strip("|").split("|")]
        if len(sel) >= 3 and sel[0] in FOLDER_RUN:
            tugas, ulang = sel[1].rsplit("_u", 1)
            baris.append((sel[0], tugas, int(ulang)))
    return baris


def muat_model(dir_run, sampel, rujukan):
    hasil = {}
    for model in sorted({m for m, _, _ in sampel}):
        for b in muat(Path(dir_run) / FOLDER_RUN[model], rujukan):
            hasil[(model, b["tugas"], b["ulang"])] = b
    return hasil


def tabel_besaran(baris, r):
    if r["nilai"].get("unanswerable"):
        return "Tugas ini **tidak bisa dijawab** dari berkasnya (jawaban benar: unanswerable).\n"
    teks = ["| Besaran | Rujukan | Toleransi | Agen | Dalam toleransi |", "|---|---|---|---|---|"]
    for h in baris["besaran"]:
        tol = r["tol"][h["besaran"]]
        persen = tol["jenis"] in ("relatif", "frek")
        nilai_tol = f"{100 * tol['nilai']:g} %" if persen else f"{tol['nilai']:g}"
        agen = "–" if h["agen"] is None else f"{h['agen']:.6g}"
        teks.append(f"| {h['besaran']} | {h['rujukan']:.6g} | ±{nilai_tol} | {agen} | "
                    f"{'ya' if h['benar'] else 'tidak'} |")
    if "sdnn_rr_ms" in r:
        teks.append(f"\nSDNN semua RR (termasuk ektopik): {r['sdnn_rr_ms']:.6g} ms.")
    return "\n".join(teks) + "\n"


def tabel_giliran(log):
    teks = ["| Giliran | Kode keluar | Baris terakhir keluaran |", "|---|---|---|"]
    for i, g in enumerate(log["giliran"], 1):
        keluar = g.get("kode_keluar")
        if keluar in (None, "", "None"):
            teks.append(f"| {i} | tanpa eksekusi | |")
            continue
        baris = [b.strip()[:160] for b in (g.get("keluaran") or "").splitlines() if b.strip()]
        ekor = " ⏎ ".join(baris[-BARIS_KELUARAN:]).replace("|", "\\|").replace("`", "'")
        teks.append(f"| {i} | {keluar} | `{ekor}` |")
    return "\n".join(teks) + "\n"


def kode_per_giliran(log):
    bagian = []
    for i, g in enumerate(log["giliran"], 1):
        if g.get("kode_keluar") in (None, "", "None"):
            continue
        m = re.search(r"```(?:python)?\s*\n(.*?)```", g.get("model") or "", re.S)
        kode = (m.group(1) if m else g.get("model") or "").rstrip()
        bagian.append(f"<details><summary>Kode giliran {i} (keluar {g.get('kode_keluar')})</summary>\n\n"
                      f"```python\n{kode}\n```\n\n</details>\n")
    return "\n".join(bagian)


def bagian_bahan(id_acak, log, baris, rujukan):
    r, t = rujukan.ruj[baris["tugas"]], rujukan.tugas[baris["tugas"]]
    final = (log.get("final") or "").replace("`", "'")
    return "\n".join([
        f"## {id_acak}\n",
        f"Jenis: {r['jenis']} · laju rekaman {laju_asli(r)} Hz\n",
        "> " + t["teks"].replace("\n", "\n> ") + "\n",
        tabel_besaran(baris, r),
        f"FINAL: `{final}`\n" if final else "FINAL: tidak ada\n",
        tabel_giliran(log),
        kode_per_giliran(log),
    ])


def tulis(a):
    sampel = baca_sampel(a.sampel)
    rujukan = muat_rujukan(an.RUJUKAN, an.TUGAS, an.RUJUKAN_HRV)
    baris_model = muat_model(a.runs, sampel, rujukan)
    urut = sampel[:]
    random.Random(BENIH_URUT).shuffle(urut)
    keluar = Path(a.keluar)
    keluar.mkdir(parents=True, exist_ok=True)
    kunci, bahan, lembar = {}, [PETUNJUK], ["| ID | Kode pengguna | Catatan |", "|---|---|---|"]
    for i, (model, id_tugas, ulang) in enumerate(urut, 1):
        id_acak = f"R{i:03d}"
        b = baris_model[(model, id_tugas, ulang)]
        log = json.loads((Path(a.runs) / FOLDER_RUN[model] / f"{id_tugas}_u{ulang}.json").read_text(encoding="utf-8"))
        kunci[id_acak] = dict(model=model, tugas=id_tugas, ulang=ulang, kode=b["kode"], subkode=b["subkode"])
        bahan.append(bagian_bahan(id_acak, log, b, rujukan))
        lembar.append(f"| {id_acak} |  |  |")
    (keluar / "kunci.json").write_text(json.dumps(kunci, ensure_ascii=False, indent=1), encoding="utf-8")
    (keluar / "bahan.md").write_text("\n".join(bahan), encoding="utf-8")
    (keluar / "lembar.md").write_text(
        f"# Lembar kode ulang AgenEKG ({len(urut)} ID, urutan acak benih {BENIH_URUT})\n\n"
        "Isi satu kode E1–E8 per baris dari `bahan.md`. Jangan buka `kunci.json` sebelum selesai.\n\n"
        + "\n".join(lembar) + "\n", encoding="utf-8")
    print(f"{len(urut)} ID ditulis ke {keluar}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sampel", required=True)
    ap.add_argument("--runs", default="C:/Data/AgenEKG_runs")
    ap.add_argument("--keluar", required=True)
    tulis(ap.parse_args())
