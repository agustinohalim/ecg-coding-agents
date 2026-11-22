"""Scoring each AgenEKG task run against the references: one row per task run with every quantity, whether it
lies within the main, strict, and loose tolerance, and the E1-E8 code when the run is not fully correct."""
import json
from dataclasses import dataclass
from pathlib import Path

from .log import angka, jawaban_final, kelas_galat_pertama, pernah_jalan
from .taksonomi import kodekan

KEPEKAAN = {  # quantity -> (strict, loose); the main tolerances are in agenekg_rujukan.json
    "hr_bpm": (("mutlak", 1.0), ("mutlak", 5.0)),
    "qt_ms": (("mutlak", 10.0), ("mutlak", 40.0)),
    "qtcb_ms": (("mutlak", 10.0), ("mutlak", 40.0)),
    "qtcf_ms": (("mutlak", 10.0), ("mutlak", 40.0)),
    "sdnn_ms": (("relatif", 0.05), ("relatif", 0.20)),
    "rmssd_ms": (("relatif", 0.05), ("relatif", 0.20)),
    "sdnn_nn_ms": (("relatif", 0.05), ("relatif", 0.20)),
    "rmssd_nn_ms": (("relatif", 0.05), ("relatif", 0.20)),
    "pnn50_pct": (("mutlak", 2.0), ("mutlak", 10.0)),
    "lf_ms2": (("frek", 0.10), ("frek", 0.40)),
    "hf_ms2": (("frek", 0.10), ("frek", 0.40)),
    "lf_hf": (("frek", 0.10), ("frek", 0.40)),
}
FREKUENSI = (("lf_ms2", "lf_a", "lf_b"), ("hf_ms2", "hf_a", "hf_b"), ("lf_hf", "lfhf_a", "lfhf_b"))


@dataclass(frozen=True)
class Rujukan:
    ruj: dict
    tugas: dict
    d_frek: dict


def muat_rujukan(path_rujukan, path_tugas, path_hrv):
    ruj = {r["id"]: r for r in json.loads(Path(path_rujukan).read_text(encoding="utf-8"))}
    tugas = {t["id"]: t for t in json.loads(Path(path_tugas).read_text(encoding="utf-8"))}
    hrv = json.loads(Path(path_hrv).read_text(encoding="utf-8"))
    return Rujukan(ruj, tugas, {"hrv_" + h["rekaman"]: beda_frekuensi(h) for h in hrv})


def beda_frekuensi(h):
    """Relative difference between the two HRV implementations, which widens the frequency tolerance."""
    return {k: abs(h[ka] - h[kb]) / abs(h[kb]) for k, ka, kb in FREKUENSI if h.get(kb)}


def muat(dir_run, rujukan):
    return [baris_tugas_ulangan(json.loads(f.read_text(encoding="utf-8")), rujukan)
            for f in sorted(Path(dir_run).glob("*_u*.json"))]


def baris_tugas_ulangan(log, rujukan):
    r, t = rujukan.ruj[log["tugas"]], rujukan.tugas[log["tugas"]]
    jawab = jawaban_final(log)
    if not isinstance(jawab, dict):
        jawab = {}
    besaran = besaran_dinilai(r, jawab, rujukan.d_frek.get(r["id"], {}))
    semua_benar = all(b["benar"] for b in besaran)
    jalan = pernah_jalan(log)
    kode, sub = (None, None) if semua_benar else kodekan(log, r, t, besaran)
    return dict(tugas=log["tugas"], ulang=log["ulang"], jenis=r["jenis"], rekaman=rekaman(r),
                besaran=besaran, semua_benar=semua_benar, jalan=jalan,
                menyerah=jawab.get("unanswerable") is True,
                jalan_tapi_salah=(jalan and not semua_benar and not r["nilai"].get("unanswerable")
                                  and all(angka(jawab.get(k)) for k in r["nilai"])),
                kode=kode, subkode=sub, galat_pertama=kelas_galat_pertama(log))


def besaran_dinilai(r, jawab, d_frek_rekaman):
    if r["nilai"].get("unanswerable"):
        return [dict(besaran="unanswerable", rujukan=None, agen=None,
                     benar=jawab.get("unanswerable") is True, ketat=None, longgar=None)]
    return [nilai_besaran(k, r, jawab, d_frek_rekaman.get(k, 0.0)) for k in r["nilai"]]


def nilai_besaran(k, r, jawab, d_frek):
    ref = r["nilai"][k]
    v = jawab.get(k)
    ok = angka(v)
    e = abs(v - ref) if ok else None
    bts = lambda g=None: batas(r["tol"][k], ref, d_frek, g)
    kp = KEPEKAAN.get(k)
    return dict(besaran=k, rujukan=ref, agen=v if ok else None,
                benar=ok and e <= bts(),
                ketat=ok and kp is not None and e <= bts(kp[0]),
                longgar=ok and kp is not None and e <= bts(kp[1]))


def batas(tol, ref, d_frek=0.0, ganti=None):
    jenis, nilai = ganti if ganti else (tol["jenis"], tol["nilai"])
    if jenis == "mutlak":
        return nilai
    if jenis == "frek":
        return max(nilai, 1.5 * d_frek) * abs(ref)
    return nilai * abs(ref)


def rekaman(r):
    """Bootstrap cluster: the record a task comes from."""
    if "asal" in r:
        return r["asal"]
    return r["id"].split("_")[-1]
