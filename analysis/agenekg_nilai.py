"""Nilai keluaran agen AgenEKG terhadap rujukan (toleransi Prareg_AgenEKG.md bagian 4).

Dua bentuk rujukan diterima:
- pilot (`agenekg_rujukan_pilot.json`): kunci besaran rata di tiap entri, toleransi dari TOL_PILOT;
- utama (`agenekg_rujukan.json`): `nilai` + `tol` per tugas ({"jenis": "mutlak"|"relatif", "nilai": x}).
  Tugas tak terjawab: `nilai` = {"unanswerable": true}; benar bila FINAL agen memuat "unanswerable": true.
  Pada tugas yang bisa dijawab, jawaban "unanswerable" dihitung salah untuk tiap besaran.

Keluaran: tabel per besaran (Markdown) dan, dengan --json, berkas JSON per besaran untuk analisis.

Pakai:
    python -X utf8 Riset/EKG/agenekg_nilai.py --rujukan Riset/EKG/agenekg_rujukan.json --log C:/Data/AgenEKG_runs/<nama>
"""
import argparse
import json
from pathlib import Path

TOL_PILOT = {"qt_ms": 20.0, "qtcb_ms": 20.0, "qtcf_ms": 20.0}


def baku(r):
    """Ubah entri rujukan ke bentuk (nilai, tol)."""
    if "nilai" in r:
        return r["nilai"], r["tol"]
    nilai = {k: r[k] for k in TOL_PILOT if k in r}
    return nilai, {k: {"jenis": "mutlak", "nilai": TOL_PILOT[k]} for k in nilai}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rujukan", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--json", default=None, help="tulis hasil per besaran ke berkas ini")
    a = ap.parse_args()
    ruj = {r["id"]: r for r in json.loads(Path(a.rujukan).read_text(encoding="utf-8"))}
    print("| Tugas | Ulang | Giliran | Eksekusi gagal | Besaran | Rujukan | Agen | Galat | Batas | Dalam toleransi |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    baris = []
    for f in sorted(Path(a.log).glob("*_u*.json")):
        log = json.loads(f.read_text(encoding="utf-8"))
        r = ruj[log["tugas"]]
        nilai, tol = baku(r)
        gagal = sum(1 for g in log["giliran"] if g.get("kode_keluar") not in (None, 0))
        try:
            jawab = json.loads(log["final"]) if log["final"] else {}
        except json.JSONDecodeError:
            jawab = {}
        if not isinstance(jawab, dict):
            jawab = {}
        kepala = f"| {log['tugas']} | {log['ulang']} | {len(log['giliran'])} | {gagal}"
        menyerah = jawab.get("unanswerable") is True
        if nilai.get("unanswerable"):
            ok = menyerah
            baris.append(dict(tugas=log["tugas"], ulang=log["ulang"], jenis=r.get("jenis"), besaran="unanswerable",
                              rujukan=True, agen=menyerah, galat=None, benar=ok))
            print(f"{kepala} | unanswerable | ya | {'ya' if menyerah else 'tidak'} | – | – | {'ya' if ok else 'tidak'} |")
            continue
        for k, ref in nilai.items():
            t = tol[k]
            batas = t["nilai"] if t["jenis"] == "mutlak" else t["nilai"] * abs(ref)
            v = jawab.get(k)
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                ok, e, teks_v = False, None, "menyerah" if menyerah else "tidak ada"
            else:
                e = v - ref
                ok, teks_v = abs(e) <= batas, f"{v:.4g}"
            baris.append(dict(tugas=log["tugas"], ulang=log["ulang"], jenis=r.get("jenis"), besaran=k, rujukan=ref,
                              agen=v if e is not None else None, galat=e, batas=batas, benar=ok))
            print(f"{kepala} | {k} | {ref:.4g} | {teks_v} | {'–' if e is None else f'{e:+.4g}'} | {batas:.4g} | "
                  f"{'ya' if ok else 'tidak'} |")
    benar = sum(b["benar"] for b in baris)
    print(f"\nDalam toleransi: {benar} dari {len(baris)} besaran.")
    if a.json:
        Path(a.json).write_text(json.dumps(baris, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
