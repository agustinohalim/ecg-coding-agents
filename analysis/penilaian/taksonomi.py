"""Error taxonomy E1-E8 (preregistration, section 7: one code per failed task run, the first rule that
matches, in order E1 -> E8, coded automatically from the log). The preregistration names the categories but not
how to detect them; the rules below were written on 19 November 2026, after the Qwen2.5-Coder-7B results were
known and before Qwen2.5-Coder-3B and Llama-3.1-8B were scored, and were then applied unchanged to every model.
The unit is one task run that is not fully correct.

  E1  no code execution finished with exit code 0.
  E2  no answer that can be scored: no FINAL, FINAL is not a JSON object, a requested quantity is not a
      number, or the agent declared "unanswerable" on an answerable task (subtype recorded).
  E3  sampling rate or unit. Unit: a wrong quantity whose ratio to the reference lies within 3 % of 10^3,
      10^-3, 10^6, or 10^-6. Rate: the anchor quantity (qt_ms on QT tasks, hr_bpm elsewhere) is wrong and its
      ratio lies within 3 % of the true rate divided by a plausibly assumed rate (128, 250, 360, 500,
      1000 Hz) or its inverse, **and** the executed code shows that rate: the number is assigned to a
      rate-like name (fs, sampling_rate, sample_rate, freq), or a NeuroKit2 ecg_*/hrv_* function is called
      without sampling_rate (default 1000 Hz). Rate and unit errors are exact factors, so a 3 % window is
      enough. Two looser versions were tried first on Qwen 7B and rejected before any other model was
      scored: a 10 % window on every quantity (a ratio of 0.76 from an ordinary detection error read as
      250/360) and a 3 % window on every quantity (with seven HRV quantities, one close to 0.5 or 1.95 by
      chance was enough). The code-evidence condition was added after testing the rule on DeepSeek logs
      (to test the rule only, not for any claim): a QT ratio of 1.46 appeared in code that used the header
      rate correctly.
  E4  lead or window: the executed code contains none of the window bounds from the task text (end sample,
      end + 1, or start sample when > 0), or the task names a channel and the code contains that name neither
      in quotes nor via `sig_name`. A number given for an unanswerable task is also E4 (a channel that does
      not exist, or a window beyond the record).
  E5  detection: QT wrong (wave boundaries), or HR wrong on an HRV or trap task (R detection).
  E6  ectopic trap where the agent's SDNN is closer to the SDNN of all RR than to the SDNN of NN.
  E7  library API error (AttributeError, TypeError, ImportError, ModuleNotFoundError naming wfdb or
      neurokit2) in the last execution before FINAL. Rarely reached because E1/E2 come first.
  E8  other (e.g. HRV with HR, SDNN, RMSSD right but LF/HF power wrong).
"""
import re

from .log import angka, eksekusi, jawaban_final, kode_dijalankan, pernah_jalan

LAJU_ASUMSI = [128, 250, 360, 500, 1000]
SATUAN = [1e3, 1e-3, 1e6, 1e-6]
JENDELA_E3 = 0.03
GALAT_API_TERAKHIR = re.compile(r"(AttributeError|TypeError|ImportError|ModuleNotFoundError)\b.*", re.S)


def kodekan(log, r, tugas, hasil_besaran):
    """(code, subtype) for one task run that is not fully correct."""
    salah = [h for h in hasil_besaran if not h["benar"]]
    return (kode_jawaban(log, r) or kode_satuan(salah) or kode_laju(log, r, salah)
            or kode_sadapan_jendela(log, tugas) or kode_analisis(log, r, salah))


def kode_jawaban(log, r):
    if not pernah_jalan(log):
        return "E1", None
    jawab = jawaban_final(log)
    if jawab is None:
        return "E2", "tanpa FINAL"
    if not isinstance(jawab, dict):
        return "E2", "FINAL rusak"
    if r["nilai"].get("unanswerable") is True:
        return "E4", "tak terjawab dijawab angka"
    if jawab.get("unanswerable") is True:
        return "E2", "menyerah"
    if any(not angka(jawab.get(k)) for k in r["nilai"]):
        return "E2", "besaran bukan angka"
    return None


def kode_satuan(salah):
    for h in salah:
        if h["rujukan"] and h["agen"] and dekat(h["agen"] / h["rujukan"], SATUAN):
            return "E3", "satuan " + h["besaran"]
    return None


def kode_laju(log, r, salah):
    jangkar = "qt_ms" if r["jenis"] == "qt" else "hr_bpm"
    for h in salah:
        if h["besaran"] == jangkar and h["rujukan"] and h["agen"]:
            f = laju_asli(r)
            bukti = laju_dalam_kode(kode_dijalankan(log), f)
            if bukti and dekat(h["agen"] / h["rujukan"], sorted({f / a for a in bukti} | {a / f for a in bukti})):
                return "E3", "laju"
    return None


def kode_sadapan_jendela(log, tugas):
    kode = kode_dijalankan(log)
    jd = jendela(tugas["teks"])
    if jd:
        awal, akhir = jd
        ada = lambda n: re.search(rf"(?<!\d){n}(?!\d)", kode) is not None
        if not (ada(akhir) or ada(akhir + 1) or (awal > 0 and ada(awal))):
            return "E4", "jendela"
    m = re.search(r"channel named `([^`]+)`", tugas["teks"])
    if m and not (re.search(rf"['\"]{re.escape(m.group(1))}['\"]", kode) or "sig_name" in kode):
        return "E4", "kanal"
    return None


def kode_analisis(log, r, salah):
    nama_salah = {h["besaran"] for h in salah}
    if r["jenis"] == "qt" or "hr_bpm" in nama_salah:
        return "E5", None
    if r["jenis"] == "jebakan_ektopik" and "sdnn_rr_ms" in r:
        v = jawaban_final(log).get("sdnn_nn_ms")
        if angka(v) and abs(v - r["sdnn_rr_ms"]) < abs(v - r["nilai"]["sdnn_nn_ms"]):
            return "E6", None
    eks = eksekusi(log)
    terakhir = eks[-1] if eks else {}
    keluaran = terakhir.get("keluaran") or ""
    if str(terakhir.get("kode_keluar")) != "0" and GALAT_API_TERAKHIR.search(keluaran) and re.search(
            r"wfdb|neurokit", keluaran):
        return "E7", None
    return "E8", ",".join(sorted(nama_salah))


def laju_asli(r):
    if "fs" in r:
        return r["fs"]
    return 360 if r["jenis"] == "jebakan_ektopik" else 250


def laju_dalam_kode(kode, f):
    """Rates other than f in the code, including NeuroKit2's 1000 Hz default when sampling_rate is omitted."""
    ada = set()
    for m in re.finditer(r"\b(?:fs|sampling_rate|sample_rate|sampfreq|freq|sr)\s*[=:]\s*(\d+(?:\.\d+)?)\b", kode):
        v = float(m.group(1))
        if v in LAJU_ASUMSI and v != f:
            ada.add(v)
    for m in re.finditer(r"\b(?:nk\.|neurokit2\.)?(?:ecg|hrv)_\w+\(([^()]*(?:\([^()]*\)[^()]*)*)\)", kode):
        if "sampling_rate" not in m.group(1) and f != 1000:
            ada.add(1000)
    return ada


def dekat(q, faktor):
    return any(abs(q - k) <= JENDELA_E3 * k for k in faktor)


def jendela(teks):
    m = re.search(r"between sample (\d+) and sample (\d+)", teks)
    return (int(m.group(1)), int(m.group(2))) if m else None
