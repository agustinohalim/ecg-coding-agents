"""Bangkitkan 5 tugas pilot QT (Prareg_AgenEKG.md bagian 2): benih 20261107, rekaman dengan denyut
beruntun dan tanpa .q2c. Menulis agenekg_tugas_pilot.json (teks tugas + rujukan terpisah)."""
import glob, json, os, random, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import agenekg_rujukan_qt as R

def main():
    F = R.FOLDER
    q2 = {os.path.basename(p)[:-4] for p in glob.glob(os.path.join(F, "*.q2c"))}
    calon = []
    for p in sorted(glob.glob(os.path.join(F, "*.q1c"))):
        r = os.path.basename(p)[:-4]
        if r in q2:
            continue
        fs = R.wfdb.rdheader(os.path.join(F, r)).fs
        d = R.denyut_qt(r, "q1c")
        if len(d) < 5:
            continue
        s = R.ringkas(d, fs)
        if s["n_rr"] == s["n"] - 1:
            calon.append((r, fs, s))
    pilih = random.Random(20261107).sample(calon, 5)
    tugas, rujukan = [], []
    for r, fs, s in pilih:
        a, b = s["awal"] - 10, s["akhir"] + 10
        teks = (f"Record `{r}` (WFDB format: {r}.hea, {r}.dat). Use signal channel 0. Consider only the beats "
                f"whose R peak lies between sample {a} and sample {b} (inclusive, 0-based sample index). For each "
                "such beat, QT = time from QRS onset to the end of the T wave. RR = interval from the previous "
                "beat's R peak to this beat's R peak, in seconds; skip QTc for the first beat in the window. "
                "Report the mean QT in milliseconds over these beats, and the mean Bazett-corrected QTc "
                "(QT / sqrt(RR)) in milliseconds. Answer as FINAL: {\"qt_ms\": <number>, \"qtcb_ms\": <number>}.")
        tugas.append({"id": f"pilot_qt_{r}", "berkas": [f"qtdb/data/qt-database-1.0.0/{r}.hea",
                      f"qtdb/data/qt-database-1.0.0/{r}.dat"], "teks": teks})
        rujukan.append({"id": f"pilot_qt_{r}", "qt_ms": round(s["qt"], 2), "qtcb_ms": round(s["qtcb"], 2),
                        "denyut": s["n"]})
    json.dump(tugas, open("agenekg_tugas_pilot.json", "w", encoding="utf-8"), indent=1)
    json.dump(rujukan, open("agenekg_rujukan_pilot.json", "w", encoding="utf-8"), indent=1)
    print(len(calon), "calon;", [r for r, _, _ in pilih])

if __name__ == "__main__":
    main()
