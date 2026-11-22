"""Reading AgenEKG agent transcripts (`<task>_u<repeat>.json` written by `agenekg_agen.py`)."""
import json
import math
import re

GALAT_API = ("AttributeError", "TypeError", "ImportError", "ModuleNotFoundError")


def angka(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def jawaban_final(log):
    """The FINAL object, None without a FINAL line, or "rusak" when FINAL is not valid JSON."""
    try:
        return json.loads(log["final"]) if log.get("final") else None
    except json.JSONDecodeError:
        return "rusak"


def eksekusi(log):
    return [g for g in log["giliran"] if g.get("kode_keluar") not in (None, "", "None")]


def pernah_jalan(log):
    return any(str(g.get("kode_keluar")) == "0" for g in eksekusi(log))


def kode_dijalankan(log):
    teks = []
    for g in eksekusi(log):
        m = re.search(r"```(?:python)?\s*\n(.*?)```", g.get("model") or "", re.S)
        teks.append(m.group(1) if m else (g.get("model") or ""))
    return "\n".join(teks)


def galat_pertama(log):
    for g in eksekusi(log):
        if str(g.get("kode_keluar")) not in ("0",):
            k = g.get("keluaran") or ""
            m = re.findall(r"^(\w+(?:Error|Exception|Interrupt))\b[^\n]*", k, re.M)
            if "[timeout" in k:
                return "timeout", k
            return (m[-1] if m else "lain"), k
    return None, ""


def kelas_galat_pertama(log):
    nama, keluaran = galat_pertama(log)
    if nama is None:
        return None
    if nama in GALAT_API and re.search(r"wfdb|neurokit|\bnk\.", keluaran):
        return "API pustaka (" + nama + ")"
    return nama
