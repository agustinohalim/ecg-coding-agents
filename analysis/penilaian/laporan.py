"""The six Markdown sections that `agenekg_analisis.py` prints; the section text stays in Indonesian."""
from collections import Counter, defaultdict

from .statistik import ci_bootstrap, per_tugas, proporsi, uji_permutasi

JENIS_URUT = ["qt", "hrv", "jebakan_ektopik", "jebakan_laju", "jebakan_kanal", "jebakan_takterjawab"]
INTI = ["qt", "hrv"]
KODE_SEMUA = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]


def pct(k, n):
    return f"{k}/{n} ({100 * k / n:.1f} %)" if n else "–"


def ringkasan_toleransi(model, rng):
    """Section 1 rows in print order; the bootstrap draws from rng in this order."""
    hasil = []
    for nama, baris in model.items():
        for j in JENIS_URUT + ["inti (QT + HRV)"]:
            bj = [b for b in baris if (b["jenis"] in INTI if j.startswith("inti") else b["jenis"] == j)]
            if bj:
                hasil.append(ringkas_jenis(nama, j, bj, rng))
    return hasil


def ringkas_jenis(nama, j, bj, rng):
    k, n = proporsi(bj)
    ci = ci_bootstrap(bj, rng=rng)
    if j == "jebakan_takterjawab":
        kt = lg = "–"
    else:
        kt, lg = pct(*proporsi(bj, "ketat")), pct(*proporsi(bj, "longgar"))
    return dict(nama=nama, jenis=j, tugas_ulangan=len(bj), benar=k, n=n, ci=ci, ketat=kt, longgar=lg)


def cetak_toleransi(ringkasan):
    print("## 1. Besaran dalam toleransi (CI 95 % bootstrap bergugus rekaman, 2.000 kali)\n")
    print("| Model | Jenis | Tugas-ulangan | Besaran benar | CI 95 % | Toleransi ketat | Toleransi longgar |")
    print("|---|---|---|---|---|---|---|")
    for s in ringkasan:
        ci = s["ci"]
        print(f"| {s['nama']} | {s['jenis']} | {s['tugas_ulangan']} | {pct(s['benar'], s['n'])} | "
              f"{'–' if ci is None else f'{100 * ci[0]:.1f}–{100 * ci[1]:.1f} %'} | {s['ketat']} | {s['longgar']} |")


def cetak_hasil_tugas(model):
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


def cetak_taksonomi(model):
    print("\n## 3. Taksonomi galat (kode pertama yang cocok, E1 -> E8)\n")
    print("| Model | Jenis | Gagal | " + " | ".join(KODE_SEMUA) + " |")
    print("|---|---|---|" + "---|" * len(KODE_SEMUA))
    for nama, baris in model.items():
        for j in JENIS_URUT + ["semua"]:
            bj = [b for b in baris if (j == "semua" or b["jenis"] == j) and b["kode"]]
            if not bj:
                continue
            c = Counter(b["kode"] for b in bj)
            print(f"| {nama} | {j} | {len(bj)} | " + " | ".join(str(c.get(k, 0)) for k in KODE_SEMUA) + " |")
    print("\nSubjenis E2/E4/E8:\n")
    for nama, baris in model.items():
        c = Counter((b["kode"], b["subkode"]) for b in baris if b["kode"] in ("E2", "E4", "E8"))
        print(f"- {nama}: " + "; ".join(f"{k} {s}: {n}" for (k, s), n in sorted(c.items(), key=lambda x: -x[1])))


def cetak_galat_pertama(model):
    print("\n## 4. Eksploratif: galat eksekusi pertama yang gagal (semua tugas-ulangan)\n")
    for nama, baris in model.items():
        c = Counter(b["galat_pertama"] or "tidak ada eksekusi gagal" for b in baris)
        print(f"- {nama}: " + "; ".join(f"{k} {n}" for k, n in c.most_common(8)))


def cetak_kesepakatan(model):
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


def cetak_permutasi(model, rng):
    nama_model = list(model)
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
