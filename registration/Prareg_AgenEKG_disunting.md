# Pra-daftar AgenEKG (7 November 2026)

> TERKUNCI 7 November 2026 (izin komit pengguna: "go"). Butir bertanda "BELUM DITETAPKAN" diputuskan
> lewat "Penyimpangan" bertanggal di akhir berkas **sebelum** agen dijalankan pada set utama; selain itu isi di atas
> bagian Penyimpangan tidak disunting.

Rencana: `Artikel_AgenEKG_Rencana.md` (A/B disetujui 7 Nov 2026). Rujukan QT: `Hasil_AgenEKG_0.md`.

## 1. Pertanyaan dan ukuran utama

Proporsi tugas yang jawaban numerik akhirnya berada dalam toleransi terhadap rujukan anotasi ahli, per
model, untuk tugas QT/QTc dan HRV domain frekuensi (inti), dengan CI bootstrap bergugus rekaman. Ukuran
kedua: laju "jalan-tapi-salah" (kode selesai tanpa galat, keluar angka, angka di luar toleransi);
taksonomi galat; kesepakatan antar-5-ulangan.

## 2. Data dan pembagian

- QT: QT Database 1.0.0, 102 rekaman layak (`Hasil_AgenEKG_0.md` bagian 1). **5 rekaman pilot** dipilih
  acak (benih 20261107) dari rekaman yang denyutnya beruntun (denyut ber-RR = denyut − 1) dan **tidak**
  punya `.q2c`; pilot dikeluarkan dari set utama. Rekaman `.q2c` (11) tetap di set utama.
- HRV: Fantasia 1.0.0 (40 rekaman, anotasi denyut diverifikasi visual). Jendela 5 menit pertama yang
  bebas denyut non-normal — BELUM DITETAPKAN: aturan pemilihan jendela.
- Jebakan: MIT-BIH Arrhythmia (denyut ektopik: tugas NN vs RR), turunan QTDB/Fantasia yang diresampel
  ke laju lain dengan header dibetulkan, sadapan ditukar urutannya, dan pertanyaan yang tak bisa dijawab
  (sadapan yang tidak ada).

## 3. Rujukan

- QT per denyut = akhir T − awal QRS dari `.q1c`; QTc Bazett QT/√RR, Fridericia QT/∛RR (RR dalam s, RR =
  jarak ke puncak denyut beranotasi sebelumnya bila < 2 s). Nilai rekaman = rata-rata denyut beranotasi.
  Kode: `agenekg_rujukan_qt.py`.
- HRV: NN dari anotasi Fantasia; SDNN, RMSSD, pNN50 dihitung langsung; LF (0,04–0,15 Hz), HF
  (0,15–0,40 Hz), LF/HF dari (a) NeuroKit2 dan (b) Welch pada NN yang diinterpolasi 4 Hz (implementasi
  sendiri). Skrip `agenekg_rujukan_hrv.py` — BELUM DITULIS.
- Agen **tidak** pernah melihat berkas anotasi; kotak pasir hanya berisi `.hea` dan `.dat`.

## 4. Toleransi (disetujui pengguna 7 Nov 2026)

| Besaran | Benar bila | Kepekaan |
|---|---|---|
| HR rata-rata | ≤ 2 bpm | 1, 5 bpm |
| QT, QTcB, QTcF rata-rata | ≤ 20 ms (median sebaran annotator 8,3 ms, `Hasil_AgenEKG_0.md`) | 10, 40 ms |
| SDNN, RMSSD | ≤ 10 % relatif | 5, 20 % |
| pNN50 | ≤ 5 poin persen | 2, 10 |
| LF, HF, LF/HF | ≤ max(20 %, 1,5 × beda relatif implementasi a vs b) | 10, 40 % |
| Tugas tak terjawab | agen menyatakan tidak bisa dijawab | — |

## 5. Tugas

Teks tugas memuat: nama rekaman, laju sampel **tidak** disebut (agen harus membaca header), jendela
sampel, sadapan, definisi besaran (sama dengan bagian 3), dan format jawaban JSON. Daftar tugas lengkap
ditulis ke `agenekg_tugas.json` — BELUM DITETAPKAN: daftar lengkap; sasaran ±100 tugas (QT ±45, HRV ±35,
jebakan ±20).

## 6. Agen dan model

- Kerangka sama untuk semua model (`agenekg_agen.py`): pesan sistem tetap; tiap giliran model menulis
  satu blok kode Python; kode dijalankan dalam kontainer Docker **tanpa jaringan**, batas 120 s per
  eksekusi; keluaran (stdout/stderr, dipotong 4.000 karakter) dikembalikan; maksimal 6 giliran; model
  mengakhiri dengan `FINAL: {json}`. Pustaka di kontainer: numpy, scipy, pandas, wfdb, neurokit2 (versi
  dicatat).
- Model lokal (inti replikasi): Qwen2.5-Coder-7B-Instruct GGUF Q4_K_M lewat LM Studio. BELUM DITETAPKAN:
  1–2 model lokal lain ≤ 8B; model frontier tier gratis (butuh kunci API dari pengguna; data ODC-By boleh).
- Suhu: bawaan penyedia, dicatat. 5 ulangan per tugas per model.

## 7. Taksonomi galat (aturan, bukan penilaian bebas)

E1 kode tidak pernah jalan sampai akhir · E2 tidak ada jawaban/format salah · E3 laju sampel/satuan
salah (galat ≈ rasio laju atau faktor 1000) · E4 sadapan/jendela salah · E5 deteksi batas gelombang
salah (QT) / deteksi R salah (HRV) · E6 RR dipakai sebagai NN (tidak membuang ektopik) · E7 API pustaka
tidak ada/berubah (AttributeError/TypeError pada pustaka) · E8 lainnya. Satu galat = satu kode
pertama yang cocok, urutan E1→E8; dikode otomatis dari log, 10 % sampel dikode ulang pengguna.

## 8. Analisis

Proporsi benar per model × jenis tugas, CI bootstrap 2.000 kali bergugus rekaman; perbandingan model
dengan uji permutasi berpasangan per tugas; tidak ada uji hipotesis lain di luar ini kecuali ditandai
eksploratif.

## Penyimpangan

**7 November 2026 — batas giliran dan giliran terakhir (disetujui pengguna: "go").** Alasan: pada pilot
DeepSeek-V4 flash dan pro (`Hasil_AgenEKG_2.md`) semua 7 tugas yang selesai habis di batas 6 giliran tanpa
`FINAL`; batas itu mengukur lama jelajah, bukan kemampuan menghitung. Diputuskan sebelum run utama, berlaku
untuk semua model (termasuk Qwen2.5-Coder-7B), pilot diulang sesudahnya:

1. Bagian 6 "maksimal 6 giliran" menjadi **maksimal 10 giliran**.
2. Umpan balik sebelum giliran terakhir ditambah satu kalimat tetap: "This is your last turn: reply now with
   FINAL: {json}." Tugas tanpa `FINAL` sesudahnya tetap E2.

Tidak ada butir lain yang berubah.

**7 November 2026 — model frontier (disetujui pengguna: "both").** Butir bagian 6 "model frontier tier gratis
— BELUM DITETAPKAN" ditetapkan: **dua** model DeepSeek berbayar, keduanya pada semua tugas, 5 ulangan, sama
seperti model lokal:

- `deepseek-v4-flash-openai` dan `deepseek-v4-pro-openai`, lewat gateway pihak ketiga yang kompatibel OpenAI
  [nama penyedia disunting]. Halaman harga resmi (dibaca 7 Nov 2026) menyebut versi DeepSeek-V4.1-Flash-1017
  dan DeepSeek-V4-Pro-0813; medan `model` di tiap jawaban dicatat di log.
- Mode berpikir bawaan penyedia (aktif), suhu bawaan. Token per giliran dicatat.
- Proksi menyisipkan teks sistem sendiri sebelum pesan kami (`Hasil_AgenEKG_2.md` bagian 3); dilaporkan
  sebagai keterbatasan, tidak dikoreksi.
- Hanya data terbuka (ODC-By) yang dikirim.

Model lokal tambahan ≤ 8B tetap BELUM DITETAPKAN.

**7 November 2026 — jendela HRV, rujukan LF/HF, definisi QT, daftar tugas, penilaian tak terjawab (disetujui
pengguna: "go").** Rincian dan angka: `Hasil_AgenEKG_4.md`, `Hasil_AgenEKG_5.md`. Diputuskan sebelum run utama.

1. Jendela HRV (bagian 2): anotasi Fantasia semuanya `N`, jadi "bebas denyut non-normal" diganti aturan RR —
   jendela 5 menit tak bertumpang pertama dengan semua RR 0,3–2,0 s dan tiap RR berubah ≤ 20 % dari RR
   sebelumnya; rekaman tanpa jendela begitu dikeluarkan (34 dari 40 lolos).
2. Rujukan LF/HF (bagian 3): nilai rujukan = implementasi (b) Welch sendiri; implementasi (a) = NeuroKit2
   `hrv_frequency` dengan `normalize=False` (bawaannya bukan ms²). Toleransi per tugas max(20 %, 1,5 × |a − b|
   / b) sesuai bagian 4. Skrip `agenekg_rujukan_hrv.py`.
3. Definisi QT (bagian 5, mengubah "sadapan" di teks tugas QT): teks tugas QT tidak menyebut satu kanal; QT =
   awal QRS paling awal sampai akhir T paling akhir di kedua kanal, karena anotasi manual QTDB tidak terikat
   satu sadapan. Jendela tugas = rangkaian terpanjang denyut `.q1c` beruntun tanpa denyut lain di antaranya
   (`.atr`, atau `.pu0` bila tak ada), ≥ 10 denyut. QTcF ikut ditanyakan.
4. Daftar tugas (bagian 5): 99 tugas — QT 45, HRV 34, jebakan 20 (ektopik MIT-BIH 6, laju sampel lain 5,
   urutan kanal ditukar 4, tak terjawab 5) — dibangkitkan `agenekg_tugas.py` (benih 20261107) ke
   `agenekg_tugas.json` dan `agenekg_rujukan.json`.
5. Penilaian (bagian 4): tugas tak terjawab benar bila FINAL memuat `"unanswerable": true`; pada tugas yang bisa
   dijawab, jawaban tak terjawab dihitung salah untuk tiap besaran. Penilai `agenekg_nilai.py`.

**19 November 2026 — cakupan model dan sasaran terbit (disetujui pengguna: pilihan "AgenEKG versi lokal").**
Alasan: kunci gateway DeepSeek kena batas anggaran (HTTP 402, 8 Nov) dan pengguna tidak membuka anggaran baru;
sasaran terbit berubah ke jurnal SINTA 3/4. Diputuskan sebelum model tambahan dijalankan pada set utama.

1. Bagian 6 "1–2 model lokal lain ≤ 8B — BELUM DITETAPKAN" ditetapkan: **Llama-3.1-8B-Instruct** GGUF Q4_K_M
   dan **Qwen2.5-Coder-3B-Instruct** GGUF Q4_K_M, keduanya lewat LM Studio di RTX 5060 8 GB, kerangka, pesan
   sistem, tugas (99 × 5 ulangan), batas 10 giliran, suhu bawaan, dan penilaian sama dengan Qwen2.5-Coder-7B.
   Tujuan: satu keluarga lain pada ukuran sama (Llama 8B vs Qwen 7B) dan satu ukuran lebih kecil pada keluarga
   sama (Qwen 3B vs 7B). Panjang konteks dicatat di log; satu pilot pada `agenekg_tugas_pilot.json` per model
   hanya untuk memastikan kerangka jalan, tidak dinilai.
2. Run DeepSeek dihentikan pada keadaan 8 Nov (flash 220/495, pro 44/495, hanya tugas QT). Angka DeepSeek tidak
   dipakai untuk klaim atau uji; bila dilaporkan, hanya sebagai catatan eksploratif bertanda "sebagian" di
   bagian keterbatasan. Perbandingan "model lokal vs frontier" di bagian 1 gugur; pertanyaan utama menjadi
   ketepatan dan jenis galat agen pengode lokal ≤ 8B.
3. Uji bagian 7 dijalankan antar ketiga model lokal (CI bootstrap bergugus rekaman, uji permutasi berpasangan
   per jenis tugas), tanpa model frontier.

Tidak ada butir lain yang berubah.

**19 November 2026 — pembanding NeuroKit2 tanpa agen (disetujui pengguna: "Ya, tambahkan").** Alasan: pemeriksaan
kebaruan 19 Nov (`Kebaruan_AgenEKG_2026-11-19.md`) menemukan pracetak yang melaporkan galat QT NeuroKit2 jauh di
atas toleransi 20 ms; tanpa pembanding, galat agen tidak bisa dipisahkan dari galat pustaka yang dipanggilnya.
Ditambahkan sebagai analisis **eksploratif**, tidak menggantikan ukuran utama bagian 1 dan tidak ikut uji bagian 8.
Diputuskan sebelum pembanding dijalankan.

1. Pipa tetap tanpa LLM (`agenekg_dasar_nk.py`), di kontainer `agenekg-py:1` yang sama (neurokit2 0.3.0, tanpa
   jaringan), pada 94 tugas yang bisa dijawab; laju dari header, kanal menurut nama di teks tugas.
2. QT: per kanal `ecg_clean` + `ecg_peaks` + `ecg_delineate` bawaan (metode `dwt`); denyut = puncak R yang terdeteksi
   di jendela tugas; QT per denyut = awal QRS paling awal sampai akhir T paling akhir di kedua kanal (pasangan
   denyut antarkanal = puncak R terdekat ≤ 50 ms); RR dari puncak R kanal pertama; QTc seperti teks tugas.
   Kepekaan: metode `peak` dan `cwt`.
3. HRV dan jebakan: `ecg_clean` + `ecg_peaks` bawaan pada kanal bernama; NN = selang antar-puncak di jendela tanpa
   koreksi ektopik; besaran domain waktu menurut teks tugas; LF/HF dari `hrv_frequency(normalize=False)`.
4. Dinilai dengan `agenekg_analisis.py` dan toleransi bagian 4 yang sama, satu ulangan (pipa deterministik).

Tidak ada butir lain yang berubah.

**19 November 2026 — run model lokal sejajar (diminta pengguna: "go lbh banyak agar cpt selesai").** Alasan
kecepatan; tidak menyentuh tugas, prompt, batas giliran, suhu, atau penilaian.

1. Ulangan dibagi ke tiga proses `agenekg_agen.py --ulang-ke` (1,4 / 2,5 / 3) yang memanggil model yang sama
   bersamaan. Tiap tugas-ulangan punya folder kerja dan berkas hasil sendiri; berkas hanya ditulis di akhir.
2. Percobaan pertama (Qwen 3B, 14.55–15.01) memuat model dengan konteks 16.384 dan `--parallel 4`. LM Studio
   membagi konteks itu bersama antar-permintaan serentak, sehingga ketiga proses berhenti dengan "Context size has
   been exceeded". Penolakan itu terjadi sebelum jawaban dibuat, jadi tidak ada tugas-ulangan yang tersimpan
   terpotong; yang gagal dijalankan ulang dari awal. 73 tugas-ulangan yang tersimpan tetap dipakai.
3. Sesudahnya model dimuat dengan konteks 32.768 (batas Qwen 3B; permintaan 49.152 dipangkas LM Studio) dan
   `--parallel 2`, jadi paling banyak dua percakapan berjalan sekaligus dengan jatah 16.384 masing-masing; proses
   ketiga mengantre. Batas 16.384 per percakapan tidak pernah mengikat: puncak token satu percakapan 8.228 pada run
   7B (495 tugas-ulangan) dan 9.174 pada 73 tugas-ulangan 3B pertama, dibaca dari kolom `token` log.
4. Pilot Llama-3.1-8B dengan konteks 16.384 dihentikan 19 Nov 15.38 sesudah 37 menit tanpa satu tugas selesai:
   tiap panggilan habis batas baca 600 s (VRAM 7,6 dari 8 GB). Pengaturan Llama ditetapkan sebelum pilot diulang.

Tidak ada butir lain yang berubah.

**21 November 2026 — pengaturan run Llama-3.1-8B (diputuskan pengguna 19 Nov: "ttp 16.384").** Tidak menyentuh
tugas, prompt, batas giliran, suhu, atau penilaian.

1. Satu proses berurutan (`Riset/EKG/jalan_llama.ps1`, komit 2bcb5b5): model dimuat dengan konteks 16.384 dan
   `--parallel 1`, sesudah aplikasi lain yang memakai GPU ditutup supaya model dan konteksnya muat di VRAM
   (7,3 dari 8,15 GB terpakai). Uji sebelum run: prompt 15.900 token selesai dalam 10 detik tanpa meluap ke RAM.
2. Pilot ulang 5/5 tugas (19 Nov 20.16–20.27), lalu run utama 495 tugas-ulangan (19 Nov 20.28 – 21 Nov 01.17),
   tanpa satu pun panggilan yang habis batas baca.
3. Run dijeda pengguna 20 Nov 09.07–21.45. Tugas-ulangan yang sedang berjalan saat itu belum punya berkas hasil,
   jadi dijalankan ulang dari awal; 362 yang sudah tersimpan dilewati.
4. Mode daya laptop berganti dari Silent ke Turbo 19 Nov ±23.08 (GPU dari 24 W ke ±85 W). Ini hanya mengubah
   kecepatan, bukan keluaran model.

Tidak ada butir lain yang berubah.

**21 November 2026 — lengan eksploratif "dokumentasi API" untuk Llama-3.1-8B (diminta pengguna 21 Nov: "Go").**
Diputuskan **sesudah** hasil tiga model diketahui (`Hasil_AgenEKG_8.md`), karena itu eksploratif: tidak masuk
perbandingan model di bagian 8 dan tidak dipakai untuk klaim utama. Ditulis sebelum lengan ini dijalankan.
Disetujui pengguna 21 Nov 2026 ("Jalan").

1. Pertanyaan: bila agen diberi ringkasan API pustaka yang terpasang, berapa banyak kegagalan antarmuka pustaka
   yang hilang (bacaan eksploratif `Hasil_AgenEKG_8.md`: 389 dari 495 run Llama diawali ImportError pada fungsi
   NeuroKit2 yang tidak ada; di transkrip tidak ada satu pun `dir()`/`help()` pada pustaka), dan apakah itu
   menambah besaran dalam toleransi.
2. Satu-satunya perubahan: system prompt ditambah isi `agenekg_api_ringkas.txt` (md5 `019e5d81…`), dibangkitkan
   `agenekg_api_ringkas.py` di dalam kontainer `agenekg-py:1` dari tanda tangan dan docstring pustaka yang terpasang
   (11 fungsi: `wfdb.rdrecord`, `wfdb.rdheader`, `nk.ecg_clean`, `ecg_peaks`, `ecg_delineate`, `ecg_rate`,
   `hrv_time`, `hrv_frequency`, `intervals_to_peaks`, `scipy.signal.find_peaks`, `welch`; atribut `Record`;
   kalimat "Call only functions listed here, or check a name with dir() or help() before using it."). Dijalankan
   lewat `agenekg_agen_api.py`, yang menambahkan teks itu ke `SISTEM`; `agenekg_agen.py` tidak diubah (md5
   `0a751ebb…`). Tugas, model dan kuantisasi, konteks 16.384, `--parallel 1`, 10 giliran, suhu bawaan,
   kontainer, dan penilaian sama dengan run utama.
3. Ulangan 1 saja dari 99 tugas (99 run), didahului pilot 5 tugas pilot; `Riset/EKG/jalan_llama_api.ps1`,
   keluaran `C:\Data\AgenEKG_runs\api_llama31_8b`. Puncak token Llama di run utama 9.105; ringkasan ±2.000 token,
   jadi tetap di bawah 16.384.
4. Pembanding: ulangan 1 run utama Llama pada 99 tugas yang sama (berpasangan per tugas). Ukuran, ditetapkan
   sekarang: (a) proporsi run yang eksekusi gagal pertamanya AttributeError/TypeError/ImportError/
   ModuleNotFoundError dari wfdb atau NeuroKit2, dan proporsi run yang eksekusi gagal pertamanya ImportError apa
   pun; (b) proporsi kode E1; (c) besaran inti dalam toleransi (QT, HRV, inti); (d) laju jalan-tapi-salah dan laju
   menyerah. Uji: permutasi berpasangan sign-flip (10.000) pada proporsi per tugas untuk (c), dilaporkan sebagai
   eksploratif tanpa koreksi. Tidak ada klaim konfirmatori.
5. Yang diakui sejak awal: ringkasan memilih fungsi (NeuroKit2 dan scipy) dan dengan itu bisa mengarahkan metode
   agen; ini bagian dari intervensi dan dinyatakan di naskah. Satu ulangan dipilih karena kelima ulangan run utama
   sepakat pada kegagalan (bagian 3.6 naskah); variasi antarulangan lengan ini tidak diukur.

Tidak ada butir lain yang berubah.

**21 November 2026 — lengan "dokumentasi API" diperluas ke Qwen2.5-Coder-7B dan -3B (diminta pengguna 21 Nov:
"go").** Diputuskan **sesudah** hasil lengan Llama diketahui (`Hasil_AgenEKG_9.md`: ImportError pertama 80 → 3,
besaran inti benar 4/373 di kedua lengan). Tujuannya menguji apakah pola itu khas Llama. Ditulis sebelum run.

1. Rancangan, ringkasan API (md5 `019e5d81…`), kerangka (`agenekg_agen_api.py`), ukuran (a)–(d), uji, dan
   pembanding (ulangan 1 run utama model yang sama, berpasangan per tugas) sama persis dengan penyimpangan Llama di
   atas. Tidak ada perubahan prompt atau ringkasan sesudah hasil Llama.
2. Kedua model dimuat dengan konteks 16.384 dan `--parallel 1` (`Riset/EKG/jalan_api_qwen.ps1`): 7B dulu, lalu
   3B; tiap model didahului pilot 5 tugas. Run utama 3B dulu memakai dua percakapan sejajar dengan jatah 16.384
   masing-masing; jatah per percakapan sama. Puncak token run utama 8.228 (7B) dan 10.009 (3B); ringkasan ±2.000
   token, jadi tetap di bawah 16.384.
3. Keluaran `C:\Data\AgenEKG_runs\api_qwen25coder7b` dan `api_qwen25coder3b`; pembanding
   `utama_qwen25coder7b_u1` dan `utama_qwen25coder3b_u1` (salinan berkas `*_u1.json`).
4. Tiga lengan API (satu per model) dilaporkan bersama sebagai eksploratif; tidak ada klaim konfirmatori, tidak
   ada koreksi uji berganda.

Disetujui pengguna 21 Nov 2026 ("go").

Tidak ada butir lain yang berubah.

**21 November 2026 — kode ulang 10 % oleh LLM, bukan oleh pengguna (diminta pengguna: "anda tulis aja").**
Bagian 7 menulis "10 % sampel dikode ulang pengguna". Pengguna memutuskan tidak mengode sendiri. Ditulis sebelum
kode ulang dijalankan.

1. Sampel tetap 145 tugas-ulangan yang ditarik `agenekg_analisis.py --sampel-kode-ulang` (benih 20261108); tidak
   ditarik ulang.
2. Bahan tersamar dari `agenekg_kode_ulang_bahan.py`: ID acak R001–R145 (benih 20261109), tanpa nama model dan
   tanpa kode otomatis; definisi E1–E8 di kepala bahan.
3. Pengode: dua sub-agen Claude Opus 5.5 (Anthropic) dalam konteks baru, masing-masing separuh ID, hanya boleh
   membaca `bahan.md`; tidak melihat `kunci.json`, sampel, skrip penilai, atau transkrip mentah. Asisten utama
   sudah melihat sebagian sampel dan sebaran kode otomatis, jadi tidak mengode sendiri.
4. Ukuran: persentase sepakat dan kappa Cohen, semua baris dan di luar E1 otomatis
   (`agenekg_kode_ulang_nilai.py`). Naskah menyebut pengodenya LLM, bukan penulis.
5. Tambahan sesudah hasil kode ulang diketahui (pengguna memilih, 21 Nov): pengguna menengahi tiga
   ketidaksepakatan dengan melihat kedua kode (R007 E5, R097 E4, R124 E5; `Hasil_AgenEKG_11.md`). Kesepakatan
   tersamar tetap dilaporkan sebagai ukuran utama; penengahan dilaporkan terpisah.

Tidak ada butir lain yang berubah.
