"""Confirmatory QT tasks for AgenEKG (Prareg_AgenEKG_Konfirmasi.md, 22 Nov 2026).

Applies the candidate rule of `agenekg_tugas.tugas_qt` unchanged, reproduces its seeded draw of 45 tasks (checked
against `agenekg_tugas.json`), and turns every remaining candidate record into one task with the same text,
window rule, tolerance, and reference. Output (script folder): `agenekg_tugas_konfirmasi.json` (for the agent) and
`agenekg_rujukan_konfirmasi.json` (never enters the sandbox).

    python -I -X utf8 Riset/EKG/agenekg_tugas_konfirmasi.py
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agenekg_tugas as G  # noqa: E402


class Rekam(random.Random):
    """Seeded generator that keeps the population of its first sample() call."""

    def sample(self, populasi, k, **kw):
        if not hasattr(self, "calon"):
            self.calon = list(populasi)
        return super().sample(populasi, k, **kw)


def main():
    rng = Rekam(G.BENIH)
    T, _, n = G.tugas_qt(rng)
    lama = [t["id"] for t in json.load(open(os.path.join(G.SINI, "agenekg_tugas.json"), encoding="utf-8"))
            if t["id"].startswith("qt_")]
    assert [t["id"] for t in T] == lama, "seeded draw differs from the main task list"
    dipakai = {t["id"][3:] for t in T}
    tugas, rujukan = [], []
    for r, fs, best in sorted(c for c in rng.calon if c[0] not in dipakai):
        s = G.R.ringkas(best, fs)
        a, b = best[0][0] - 10, best[-1][0] + 10
        i = f"qt_{r}"
        tugas.append({"id": i, "berkas": G.berkas(G.QT_REL, r), "teks": G.TEKS_QT.format(r=r, a=a, b=b)})
        rujukan.append({"id": i, "jenis": "qt", "nilai": {"qt_ms": round(s["qt"], 2), "qtcb_ms": round(s["qtcb"], 2),
                        "qtcf_ms": round(s["qtcf"], 2)}, "tol": G.TOL_QT, "denyut": s["n"]})
    print(f"candidates {n}, main {len(T)}, confirmatory {len(tugas)}")
    for nama, isi in (("agenekg_tugas_konfirmasi.json", tugas), ("agenekg_rujukan_konfirmasi.json", rujukan)):
        with open(os.path.join(G.SINI, nama), "w", encoding="utf-8") as f:
            json.dump(isi, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
