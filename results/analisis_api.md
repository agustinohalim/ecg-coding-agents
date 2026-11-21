## 1. Besaran dalam toleransi (CI 95 % bootstrap bergugus rekaman, 2.000 kali)

| Model | Jenis | Tugas-ulangan | Besaran benar | CI 95 % | Toleransi ketat | Toleransi longgar |
|---|---|---|---|---|---|---|
| api_llama8b | qt | 45 | 0/135 (0.0 %) | 0.0–0.0 % | 0/135 (0.0 %) | 1/135 (0.7 %) |
| api_llama8b | hrv | 34 | 4/238 (1.7 %) | 0.0–3.8 % | 2/238 (0.8 %) | 8/238 (3.4 %) |
| api_llama8b | jebakan_ektopik | 6 | 0/18 (0.0 %) | 0.0–0.0 % | 0/18 (0.0 %) | 0/18 (0.0 %) |
| api_llama8b | jebakan_laju | 5 | 0/15 (0.0 %) | 0.0–0.0 % | 0/15 (0.0 %) | 0/15 (0.0 %) |
| api_llama8b | jebakan_kanal | 4 | 0/12 (0.0 %) | 0.0–0.0 % | 0/12 (0.0 %) | 0/12 (0.0 %) |
| api_llama8b | jebakan_takterjawab | 5 | 1/5 (20.0 %) | 0.0–60.0 % | – | – |
| api_llama8b | inti (QT + HRV) | 79 | 4/373 (1.1 %) | 0.0–2.6 % | 2/373 (0.5 %) | 9/373 (2.4 %) |
| utama_llama8b_u1 | qt | 45 | 0/135 (0.0 %) | 0.0–0.0 % | 0/135 (0.0 %) | 1/135 (0.7 %) |
| utama_llama8b_u1 | hrv | 34 | 4/238 (1.7 %) | 0.4–3.4 % | 4/238 (1.7 %) | 6/238 (2.5 %) |
| utama_llama8b_u1 | jebakan_ektopik | 6 | 1/18 (5.6 %) | 0.0–16.7 % | 1/18 (5.6 %) | 1/18 (5.6 %) |
| utama_llama8b_u1 | jebakan_laju | 5 | 0/15 (0.0 %) | 0.0–0.0 % | 0/15 (0.0 %) | 0/15 (0.0 %) |
| utama_llama8b_u1 | jebakan_kanal | 4 | 0/12 (0.0 %) | 0.0–0.0 % | 0/12 (0.0 %) | 0/12 (0.0 %) |
| utama_llama8b_u1 | jebakan_takterjawab | 5 | 1/5 (20.0 %) | 0.0–60.0 % | – | – |
| utama_llama8b_u1 | inti (QT + HRV) | 79 | 4/373 (1.1 %) | 0.3–2.2 % | 4/373 (1.1 %) | 7/373 (1.9 %) |

## 2. Tugas-ulangan: seluruhnya benar, jalan-tapi-salah, menyerah

| Model | Jenis | Tugas-ulangan | Seluruhnya benar | Kode pernah jalan | Jalan-tapi-salah | Menyerah |
|---|---|---|---|---|---|---|
| api_llama8b | qt | 45 | 0/45 (0.0 %) | 13/45 (28.9 %) | 4/45 (8.9 %) | 15/45 (33.3 %) |
| api_llama8b | hrv | 34 | 0/34 (0.0 %) | 9/34 (26.5 %) | 3/34 (8.8 %) | 15/34 (44.1 %) |
| api_llama8b | jebakan_ektopik | 6 | 0/6 (0.0 %) | 0/6 (0.0 %) | 0/6 (0.0 %) | 1/6 (16.7 %) |
| api_llama8b | jebakan_laju | 5 | 0/5 (0.0 %) | 3/5 (60.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) |
| api_llama8b | jebakan_kanal | 4 | 0/4 (0.0 %) | 2/4 (50.0 %) | 0/4 (0.0 %) | 1/4 (25.0 %) |
| api_llama8b | jebakan_takterjawab | 5 | 1/5 (20.0 %) | 3/5 (60.0 %) | 0/5 (0.0 %) | 1/5 (20.0 %) |
| utama_llama8b_u1 | qt | 45 | 0/45 (0.0 %) | 6/45 (13.3 %) | 0/45 (0.0 %) | 3/45 (6.7 %) |
| utama_llama8b_u1 | hrv | 34 | 0/34 (0.0 %) | 3/34 (8.8 %) | 1/34 (2.9 %) | 15/34 (44.1 %) |
| utama_llama8b_u1 | jebakan_ektopik | 6 | 0/6 (0.0 %) | 0/6 (0.0 %) | 0/6 (0.0 %) | 1/6 (16.7 %) |
| utama_llama8b_u1 | jebakan_laju | 5 | 0/5 (0.0 %) | 3/5 (60.0 %) | 2/5 (40.0 %) | 1/5 (20.0 %) |
| utama_llama8b_u1 | jebakan_kanal | 4 | 0/4 (0.0 %) | 3/4 (75.0 %) | 1/4 (25.0 %) | 0/4 (0.0 %) |
| utama_llama8b_u1 | jebakan_takterjawab | 5 | 1/5 (20.0 %) | 0/5 (0.0 %) | 0/5 (0.0 %) | 1/5 (20.0 %) |

## 3. Taksonomi galat (kode pertama yang cocok, E1 -> E8)

| Model | Jenis | Gagal | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
|---|---|---|---|---|---|---|---|---|---|---|
| api_llama8b | qt | 45 | 32 | 9 | 0 | 0 | 4 | 0 | 0 | 0 |
| api_llama8b | hrv | 34 | 25 | 6 | 0 | 1 | 2 | 0 | 0 | 0 |
| api_llama8b | jebakan_ektopik | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_llama8b | jebakan_laju | 5 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_llama8b | jebakan_kanal | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| api_llama8b | jebakan_takterjawab | 4 | 1 | 1 | 0 | 2 | 0 | 0 | 0 | 0 |
| api_llama8b | semua | 98 | 68 | 21 | 0 | 3 | 6 | 0 | 0 | 0 |
| utama_llama8b_u1 | qt | 45 | 39 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_llama8b_u1 | hrv | 34 | 31 | 2 | 0 | 1 | 0 | 0 | 0 | 0 |
| utama_llama8b_u1 | jebakan_ektopik | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_llama8b_u1 | jebakan_laju | 5 | 2 | 1 | 0 | 1 | 1 | 0 | 0 | 0 |
| utama_llama8b_u1 | jebakan_kanal | 4 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| utama_llama8b_u1 | jebakan_takterjawab | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| utama_llama8b_u1 | semua | 98 | 83 | 11 | 0 | 2 | 2 | 0 | 0 | 0 |

Subjenis E2/E4/E8:

- api_llama8b: E2 FINAL rusak: 10; E2 besaran bukan angka: 5; E2 menyerah: 5; E4 tak terjawab dijawab angka: 2; E4 kanal: 1; E2 tanpa FINAL: 1
- utama_llama8b_u1: E2 FINAL rusak: 6; E2 besaran bukan angka: 4; E4 kanal: 2; E2 menyerah: 1

## 4. Eksploratif: galat eksekusi pertama yang gagal (semua tugas-ulangan)

- api_llama8b: API pustaka (TypeError) 63; ValueError 8; TypeError 7; NameError 6; FileNotFoundError 4; lain 3; API pustaka (ImportError) 3; SyntaxError 2
- utama_llama8b_u1: API pustaka (ImportError) 80; SyntaxError 8; API pustaka (TypeError) 3; tidak ada eksekusi gagal 3; AttributeError 2; FileNotFoundError 2; NameError 1

## 5. Kesepakatan antar-ulangan

| Model | Jenis | Tugas | Kelima ulangan sama (seluruhnya benar atau tidak) | Tugas dengan >= 1 ulangan benar |
|---|---|---|---|---|
| api_llama8b | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| api_llama8b | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| api_llama8b | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| api_llama8b | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| api_llama8b | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| api_llama8b | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 1/5 (20.0 %) |
| utama_llama8b_u1 | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| utama_llama8b_u1 | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| utama_llama8b_u1 | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| utama_llama8b_u1 | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| utama_llama8b_u1 | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| utama_llama8b_u1 | jebakan_takterjawab | 5 | 5/5 (100.0 %) | 1/5 (20.0 %) |

## 6. Uji permutasi berpasangan per tugas (tukar tanda, 10.000 kali, dua sisi)

| Jenis | Model A | Model B | Beda rata-rata proporsi (A − B) | p | Tugas |
|---|---|---|---|---|---|
| qt | api_llama8b | utama_llama8b_u1 | +0.000 | 1.0000 | 45 |
| hrv | api_llama8b | utama_llama8b_u1 | +0.000 | 1.0000 | 34 |
