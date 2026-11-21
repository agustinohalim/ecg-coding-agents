## 1. Besaran dalam toleransi (CI 95 % bootstrap bergugus rekaman, 2.000 kali)

| Model | Jenis | Tugas-ulangan | Besaran benar | CI 95 % | Toleransi ketat | Toleransi longgar |
|---|---|---|---|---|---|---|
| api_qwen7b | qt | 45 | 0/135 (0.0 %) | 0.0–0.0 % | 0/135 (0.0 %) | 0/135 (0.0 %) |
| api_qwen7b | hrv | 34 | 0/238 (0.0 %) | 0.0–0.0 % | 0/238 (0.0 %) | 0/238 (0.0 %) |
| api_qwen7b | jebakan_ektopik | 6 | 0/18 (0.0 %) | 0.0–0.0 % | 0/18 (0.0 %) | 0/18 (0.0 %) |
| api_qwen7b | jebakan_laju | 5 | 0/15 (0.0 %) | 0.0–0.0 % | 0/15 (0.0 %) | 0/15 (0.0 %) |
| api_qwen7b | jebakan_kanal | 4 | 0/12 (0.0 %) | 0.0–0.0 % | 0/12 (0.0 %) | 0/12 (0.0 %) |
| api_qwen7b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 100.0–100.0 % | – | – |
| api_qwen7b | inti (QT + HRV) | 79 | 0/373 (0.0 %) | 0.0–0.0 % | 0/373 (0.0 %) | 0/373 (0.0 %) |
| utama_qwen7b_u1 | qt | 45 | 0/135 (0.0 %) | 0.0–0.0 % | 0/135 (0.0 %) | 0/135 (0.0 %) |
| utama_qwen7b_u1 | hrv | 34 | 0/238 (0.0 %) | 0.0–0.0 % | 0/238 (0.0 %) | 0/238 (0.0 %) |
| utama_qwen7b_u1 | jebakan_ektopik | 6 | 0/18 (0.0 %) | 0.0–0.0 % | 0/18 (0.0 %) | 0/18 (0.0 %) |
| utama_qwen7b_u1 | jebakan_laju | 5 | 0/15 (0.0 %) | 0.0–0.0 % | 0/15 (0.0 %) | 0/15 (0.0 %) |
| utama_qwen7b_u1 | jebakan_kanal | 4 | 0/12 (0.0 %) | 0.0–0.0 % | 0/12 (0.0 %) | 0/12 (0.0 %) |
| utama_qwen7b_u1 | jebakan_takterjawab | 5 | 4/5 (80.0 %) | 40.0–100.0 % | – | – |
| utama_qwen7b_u1 | inti (QT + HRV) | 79 | 0/373 (0.0 %) | 0.0–0.0 % | 0/373 (0.0 %) | 0/373 (0.0 %) |

## 2. Tugas-ulangan: seluruhnya benar, jalan-tapi-salah, menyerah

| Model | Jenis | Tugas-ulangan | Seluruhnya benar | Kode pernah jalan | Jalan-tapi-salah | Menyerah |
|---|---|---|---|---|---|---|
| api_qwen7b | qt | 45 | 0/45 (0.0 %) | 2/45 (4.4 %) | 0/45 (0.0 %) | 31/45 (68.9 %) |
| api_qwen7b | hrv | 34 | 0/34 (0.0 %) | 2/34 (5.9 %) | 0/34 (0.0 %) | 29/34 (85.3 %) |
| api_qwen7b | jebakan_ektopik | 6 | 0/6 (0.0 %) | 0/6 (0.0 %) | 0/6 (0.0 %) | 6/6 (100.0 %) |
| api_qwen7b | jebakan_laju | 5 | 0/5 (0.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) | 3/5 (60.0 %) |
| api_qwen7b | jebakan_kanal | 4 | 0/4 (0.0 %) | 0/4 (0.0 %) | 0/4 (0.0 %) | 3/4 (75.0 %) |
| api_qwen7b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 1/5 (20.0 %) | 0/5 (0.0 %) | 5/5 (100.0 %) |
| utama_qwen7b_u1 | qt | 45 | 0/45 (0.0 %) | 3/45 (6.7 %) | 1/45 (2.2 %) | 39/45 (86.7 %) |
| utama_qwen7b_u1 | hrv | 34 | 0/34 (0.0 %) | 0/34 (0.0 %) | 0/34 (0.0 %) | 28/34 (82.4 %) |
| utama_qwen7b_u1 | jebakan_ektopik | 6 | 0/6 (0.0 %) | 0/6 (0.0 %) | 0/6 (0.0 %) | 5/6 (83.3 %) |
| utama_qwen7b_u1 | jebakan_laju | 5 | 0/5 (0.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) | 3/5 (60.0 %) |
| utama_qwen7b_u1 | jebakan_kanal | 4 | 0/4 (0.0 %) | 1/4 (25.0 %) | 0/4 (0.0 %) | 2/4 (50.0 %) |
| utama_qwen7b_u1 | jebakan_takterjawab | 5 | 4/5 (80.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) | 4/5 (80.0 %) |

## 3. Taksonomi galat (kode pertama yang cocok, E1 -> E8)

| Model | Jenis | Gagal | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
|---|---|---|---|---|---|---|---|---|---|---|
| api_qwen7b | qt | 45 | 43 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen7b | hrv | 34 | 32 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen7b | jebakan_ektopik | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen7b | jebakan_laju | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen7b | jebakan_kanal | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_qwen7b | semua | 94 | 90 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen7b_u1 | qt | 45 | 42 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| utama_qwen7b_u1 | hrv | 34 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen7b_u1 | jebakan_ektopik | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen7b_u1 | jebakan_laju | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen7b_u1 | jebakan_kanal | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen7b_u1 | jebakan_takterjawab | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_qwen7b_u1 | semua | 95 | 91 | 3 | 0 | 0 | 1 | 0 | 0 | 0 |

Subjenis E2/E4/E8:

- api_qwen7b: E2 tanpa FINAL: 2; E2 menyerah: 1; E2 FINAL rusak: 1
- utama_qwen7b_u1: E2 tanpa FINAL: 1; E2 besaran bukan angka: 1; E2 menyerah: 1

## 4. Eksploratif: galat eksekusi pertama yang gagal (semua tugas-ulangan)

- api_qwen7b: API pustaka (TypeError) 50; ValueError 31; NameError 13; SyntaxError 3; TypeError 1; tidak ada eksekusi gagal 1
- utama_qwen7b_u1: API pustaka (AttributeError) 40; API pustaka (TypeError) 19; SyntaxError 10; API pustaka (ImportError) 8; NameError 6; AttributeError 5; FileNotFoundError 4; ValueError 4

## 5. Kesepakatan antar-ulangan

| Model | Jenis | Tugas | Kelima ulangan sama (seluruhnya benar atau tidak) | Tugas dengan >= 1 ulangan benar |
|---|---|---|---|---|
| api_qwen7b | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| api_qwen7b | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| api_qwen7b | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| api_qwen7b | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| api_qwen7b | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| api_qwen7b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 5/5 (100.0 %) |
| utama_qwen7b_u1 | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| utama_qwen7b_u1 | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| utama_qwen7b_u1 | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| utama_qwen7b_u1 | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| utama_qwen7b_u1 | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| utama_qwen7b_u1 | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 4/5 (80.0 %) |

## 6. Uji permutasi berpasangan per tugas (tukar tanda, 10.000 kali, dua sisi)

| Jenis | Model A | Model B | Beda rata-rata proporsi (A − B) | p | Tugas |
|---|---|---|---|---|---|
| qt | api_qwen7b | utama_qwen7b_u1 | +0.000 | 1.0000 | 45 |
| hrv | api_qwen7b | utama_qwen7b_u1 | +0.000 | 1.0000 | 34 |
