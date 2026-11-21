"""Bahan kode ulang taksonomi AgenEKG secara tersamar.

Sampel 145 tugas-ulangan ditarik oleh `agenekg_analisis.py --sampel-kode-ulang` (benih 20261108) dan tidak
ditarik ulang di sini. Skrip ini menulis tiga berkas ke folder keluaran:

  lembar.md   ID acak R001-R145, kolom Kode pengguna dan Catatan; tanpa model dan tanpa kode otomatis
  bahan.md    per ID: teks tugas, rujukan dan toleransi, FINAL, kode keluar tiap giliran, kode yang dijalankan
  kunci.json  ID -> model, tugas-ulangan, kode otomatis (jangan dibuka sebelum lembar selesai)

Kesepakatan dihitung sesudahnya oleh `agenekg_kode_ulang_nilai.py`.

Pakai:
    python -X utf8 Riset/EKG/agenekg_kode_ulang_bahan.py --sampel C:/Data/AgenEKG_runs/sampel_kode_ulang.md \
        --keluar C:/Data/AgenEKG_runs/kode_ulang
"""
import argparse
import json
import random
import re
from pathlib import Path

import agenekg_analisis as an

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
    """Format tabel mengikuti yang ditulis agenekg_analisis.py."""
    baris = []
    for teks in Path(path).read_text(encoding="utf-8").splitlines():
        sel = [s.strip() for s in teks.strip().strip("|").split("|")]
        if len(sel) >= 3 and sel[0] in FOLDER_RUN:
            tugas, ulang = sel[1].rsplit("_u", 1)
            baris.append((sel[0], tugas, int(ulang)))
    return baris


def muat_rujukan():
    ruj = {r["id"]: r for r in json.loads((an.DIR / "agenekg_rujukan.json").read_text(encoding="utf-8"))}
    tugas = {t["id"]: t for t in json.loads((an.DIR / "agenekg_tugas.json").read_text(encoding="utf-8"))}
    d_frek = {}
    for h in json.loads((an.DIR / "agenekg_rujukan_hrv.json").read_text(encoding="utf-8")):
        d = {}
        for k, ka, kb in (("lf_ms2", "lf_a", "lf_b"), ("hf_ms2", "hf_a", "hf_b"), ("lf_hf", "lfhf_a", "lfhf_b")):
            if h.get(kb):
                d[k] = abs(h[ka] - h[kb]) / abs(h[kb])
        d_frek["hrv_" + h["rekaman"]] = d
    return ruj, tugas, d_frek


def muat_model(dir_run, sampel, ruj, tugas, d_frek):
    hasil = {}
    for model in sorted({m for m, _, _ in sampel}):
        for b in an.muat(Path(dir_run) / FOLDER_RUN[model], ruj, tugas, d_frek):
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


def bagian_bahan(id_acak, log, r, t, baris):
    final = (log.get("final") or "").replace("`", "'")
    return "\n".join([
        f"## {id_acak}\n",
        f"Jenis: {r['jenis']} · laju rekaman {an.laju_asli(r)} Hz\n",
        "> " + t["teks"].replace("\n", "\n> ") + "\n",
        tabel_besaran(baris, r),
        f"FINAL: `{final}`\n" if final else "FINAL: tidak ada\n",
        tabel_giliran(log),
        kode_per_giliran(log),
    ])


def tulis(a):
    sampel = baca_sampel(a.sampel)
    ruj, tugas, d_frek = muat_rujukan()
    baris_model = muat_model(a.runs, sampel, ruj, tugas, d_frek)
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
        bahan.append(bagian_bahan(id_acak, log, ruj[id_tugas], tugas[id_tugas], b))
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
