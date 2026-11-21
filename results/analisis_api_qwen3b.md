## 1. Besaran dalam toleransi (CI 95 % bootstrap bergugus rekaman, 2.000 kali)

| Model | Jenis | Tugas-ulangan | Besaran benar | CI 95 % | Toleransi ketat | Toleransi longgar |
|---|---|---|---|---|---|---|
| api_qwen3b | qt | 45 | 0/135 (0.0 %) | 0.0–0.0 % | 0/135 (0.0 %) | 0/135 (0.0 %) |
| api_qwen3b | hrv | 34 | 0/238 (0.0 %) | 0.0–0.0 % | 0/238 (0.0 %) | 0/238 (0.0 %) |
| api_qwen3b | jebakan_ektopik | 6 | 0/18 (0.0 %) | 0.0–0.0 % | 0/18 (0.0 %) | 0/18 (0.0 %) |
| api_qwen3b | jebakan_laju | 5 | 0/15 (0.0 %) | 0.0–0.0 % | 0/15 (0.0 %) | 1/15 (6.7 %) |
| api_qwen3b | jebakan_kanal | 4 | 0/12 (0.0 %) | 0.0–0.0 % | 0/12 (0.0 %) | 0/12 (0.0 %) |
| api_qwen3b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 100.0–100.0 % | – | – |
| api_qwen3b | inti (QT + HRV) | 79 | 0/373 (0.0 %) | 0.0–0.0 % | 0/373 (0.0 %) | 0/373 (0.0 %) |
| utama_qwen3b_u1 | qt | 45 | 0/135 (0.0 %) | 0.0–0.0 % | 0/135 (0.0 %) | 0/135 (0.0 %) |
| utama_qwen3b_u1 | hrv | 34 | 2/238 (0.8 %) | 0.0–2.1 % | 2/238 (0.8 %) | 2/238 (0.8 %) |
| utama_qwen3b_u1 | jebakan_ektopik | 6 | 0/18 (0.0 %) | 0.0–0.0 % | 0/18 (0.0 %) | 0/18 (0.0 %) |
| utama_qwen3b_u1 | jebakan_laju | 5 | 0/15 (0.0 %) | 0.0–0.0 % | 0/15 (0.0 %) | 0/15 (0.0 %) |
| utama_qwen3b_u1 | jebakan_kanal | 4 | 0/12 (0.0 %) | 0.0–0.0 % | 0/12 (0.0 %) | 0/12 (0.0 %) |
| utama_qwen3b_u1 | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 100.0–100.0 % | – | – |
| utama_qwen3b_u1 | inti (QT + HRV) | 79 | 2/373 (0.5 %) | 0.0–1.3 % | 2/373 (0.5 %) | 2/373 (0.5 %) |

## 2. Tugas-ulangan: seluruhnya benar, jalan-tapi-salah, menyerah

| Model | Jenis | Tugas-ulangan | Seluruhnya benar | Kode pernah jalan | Jalan-tapi-salah | Menyerah |
|---|---|---|---|---|---|---|
| api_qwen3b | qt | 45 | 0/45 (0.0 %) | 6/45 (13.3 %) | 0/45 (0.0 %) | 30/45 (66.7 %) |
| api_qwen3b | hrv | 34 | 0/34 (0.0 %) | 2/34 (5.9 %) | 0/34 (0.0 %) | 28/34 (82.4 %) |
| api_qwen3b | jebakan_ektopik | 6 | 0/6 (0.0 %) | 0/6 (0.0 %) | 0/6 (0.0 %) | 5/6 (83.3 %) |
| api_qwen3b | jebakan_laju | 5 | 0/5 (0.0 %) | 1/5 (20.0 %) | 1/5 (20.0 %) | 1/5 (20.0 %) |
| api_qwen3b | jebakan_kanal | 4 | 0/4 (0.0 %) | 0/4 (0.0 %) | 0/4 (0.0 %) | 4/4 (100.0 %) |
| api_qwen3b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) | 5/5 (100.0 %) |
| utama_qwen3b_u1 | qt | 45 | 0/45 (0.0 %) | 7/45 (15.6 %) | 0/45 (0.0 %) | 33/45 (73.3 %) |
| utama_qwen3b_u1 | hrv | 34 | 0/34 (0.0 %) | 11/34 (32.4 %) | 2/34 (5.9 %) | 24/34 (70.6 %) |
| utama_qwen3b_u1 | jebakan_ektopik | 6 | 0/6 (0.0 %) | 2/6 (33.3 %) | 0/6 (0.0 %) | 3/6 (50.0 %) |
| utama_qwen3b_u1 | jebakan_laju | 5 | 0/5 (0.0 %) | 2/5 (40.0 %) | 0/5 (0.0 %) | 5/5 (100.0 %) |
| utama_qwen3b_u1 | jebakan_kanal | 4 | 0/4 (0.0 %) | 0/4 (0.0 %) | 0/4 (0.0 %) | 4/4 (100.0 %) |
| utama_qwen3b_u1 | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) | 5/5 (100.0 %) |

## 3. Taksonomi galat (kode pertama yang cocok, E1 -> E8)

| Model | Jenis | Gagal | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
|---|---|---|---|---|---|---|---|---|---|---|
| api_qwen3b | qt | 45 | 39 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen3b | hrv | 34 | 32 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen3b | jebakan_ektopik | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen3b | jebakan_laju | 5 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| api_qwen3b | jebakan_kanal | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen3b | semua | 94 | 85 | 8 | 0 | 1 | 0 | 0 | 0 | 0 |
| utama_qwen3b_u1 | qt | 45 | 38 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen3b_u1 | hrv | 34 | 23 | 9 | 1 | 1 | 0 | 0 | 0 | 0 |
| utama_qwen3b_u1 | jebakan_ektopik | 6 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen3b_u1 | jebakan_laju | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen3b_u1 | jebakan_kanal | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen3b_u1 | semua | 94 | 72 | 20 | 1 | 1 | 0 | 0 | 0 | 0 |

Subjenis E2/E4/E8:

- api_qwen3b: E2 menyerah: 4; E2 tanpa FINAL: 2; E2 FINAL rusak: 2; E4 kanal: 1
- utama_qwen3b_u1: E2 menyerah: 12; E2 tanpa FINAL: 4; E2 FINAL rusak: 3; E2 besaran bukan angka: 1; E4 kanal: 1

## 4. Eksploratif: galat eksekusi pertama yang gagal (semua tugas-ulangan)

- api_qwen3b: API pustaka (TypeError) 27; ValueError 21; NameError 18; SyntaxError 10; TypeError 5; IndexError 4; API pustaka (ModuleNotFoundError) 3; KeyError 3
- utama_qwen3b_u1: AttributeError 30; API pustaka (AttributeError) 24; NameError 12; ValueError 8; tidak ada eksekusi gagal 7; IndexError 5; SyntaxError 5; API pustaka (ImportError) 2

## 5. Kesepakatan antar-ulangan

| Model | Jenis | Tugas | Kelima ulangan sama (seluruhnya benar atau tidak) | Tugas dengan >= 1 ulangan benar |
|---|---|---|---|---|
| api_qwen3b | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| api_qwen3b | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| api_qwen3b | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| api_qwen3b | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| api_qwen3b | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| api_qwen3b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 5/5 (100.0 %) |
| utama_qwen3b_u1 | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| utama_qwen3b_u1 | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| utama_qwen3b_u1 | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| utama_qwen3b_u1 | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| utama_qwen3b_u1 | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| utama_qwen3b_u1 | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 5/5 (100.0 %) |

## 6. Uji permutasi berpasangan per tugas (tukar tanda, 10.000 kali, dua sisi)

| Jenis | Model A | Model B | Beda rata-rata proporsi (A − B) | p | Tugas |
|---|---|---|---|---|---|
| qt | api_qwen3b | utama_qwen3b_u1 | +0.000 | 1.0000 | 45 |
| hrv | api_qwen3b | utama_qwen3b_u1 | -0.008 | 0.4973 | 34 |
