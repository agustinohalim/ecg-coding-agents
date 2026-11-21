"""Analisis AgenEKG menurut Prareg_AgenEKG.md bagian 7-8: skor, CI bootstrap bergugus rekaman, laju
jalan-tapi-salah, taksonomi galat E1-E8, kesepakatan antar-ulangan, kepekaan toleransi, dan uji permutasi
berpasangan antar-model.

Aturan taksonomi (bagian 7: "satu galat = satu kode pertama yang cocok, urutan E1 -> E8; dikode otomatis dari
log"). Pra-daftar menamai kategorinya, tidak merinci cara mendeteksinya; rincian di bawah ditulis 19 Nov 2026
sesudah hasil Qwen2.5-Coder-7B diketahui dan sebelum hasil Qwen2.5-Coder-3B dan Llama-3.1-8B dinilai, lalu
dipakai tanpa diubah untuk ketiganya. Satuan = satu tugas-ulangan yang tidak seluruhnya benar.

  E1  tidak ada satu pun eksekusi kode yang selesai dengan kode keluar 0.
  E2  tidak ada jawaban yang bisa dinilai: tanpa FINAL, FINAL bukan objek JSON, besaran yang diminta bukan
      angka, atau agen menyatakan "unanswerable" pada tugas yang bisa dijawab (subjenis dicatat).
  E3  laju sampel atau satuan. Satuan: ada besaran salah yang rasionya terhadap rujukan dalam 3 % dari 10^3,
      10^-3, 10^6, atau 10^-6. Laju: besaran jangkar (qt_ms pada tugas QT, hr_bpm pada tugas lain) salah dan
      rasionya dalam 3 % dari laju sebenarnya dibagi laju yang mungkin diasumsikan (128, 250, 360, 500,
      1000 Hz) atau kebalikannya, **dan** kode yang dijalankan memuat bukti laju itu: angka laju tersebut
      ditetapkan ke nama mirip laju (fs, sampling_rate, sample_rate, freq), atau fungsi NeuroKit2 ecg_*/hrv_*
      dipanggil tanpa sampling_rate (bawaannya 1000 Hz). Galat laju dan satuan berupa perkalian persis, jadi
      jendela 3 % cukup.
      Dua versi lebih longgar dicoba lebih dulu pada Qwen 7B dan ditolak sebelum model lain dinilai: jendela
      10 % pada semua besaran (rasio 0,76 dari galat deteksi biasa terbaca sebagai 250/360) dan jendela 3 %
      pada semua besaran (dengan tujuh besaran HRV, satu yang kebetulan dekat 0,5 atau 1,95 sudah cukup).
      Syarat bukti kode ditambahkan sesudah uji aturan pada log DeepSeek (hanya untuk menguji aturan, bukan
      untuk klaim): rasio QT 1,46 muncul pada kode yang memakai laju header dengan benar.
  E4  sadapan atau jendela: kode yang dijalankan tidak memuat batas jendela dari teks tugas (sampel akhir atau
      akhir+1, atau sampel awal bila > 0), atau tugas menyebut kanal bernama dan kode tidak memuat nama itu
      dalam tanda kutip maupun `sig_name`. Tugas tak terjawab yang dijawab dengan angka juga E4 (kanal yang
      tidak ada atau jendela di luar rekaman).
  E5  deteksi: QT salah (batas gelombang), atau HR salah pada tugas HRV/jebakan (deteksi R).
  E6  jebakan ektopik dengan SDNN agen lebih dekat ke SDNN semua RR daripada ke SDNN NN.
  E7  galat API pustaka (AttributeError, TypeError, ImportError, ModuleNotFoundError yang menyebut wfdb atau
      neurokit2) pada eksekusi terakhir sebelum FINAL. Jarang tercapai karena E1/E2 mendahului.
  E8  lainnya (mis. HRV dengan HR, SDNN, RMSSD benar tetapi daya LF/HF salah).

Tambahan eksploratif (tidak dipra-daftarkan): jenis galat eksekusi pertama yang gagal, untuk melihat berapa
kegagalan E1 yang berawal dari API pustaka.

Pakai:
    python -X utf8 Riset/EKG/agenekg_analisis.py --run qwen7b=C:/Data/AgenEKG_runs/utama_qwen25coder7b \
        [--run qwen3b=...] [--json keluar.json] [--sampel-kode-ulang berkas.md]
"""
import argparse
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent
B_BOOT = 2000
B_PERM = 10000
BENIH = 20261107
JENIS_URUT = ["qt", "hrv", "jebakan_ektopik", "jebakan_laju", "jebakan_kanal", "jebakan_takterjawab"]
INTI = ["qt", "hrv"]
LAJU_ASUMSI = [128, 250, 360, 500, 1000]
SATUAN = [1e3, 1e-3, 1e6, 1e-6]
JENDELA_E3 = 0.03


def laju_asli(r):
    if "fs" in r:
        return r["fs"]
    return 360 if r["jenis"] == "jebakan_ektopik" else 250


def laju_dalam_kode(kode, f):
    """Laju selain f yang tampak dipakai di kode: angka literal ke nama mirip laju, atau 1000 Hz bawaan
    NeuroKit2 bila fungsi ecg_*/hrv_* dipanggil tanpa sampling_rate."""
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
KEPEKAAN = {  # besaran -> (ketat, longgar); toleransi utama ada di agenekg_rujukan.json
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
API_GALAT = re.compile(r"(AttributeError|TypeError|ImportError|ModuleNotFoundError)\b.*", re.S)


def rekaman(r):
    """Gugus bootstrap: rekaman asal tugas."""
    if "asal" in r:
        return r["asal"]
    return r["id"].split("_")[-1]


def batas(tol, ref, d_frek=0.0, ganti=None):
    jenis, nilai = ganti if ganti else (tol["jenis"], tol["nilai"])
    if jenis == "mutlak":
        return nilai
    if jenis == "frek":
        return max(nilai, 1.5 * d_frek) * abs(ref)
    return nilai * abs(ref)


def angka(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def eksekusi(log):
    return [g for g in log["giliran"] if g.get("kode_keluar") not in (None, "", "None")]


def kode_dijalankan(log):
    teks = []
    for g in eksekusi(log):
        m = re.search(r"```(?:python)?\s*\n(.*?)```", g.get("model") or "", re.S)
        teks.append(m.group(1) if m else (g.get("model") or ""))
    return "\n".join(teks)


def jendela(teks):
    m = re.search(r"between sample (\d+) and sample (\d+)", teks)
    return (int(m.group(1)), int(m.group(2))) if m else None


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
    if nama in ("AttributeError", "TypeError", "ImportError", "ModuleNotFoundError") and re.search(
            r"wfdb|neurokit|\bnk\.", keluaran):
        return "API pustaka (" + nama + ")"
    return nama


def kodekan(log, r, tugas, hasil_besaran, d_frek):
    """Kode E1-E8 untuk satu tugas-ulangan yang tidak seluruhnya benar."""
    eks = eksekusi(log)
    if not any(str(g.get("kode_keluar")) == "0" for g in eks):
        return "E1", None
    try:
        jawab = json.loads(log["final"]) if log.get("final") else None
    except json.JSONDecodeError:
        jawab = "rusak"
    takterjawab = r["nilai"].get("unanswerable") is True
    if jawab is None:
        return "E2", "tanpa FINAL"
    if not isinstance(jawab, dict):
        return "E2", "FINAL rusak"
    if takterjawab:
        return "E4", "tak terjawab dijawab angka"
    if jawab.get("unanswerable") is True:
        return "E2", "menyerah"
    if any(not angka(jawab.get(k)) for k in r["nilai"]):
        return "E2", "besaran bukan angka"
    salah = [h for h in hasil_besaran if not h["benar"]]
    for h in salah:
        if h["rujukan"] and h["agen"] and dekat(h["agen"] / h["rujukan"], SATUAN):
            return "E3", "satuan " + h["besaran"]
    jangkar = "qt_ms" if r["jenis"] == "qt" else "hr_bpm"
    for h in salah:
        if h["besaran"] == jangkar and h["rujukan"] and h["agen"]:
            f = laju_asli(r)
            bukti = laju_dalam_kode(kode_dijalankan(log), f)
            if bukti and dekat(h["agen"] / h["rujukan"], sorted({f / a for a in bukti} | {a / f for a in bukti})):
                return "E3", "laju"
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
    nama_salah = {h["besaran"] for h in salah}
    if r["jenis"] == "qt" or "hr_bpm" in nama_salah:
        return "E5", None
    if r["jenis"] == "jebakan_ektopik" and "sdnn_rr_ms" in r:
        v = jawab.get("sdnn_nn_ms")
        if angka(v) and abs(v - r["sdnn_rr_ms"]) < abs(v - r["nilai"]["sdnn_nn_ms"]):
            return "E6", None
    terakhir = eks[-1] if eks else {}
    if str(terakhir.get("kode_keluar")) != "0" and API_GALAT.search(terakhir.get("keluaran") or "") and re.search(
            r"wfdb|neurokit", terakhir.get("keluaran") or ""):
        return "E7", None
    return "E8", ",".join(sorted(nama_salah))


def muat(dir_run, ruj, tugas, d_frek):
    """Satu baris per tugas-ulangan: besaran, kebenaran, kode galat."""
    out = []
    for f in sorted(Path(dir_run).glob("*_u*.json")):
        log = json.loads(f.read_text(encoding="utf-8"))
        r, t = ruj[log["tugas"]], tugas[log["tugas"]]
        try:
            jawab = json.loads(log["final"]) if log.get("final") else {}
        except json.JSONDecodeError:
            jawab = {}
        if not isinstance(jawab, dict):
            jawab = {}
        besaran = []
        if r["nilai"].get("unanswerable"):
            besaran.append(dict(besaran="unanswerable", rujukan=None, agen=None,
                                benar=jawab.get("unanswerable") is True, ketat=None, longgar=None))
        else:
            for k, ref in r["nilai"].items():
                v = jawab.get(k)
                ok = angka(v)
                e = abs(v - ref) if ok else None
                df = d_frek.get(r["id"], {}).get(k, 0.0)
                bts = lambda g=None: batas(r["tol"][k], ref, df, g)
                kp = KEPEKAAN.get(k)
                besaran.append(dict(
                    besaran=k, rujukan=ref, agen=v if ok else None,
                    benar=ok and e <= bts(),
                    ketat=ok and kp is not None and e <= bts(kp[0]),
                    longgar=ok and kp is not None and e <= bts(kp[1])))
        semua_benar = all(b["benar"] for b in besaran)
        jalan = any(str(g.get("kode_keluar")) == "0" for g in eksekusi(log))
        kode, sub = (None, None) if semua_benar else kodekan(log, r, t, besaran, d_frek)
        out.append(dict(tugas=log["tugas"], ulang=log["ulang"], jenis=r["jenis"], rekaman=rekaman(r),
                        besaran=besaran, semua_benar=semua_benar, jalan=jalan,
                        menyerah=jawab.get("unanswerable") is True,
                        jalan_tapi_salah=(jalan and not semua_benar and not r["nilai"].get("unanswerable")
                                          and all(angka(jawab.get(k)) for k in r["nilai"])),
                        kode=kode, subkode=sub, galat_pertama=kelas_galat_pertama(log)))
    return out


def proporsi(baris, kunci="benar"):
    n = sum(len(b["besaran"]) for b in baris)
    k = sum(sum(1 for x in b["besaran"] if x[kunci]) for b in baris)
    return k, n


def ci_bootstrap(baris, kunci="benar", rng=None):
    """CI 95 % persentil, rekaman diambil ulang dengan pengembalian."""
    per = defaultdict(lambda: [0, 0])
    for b in baris:
        for x in b["besaran"]:
            per[b["rekaman"]][0] += bool(x[kunci])
            per[b["rekaman"]][1] += 1
    gugus = list(per.values())
    if not gugus:
        return None
    nilai = []
    for _ in range(B_BOOT):
        s = [gugus[rng.randrange(len(gugus))] for _ in gugus]
        nilai.append(sum(a for a, _ in s) / sum(n for _, n in s))
    nilai.sort()
    return nilai[int(0.025 * B_BOOT)], nilai[int(0.975 * B_BOOT) - 1]


def per_tugas(baris):
    per = defaultdict(lambda: [0, 0])
    for b in baris:
        for x in b["besaran"]:
            per[b["tugas"]][0] += bool(x["benar"])
            per[b["tugas"]][1] += 1
    return {t: a / n for t, (a, n) in per.items()}


def uji_permutasi(a, b, rng):
    """Uji permutasi berpasangan (tukar tanda per tugas), dua sisi; statistik = rata-rata beda proporsi."""
    sama = sorted(set(a) & set(b))
    beda = [a[t] - b[t] for t in sama]
    if not beda:
        return None, None, 0
    obs = sum(beda) / len(beda)
    if all(d == 0 for d in beda):
        return obs, 1.0, len(beda)
    lebih = 0
    for _ in range(B_PERM):
        s = sum(d if rng.random() < 0.5 else -d for d in beda) / len(beda)
        lebih += abs(s) >= abs(obs) - 1e-12
    return obs, (lebih + 1) / (B_PERM + 1), len(beda)


def pct(k, n):
    return f"{k}/{n} ({100 * k / n:.1f} %)" if n else "–"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="append", required=True, help="nama=folder_run")
    ap.add_argument("--rujukan", default=str(DIR / "agenekg_rujukan.json"))
    ap.add_argument("--tugas", default=str(DIR / "agenekg_tugas.json"))
    ap.add_argument("--rujukan-hrv", default=str(DIR / "agenekg_rujukan_hrv.json"))
    ap.add_argument("--json", default=None)
    ap.add_argument("--sampel-kode-ulang", default=None, help="tulis 10 %% sampel kode galat untuk dikode ulang")
    a = ap.parse_args()

    ruj = {r["id"]: r for r in json.loads(Path(a.rujukan).read_text(encoding="utf-8"))}
    tugas = {t["id"]: t for t in json.loads(Path(a.tugas).read_text(encoding="utf-8"))}
    d_frek = {}
    for h in json.loads(Path(a.rujukan_hrv).read_text(encoding="utf-8")):
        d = {}
        for k, ka, kb in (("lf_ms2", "lf_a", "lf_b"), ("hf_ms2", "hf_a", "hf_b"), ("lf_hf", "lfhf_a", "lfhf_b")):
            if h.get(kb):
                d[k] = abs(h[ka] - h[kb]) / abs(h[kb])
        d_frek["hrv_" + h["rekaman"]] = d

    rng = random.Random(BENIH)
    model = {}
    for s in a.run:
        nama, folder = s.split("=", 1)
        model[nama] = muat(folder, ruj, tugas, d_frek)

    print("## 1. Besaran dalam toleransi (CI 95 % bootstrap bergugus rekaman, 2.000 kali)\n")
    print("| Model | Jenis | Tugas-ulangan | Besaran benar | CI 95 % | Toleransi ketat | Toleransi longgar |")
    print("|---|---|---|---|---|---|---|")
    ringkas = {}
    for nama, baris in model.items():
        for j in JENIS_URUT + ["inti (QT + HRV)"]:
            bj = [b for b in baris if (b["jenis"] in INTI if j.startswith("inti") else b["jenis"] == j)]
            if not bj:
                continue
            k, n = proporsi(bj)
            ci = ci_bootstrap(bj, rng=rng)
            if j == "jebakan_takterjawab":
                kt = lg = "–"
            else:
                kt, lg = pct(*proporsi(bj, "ketat")), pct(*proporsi(bj, "longgar"))
            ringkas[(nama, j)] = dict(benar=k, n=n, ci=ci)
            print(f"| {nama} | {j} | {len(bj)} | {pct(k, n)} | "
                  f"{'–' if ci is None else f'{100 * ci[0]:.1f}–{100 * ci[1]:.1f} %'} | {kt} | {lg} |")

    print("\n## 2. Tugas-ulangan: seluruhnya benar, jalan-tapi-salah, menyerah\n")
    print("| Model | Jenis | Tugas-ulangan | Seluruhnya benar | Kode pernah jalan | Jalan-tapi-salah | Menyerah |")
    print("|---|---|---|---|---|---|---|")
    for nama, baris in model.items():
        for j in JENIS_URUT:
            bj = [b for b in baris if b["jenis"] == j]
            if not bj:
                continue
            n = len(bj)
            print(f"| {nama} | {j} | {n} | {pct(sum(b['semua_benar'] for b in bj), n)} | "
                  f"{pct(sum(b['jalan'] for b in bj), n)} | {pct(sum(b['jalan_tapi_salah'] for b in bj), n)} | "
                  f"{pct(sum(b['menyerah'] for b in bj), n)} |")

    print("\n## 3. Taksonomi galat (kode pertama yang cocok, E1 -> E8)\n")
    kode_semua = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
    print("| Model | Jenis | Gagal | " + " | ".join(kode_semua) + " |")
    print("|---|---|---|" + "---|" * len(kode_semua))
    for nama, baris in model.items():
        for j in JENIS_URUT + ["semua"]:
            bj = [b for b in baris if (j == "semua" or b["jenis"] == j) and b["kode"]]
            if not bj:
                continue
            c = Counter(b["kode"] for b in bj)
            print(f"| {nama} | {j} | {len(bj)} | " + " | ".join(str(c.get(k, 0)) for k in kode_semua) + " |")
    print("\nSubjenis E2/E4/E8:\n")
    for nama, baris in model.items():
        c = Counter((b["kode"], b["subkode"]) for b in baris if b["kode"] in ("E2", "E4", "E8"))
        print(f"- {nama}: " + "; ".join(f"{k} {s}: {n}" for (k, s), n in sorted(c.items(), key=lambda x: -x[1])))

    print("\n## 4. Eksploratif: galat eksekusi pertama yang gagal (semua tugas-ulangan)\n")
    for nama, baris in model.items():
        c = Counter(b["galat_pertama"] or "tidak ada eksekusi gagal" for b in baris)
        print(f"- {nama}: " + "; ".join(f"{k} {n}" for k, n in c.most_common(8)))

    print("\n## 5. Kesepakatan antar-ulangan\n")
    print("| Model | Jenis | Tugas | Kelima ulangan sama (seluruhnya benar atau tidak) | Tugas dengan >= 1 ulangan benar |")
    print("|---|---|---|---|---|")
    for nama, baris in model.items():
        for j in JENIS_URUT:
            per = defaultdict(list)
            for b in baris:
                if b["jenis"] == j:
                    per[b["tugas"]].append(b["semua_benar"])
            if not per:
                continue
            sama = sum(1 for v in per.values() if len(set(v)) == 1)
            print(f"| {nama} | {j} | {len(per)} | {pct(sama, len(per))} | {pct(sum(any(v) for v in per.values()), len(per))} |")

    nama_model = list(model)
    if len(nama_model) > 1:
        print("\n## 6. Uji permutasi berpasangan per tugas (tukar tanda, 10.000 kali, dua sisi)\n")
        print("| Jenis | Model A | Model B | Beda rata-rata proporsi (A − B) | p | Tugas |")
        print("|---|---|---|---|---|---|")
        for j in INTI:
            for i in range(len(nama_model)):
                for k in range(i + 1, len(nama_model)):
                    A, B = nama_model[i], nama_model[k]
                    pa = per_tugas([b for b in model[A] if b["jenis"] == j])
                    pb = per_tugas([b for b in model[B] if b["jenis"] == j])
                    obs, p, n = uji_permutasi(pa, pb, rng)
                    if obs is not None:
                        print(f"| {j} | {A} | {B} | {obs:+.3f} | {p:.4f} | {n} |")

    if a.json:
        Path(a.json).write_text(json.dumps({"model": model, "ringkas": {f"{m}|{j}": v for (m, j), v in ringkas.items()}},
                                           ensure_ascii=False, indent=1), encoding="utf-8")
    if a.sampel_kode_ulang:
        r2 = random.Random(BENIH + 1)
        baris = []
        for nama, bb in model.items():
            gagal = [b for b in bb if b["kode"]]
            for b in r2.sample(gagal, max(1, round(0.1 * len(gagal)))):
                baris.append(f"| {nama} | {b['tugas']}_u{b['ulang']} | {b['kode']} | {b['subkode'] or ''} |  |  |")
        Path(a.sampel_kode_ulang).write_text(
            f"# Kode ulang taksonomi AgenEKG (10 % sampel acak, benih {BENIH + 1})\n\n"
            + "Isi kolom **Kode pengguna** (E1–E8) tanpa melihat kolom kode otomatis bila bisa; transkrip ada di "
              "folder run model (`<tugas>_u<ulang>.json`).\n\n"
            + "| Model | Tugas-ulangan | Kode otomatis | Subjenis | Kode pengguna | Catatan |\n|---|---|---|---|---|---|\n"
            + "\n".join(baris) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
