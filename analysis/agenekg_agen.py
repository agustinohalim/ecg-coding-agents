"""Kerangka agen pengode AgenEKG (lihat Prareg_AgenEKG.md bagian 6).

Satu kerangka untuk semua model: model menulis satu blok kode Python per giliran, kode dijalankan dalam
kontainer Docker `agenekg-py:1` tanpa jaringan, keluaran dikembalikan, maksimal 10 giliran (sebelum giliran
terakhir model diberi tahu bahwa itu giliran terakhir), model mengakhiri dengan `FINAL: {json}`. Kotak pasir hanya berisi berkas `.hea`/`.dat` rekaman tugas —
berkas anotasi tidak pernah disalin.

Model dipanggil lewat API kompatibel OpenAI (LM Studio lokal: http://localhost:1234/v1).
Semua transkrip disimpan sebagai JSON di folder keluaran (di luar repo).

Pakai:
    python -X utf8 Riset/EKG/agenekg_agen.py --tugas tugas.json --model <id> --ulang 1 \
        --keluar C:/Data/AgenEKG_runs/<nama>
"""
import argparse
import json
import re
import os
import shutil
import stat
import subprocess
import time
from pathlib import Path

import requests

SISTEM = (
    "You are a coding agent analysing ECG recordings. Files for the task are in the current working "
    "directory. Each turn, reply with exactly one Python code block (```python ... ```); it will be run "
    "with Python 3.12 (numpy, scipy, pandas, wfdb, neurokit2 installed; no internet) and you will see "
    "its stdout and stderr. When you are confident of the answer, reply with a line starting with "
    "FINAL: followed by the JSON object requested in the task, and no code block. If the task cannot be "
    "answered from the files, reply FINAL: {\"unanswerable\": true, \"reason\": \"...\"}."
)
MAKS_GILIRAN = 10  # Penyimpangan 7 Nov 2026 (Prareg_AgenEKG.md): dari 6
AKHIR = "This is your last turn: reply now with FINAL: {json}."
BATAS_DETIK = 120
POTONG = 4000
GAMBAR = "agenekg-py:1"


def kunci_api(nama):
    """Kunci API dari peubah lingkungan `nama`, atau dari ~/.secrets/<nama> (di luar repo). Tidak dicetak."""
    import os
    if not nama:
        return None
    if os.environ.get(nama):
        return os.environ[nama].strip()
    f = Path.home() / ".secrets" / nama
    if f.exists():
        isi = f.read_text(encoding="utf-8-sig").strip()
        m = re.search(r'"apiKey"\s*:\s*"([^"]+)"', isi)  # berkas konfigurasi gateway (JSON)
        return m.group(1) if m else isi
    raise SystemExit(f"Kunci {nama} tidak ditemukan (peubah lingkungan atau ~/.secrets/{nama}).")


KUNCI = None
LUAR_PUNCAK = False


def tunggu_luar_puncak():
    """Tarif puncak DeepSeek: Senin–Jumat 01–04 dan 06–10 UTC (harga dua kali). Tunggu sampai jam luar puncak.

    Dicek sebelum tiap panggilan; tugas yang sedang berjalan hanya tertunda, tidak diulang.
    """
    import datetime as dt
    while LUAR_PUNCAK:
        t = dt.datetime.now(dt.timezone.utc)
        if t.weekday() >= 5 or not (1 <= t.hour < 4 or 6 <= t.hour < 10):
            return
        time.sleep(60)


def panggil(url, model, pesan, suhu):
    tunggu_luar_puncak()
    badan = {"model": model, "messages": pesan}
    if suhu is not None:
        badan["temperature"] = suhu
    kepala = {"Authorization": f"Bearer {KUNCI}"} if KUNCI else {}
    # Galat jaringan/server penyedia bukan galat agen: ulangi dengan jeda makin panjang (total ±30 menit),
    # lalu hentikan run. Gangguan gateway 7 Nov 2026 lebih lama dari 3 × 30 s.
    jeda = [30, 60, 120, 300, 600, 900]
    for coba in range(len(jeda) + 1):
        try:
            r = requests.post(f"{url}/chat/completions", json=badan, headers=kepala, timeout=600)
            if 400 <= r.status_code < 500 and r.status_code != 429:
                raise RuntimeError(f"Penyedia model menolak: HTTP {r.status_code} {r.text[:200]}")
            if r.status_code >= 400:
                raise requests.ConnectionError(f"HTTP {r.status_code} {r.text[:200]}")
            d = r.json()
            return d["choices"][0]["message"]["content"], d.get("usage"), coba
        except (requests.Timeout, requests.ConnectionError) as e:
            print(f"[ulang API {coba + 1}] {str(e)[:200]}", flush=True)
            if coba == len(jeda):
                raise RuntimeError(f"Penyedia model gagal {coba + 1} kali: {e}") from e
            time.sleep(jeda[coba])
            tunggu_luar_puncak()


def jalankan(kode, kotak):
    (kotak / "_agen.py").write_text(kode, encoding="utf-8")
    perintah = ["docker", "run", "--rm", "--network", "none", "--memory", "2g", "--cpus", "2",
                "-v", f"{kotak.resolve()}:/work", "-w", "/work", GAMBAR, "python", "_agen.py"]
    t0 = time.time()
    try:
        p = subprocess.run(perintah, capture_output=True, text=True, timeout=BATAS_DETIK + 30,
                           encoding="utf-8", errors="replace")
        keluar = p.stdout[-POTONG:] + ("\n[stderr]\n" + p.stderr[-POTONG:] if p.stderr else "")
        kode_keluar = p.returncode
    except subprocess.TimeoutExpired:
        keluar, kode_keluar = f"[timeout after {BATAS_DETIK} s]", -9
    if "docker API" in keluar or "Unable to find image" in keluar:
        # Galat kotak pasir, bukan galat agen: hentikan run agar tidak tercatat sebagai jawaban agen.
        raise RuntimeError("Kotak pasir Docker gagal: " + keluar[-300:])
    return keluar, kode_keluar, round(time.time() - t0, 1)


def satu_tugas(tugas, args, ulang):
    kotak = Path(args.keluar) / f"{tugas['id']}_u{ulang}"
    if kotak.exists():
        # sisa tugas yang terputus; salinan .dat bisa read-only di Windows
        shutil.rmtree(kotak, onexc=lambda f, p, e: (os.chmod(p, stat.S_IWRITE), f(p)))
    kotak.mkdir(parents=True)
    for b in tugas["berkas"]:
        shutil.copyfile(Path(args.data) / b, kotak / Path(b).name)  # tanpa atribut read-only
    pesan = [{"role": "system", "content": SISTEM}, {"role": "user", "content": tugas["teks"]}]
    log = {"tugas": tugas["id"], "model": args.model, "ulang": ulang, "giliran": [], "final": None}
    for g in range(MAKS_GILIRAN):
        jawab, pakai, ulang_api = panggil(args.url, args.model, pesan, args.suhu)
        meta = {"token": pakai, "ulang_api": ulang_api}
        pesan.append({"role": "assistant", "content": jawab})
        m_final = re.search(r"^FINAL:\s*(\{.*\})", jawab, re.M | re.S)
        m_kode = re.search(r"```(?:python)?\n(.*?)```", jawab, re.S)
        if m_final and not m_kode:
            log["final"] = m_final.group(1).strip()
            log["giliran"].append({"model": jawab, **meta})
            break
        if not m_kode:
            umpan = "No code block and no FINAL line found. Reply with one Python code block or FINAL: {json}."
            log["giliran"].append({"model": jawab, "eksekusi": None, **meta})
        else:
            keluar, kk, dt = jalankan(m_kode.group(1), kotak)
            log["giliran"].append({"model": jawab, "kode_keluar": kk, "detik": dt, "keluaran": keluar, **meta})
            umpan = f"Exit code {kk}. Output:\n{keluar}"
        if g == MAKS_GILIRAN - 2:
            umpan += "\n\n" + AKHIR
        pesan.append({"role": "user", "content": umpan})
    (kotak / "_agen.py").unlink(missing_ok=True)
    for b in tugas["berkas"]:  # salinan data tidak perlu disimpan; hemat disk
        (kotak / Path(b).name).unlink(missing_ok=True)
    (Path(args.keluar) / f"{tugas['id']}_u{ulang}.json").write_text(
        json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    return log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tugas", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--url", default="http://localhost:1234/v1")
    ap.add_argument("--data", default="C:/Data/PhysioNet")
    ap.add_argument("--keluar", required=True)
    ap.add_argument("--ulang", type=int, default=1)
    ap.add_argument("--ulang-ke", default=None,
                    help="jalankan hanya ulangan ini, mis. 2 atau 1,3,5 (untuk beberapa proses sejajar)")
    ap.add_argument("--suhu", type=float, default=None)
    ap.add_argument("--kunci", default=None, help="nama peubah/berkas kunci API, mis. DEEPSEEK_API_KEY")
    ap.add_argument("--luar-puncak", action="store_true", help="tunda panggilan API selama jam tarif puncak DeepSeek")
    args = ap.parse_args()
    global KUNCI, LUAR_PUNCAK
    KUNCI = kunci_api(args.kunci)
    LUAR_PUNCAK = args.luar_puncak
    cek = subprocess.run(["docker", "image", "inspect", GAMBAR], capture_output=True, text=True)
    if cek.returncode != 0:
        raise SystemExit(f"Docker atau gambar {GAMBAR} tidak tersedia: {cek.stderr.strip()[:300]}")
    daftar = json.loads(Path(args.tugas).read_text(encoding="utf-8"))
    ulangan = [int(x) for x in args.ulang_ke.split(",")] if args.ulang_ke else range(1, args.ulang + 1)
    for t in daftar:
        for u in ulangan:
            if (Path(args.keluar) / f"{t['id']}_u{u}.json").exists():
                continue  # sudah selesai pada run sebelumnya (lanjut sesudah terputus)
            log = satu_tugas(t, args, u)
            print(t["id"], u, "FINAL" if log["final"] else "tanpa FINAL", len(log["giliran"]), "giliran", flush=True)


if __name__ == "__main__":
    main()
