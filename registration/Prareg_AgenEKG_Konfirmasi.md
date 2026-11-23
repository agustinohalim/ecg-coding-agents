# Rencana uji konfirmasi AgenEKG (22 November 2026)

> DIKUNCI saat dikomit, **sebelum** tugas konfirmasi dibangkitkan dan sebelum satu pun run konfirmasi dijalankan
> (pengguna memilih "Analisis ulang + uji konfirmasi", 22 Nov 2026, sesudah panel JIKI 2). Perubahan sesudah komit
> hanya lewat bagian "Penyimpangan" bertanggal di akhir berkas; isi di atasnya tidak disunting.

Induk: `Prareg_AgenEKG.md` (7 Nov 2026). Alasan: temuan "jawaban QT agen komersial lebih dekat ke rujukan daripada
jawaban konstan" (`Hasil_AgenEKG_17.md`) ditemukan **sesudah** semua hasil, di 45 tugas yang sama, dan panel 2
meminta uji di data yang belum disentuh. Uji ini menjawab satu pertanyaan: apakah keunggulan kesepakatan itu
bertahan pada rekaman QT Database yang belum pernah menjadi tugas.

## 1. Tugas

- Rekaman: semua calon QT yang lolos aturan `agenekg_tugas.tugas_qt` (rangkaian terpanjang ≥ 10 denyut `.q1c`
  beruntun, tanpa denyut lain di antaranya, RR < 2 s, di luar 5 pilot) **dan tidak** terpilih sebagai 45 tugas
  utama. Menurut `Hasil_AgenEKG_17.md` ada 31. Bila pembangkit menghasilkan jumlah lain, semuanya tetap dipakai dan
  jumlahnya dicatat.
- Teks tugas, jendela (±10 sampel di sekitar rangkaian), toleransi (20 ms), dan rujukan (`R.ringkas`, dibulatkan
  2 desimal) identik dengan tugas utama. Pembangkit: `agenekg_tugas_konfirmasi.py`; ia memeriksa bahwa undian
  benih 20261107 menghasilkan 45 tugas utama yang sama persis dengan `agenekg_tugas.json`.
- Yang sudah diketahui sebelum uji: nilai rujukan rekaman-rekaman ini pernah dihitung untuk konstanta luar-tugas
  di `Hasil_AgenEKG_17.md` (hanya median dan laju kena yang dilihat). Dua di antaranya mungkin pernah dipakai di
  tugas jebakan "jendela di luar rekaman" (berkas sama, jendela mustahil); itu dicatat, tidak dikeluarkan.
  Tidak ada run agen pada tugas-tugas ini.

## 2. Agen

DeepSeek-V4-flash (`deepseek-v4-flash-openai`) lewat gateway yang sama, `agenekg_agen.py` tanpa perubahan, suhu
bawaan, 10 giliran, `--luar-puncak`, kontainer `agenekg-py:1`, 5 ulangan per tugas (31 × 5 = 155 run), dua proses
(`--ulang-ke 1,3,5` dan `2,4`). Peluncur `jalan_konfirmasi.ps1` (memeriksa pengisi daya dan image Docker).
Keluaran `C:\Data\AgenEKG_runs\konfirmasi_deepseek-v4-flash-openai`. Pembanding NeuroKit2 DWT dijalankan pada tugas
yang sama dengan `agenekg_dasar_nk.py --tugas/--rujukan` (sekunder).

## 3. Pembanding (ditetapkan dari 45 tugas utama, tanpa melihat tugas konfirmasi)

- **Konstan:** median rujukan 45 tugas utama per besaran.
- **Model RR:** kuadrat terkecil QT = a + b·RR pada 45 tugas utama (RR = (QT/QTcB)² dari rujukan), diterapkan ke RR
  rujukan tugas konfirmasi; QTcB = QT/√RR, QTcF = QT/∛RR. Model ini tahu laju jantung dengan tepat dan tidak tahu
  apa pun tentang batas gelombang.

## 4. Hipotesis utama (QT saja)

Selisih berpasangan per tugas = rata-rata atas run dari |agen − rujukan| dikurangi |pembanding − rujukan|;
ringkasan = median atas tugas; selang bootstrap tugas 10.000 ulangan (benih 20261122), **98,33 %** (Bonferroni
atas tiga hipotesis).

- **H1:** agen lebih dekat daripada konstan — batas atas selang < 0.
- **H2:** agen lebih dekat daripada model RR — batas atas selang < 0.
- **H3:** kesepakatan berurutan di tingkat run — Spearman ρ (semua run berjawaban numerik) batas bawah > 0.

Run tanpa jawaban numerik bukan nol keluar dari ukuran kesepakatan dan dihitung; bila lebih dari 10 % run, hal itu
ditulis bersama hasil H1–H3. Pada laju dalam-toleransi, run seperti itu dihitung salah.

## 5. Sekunder (dilaporkan, tanpa aturan keputusan)

QTcB dan QTcF dengan ukuran yang sama; galat mutlak median, bias Bland–Altman dan batas kesepakatan 95 %, kemiringan
Theil–Sen beserta selang terhadap 1; laju dalam 10/20/40 ms untuk agen, konstan, dan model RR; jumlah run "semua
benar"; NeuroKit2 DWT dengan ukuran yang sama. Skrip: `agenekg_konfirmasi_nilai.py` (dikomit bersama berkas ini).

## 6. Aturan keputusan untuk naskah

| Hasil | Yang ditulis |
|---|---|
| H1 dan H2 didukung | Kesepakatan QT agen terkonfirmasi pada rekaman baru, melebihi jawaban konstan dan model yang hanya tahu laju jantung. |
| H1 didukung, H2 tidak | Agen lebih dekat daripada konstan, tetapi tidak terbukti melebihi model laju jantung; klaim "mengukur batas gelombang" tidak dibuat. |
| H1 tidak didukung | Temuan kesepakatan eksploratif tidak terulang; klaim itu keluar dari judul dan abstrak dan dilaporkan sebagai tidak terkonfirmasi. |

H3 dilaporkan apa pun hasilnya. Semua hasil masuk naskah, ke arah mana pun. Tidak ada analisis konfirmasi lain
yang dipakai untuk klaim; analisis tambahan sesudah hasil ditandai pasca-hasil.

## Penyimpangan

**22 November 2026, 21:15 — dua gangguan saat run, sebelum hasil konfirmasi dinilai atau dibaca.**

1. 19:07: run dihentikan Claude Code karena memori laptop kritis (proses lain memakai ±4 GB). 73 run tersimpan
   utuh; run yang terputus dihapus dan diulang dari awal oleh peluncur (seperti Penyimpangan ketujuh induk).
   Dilanjutkan 20:08 atas izin pengguna ("go").
2. 21:13: proses ulangan 1, 3, 5 berhenti karena gateway menolak permintaan run `qt_sel301` ulangan 5 dengan
   HTTP 413 (badan permintaan terlalu besar; `agenekg_agen.py` menghentikan proses pada penolakan 4xx agar galat
   penyedia tidak tercatat sebagai jawaban agen). 106 run tersimpan. Run itu diulang dari awal bersama 48 run
   yang belum dijalankan. Aturan yang ditetapkan sekarang, sebelum penilaian: bila satu tugas-ulangan ditolak 413
   lagi, ia dinilai "tanpa jawaban yang bisa dipakai" (salah pada laju dalam-toleransi, keluar dari ukuran
   kesepakatan) dan dilaporkan; run lain dilanjutkan tanpa dia.
3. 21:42, masih sebelum penilaian: `qt_sel301` ulangan 5 selesai pada percobaan kedua; tugas-ulangan lain
   (`qt_sel31` ulangan 1) ditolak 413 untuk pertama kali. Aturan butir 2 berlaku per tugas-ulangan: penolakan 413
   pertama diulang dari awal, yang kedua dinilai tanpa jawaban. Jumlah 413 dilaporkan. Sisa run (ulangan 1, 3, 5)
   dibagi ke tiga proses, bukan satu, agar selesai lebih cepat; tugas, kerangka, dan model tidak berubah.
