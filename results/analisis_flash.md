## 1. Besaran dalam toleransi (CI 95 % bootstrap bergugus rekaman, 2.000 kali)

| Model | Jenis | Tugas-ulangan | Besaran benar | CI 95 % | Toleransi ketat | Toleransi longgar |
|---|---|---|---|---|---|---|
| flash | qt | 225 | 319/675 (47.3 %) | 39.9–54.8 % | 182/675 (27.0 %) | 444/675 (65.8 %) |
| flash | hrv | 170 | 829/1190 (69.7 %) | 64.5–74.3 % | 766/1190 (64.4 %) | 961/1190 (80.8 %) |
| flash | jebakan_ektopik | 30 | 44/90 (48.9 %) | 44.4–54.4 % | 38/90 (42.2 %) | 47/90 (52.2 %) |
| flash | jebakan_laju | 25 | 69/75 (92.0 %) | 81.3–100.0 % | 68/75 (90.7 %) | 72/75 (96.0 %) |
| flash | jebakan_kanal | 20 | 54/60 (90.0 %) | 70.0–100.0 % | 50/60 (83.3 %) | 54/60 (90.0 %) |
| flash | jebakan_takterjawab | 25 | 6/25 (24.0 %) | 4.0–44.0 % | – | – |
| flash | inti (QT + HRV) | 395 | 1148/1865 (61.6 %) | 56.5–65.9 % | 948/1865 (50.8 %) | 1405/1865 (75.3 %) |
| qwen7b | qt | 225 | 0/675 (0.0 %) | 0.0–0.0 % | 0/675 (0.0 %) | 0/675 (0.0 %) |
| qwen7b | hrv | 170 | 2/1190 (0.2 %) | 0.0–0.5 % | 2/1190 (0.2 %) | 5/1190 (0.4 %) |
| qwen7b | jebakan_ektopik | 30 | 0/90 (0.0 %) | 0.0–0.0 % | 0/90 (0.0 %) | 0/90 (0.0 %) |
| qwen7b | jebakan_laju | 25 | 0/75 (0.0 %) | 0.0–0.0 % | 0/75 (0.0 %) | 0/75 (0.0 %) |
| qwen7b | jebakan_kanal | 20 | 0/60 (0.0 %) | 0.0–0.0 % | 0/60 (0.0 %) | 0/60 (0.0 %) |
| qwen7b | jebakan_takterjawab | 25 | 17/25 (68.0 %) | 52.0–88.0 % | – | – |
| qwen7b | inti (QT + HRV) | 395 | 2/1865 (0.1 %) | 0.0–0.3 % | 2/1865 (0.1 %) | 5/1865 (0.3 %) |
| qwen3b | qt | 225 | 0/675 (0.0 %) | 0.0–0.0 % | 0/675 (0.0 %) | 0/675 (0.0 %) |
| qwen3b | hrv | 170 | 2/1190 (0.2 %) | 0.0–0.4 % | 2/1190 (0.2 %) | 2/1190 (0.2 %) |
| qwen3b | jebakan_ektopik | 30 | 0/90 (0.0 %) | 0.0–0.0 % | 0/90 (0.0 %) | 0/90 (0.0 %) |
| qwen3b | jebakan_laju | 25 | 0/75 (0.0 %) | 0.0–0.0 % | 0/75 (0.0 %) | 0/75 (0.0 %) |
| qwen3b | jebakan_kanal | 20 | 0/60 (0.0 %) | 0.0–0.0 % | 0/60 (0.0 %) | 0/60 (0.0 %) |
| qwen3b | jebakan_takterjawab | 25 | 17/25 (68.0 %) | 52.0–80.0 % | – | – |
| qwen3b | inti (QT + HRV) | 395 | 2/1865 (0.1 %) | 0.0–0.3 % | 2/1865 (0.1 %) | 2/1865 (0.1 %) |
| llama8b | qt | 225 | 1/675 (0.1 %) | 0.0–0.6 % | 1/675 (0.1 %) | 3/675 (0.4 %) |
| llama8b | hrv | 170 | 30/1190 (2.5 %) | 1.6–3.6 % | 24/1190 (2.0 %) | 41/1190 (3.4 %) |
| llama8b | jebakan_ektopik | 30 | 1/90 (1.1 %) | 0.0–3.3 % | 1/90 (1.1 %) | 2/90 (2.2 %) |
| llama8b | jebakan_laju | 25 | 1/75 (1.3 %) | 0.0–4.0 % | 1/75 (1.3 %) | 2/75 (2.7 %) |
| llama8b | jebakan_kanal | 20 | 0/60 (0.0 %) | 0.0–0.0 % | 0/60 (0.0 %) | 0/60 (0.0 %) |
| llama8b | jebakan_takterjawab | 25 | 6/25 (24.0 %) | 12.0–36.0 % | – | – |
| llama8b | inti (QT + HRV) | 395 | 31/1865 (1.7 %) | 1.0–2.4 % | 25/1865 (1.3 %) | 44/1865 (2.4 %) |

## 2. Tugas-ulangan: seluruhnya benar, jalan-tapi-salah, menyerah

| Model | Jenis | Tugas-ulangan | Seluruhnya benar | Kode pernah jalan | Jalan-tapi-salah | Menyerah |
|---|---|---|---|---|---|---|
| flash | qt | 225 | 98/225 (43.6 %) | 225/225 (100.0 %) | 124/225 (55.1 %) | 0/225 (0.0 %) |
| flash | hrv | 170 | 36/170 (21.2 %) | 170/170 (100.0 %) | 131/170 (77.1 %) | 0/170 (0.0 %) |
| flash | jebakan_ektopik | 30 | 3/30 (10.0 %) | 30/30 (100.0 %) | 26/30 (86.7 %) | 0/30 (0.0 %) |
| flash | jebakan_laju | 25 | 21/25 (84.0 %) | 25/25 (100.0 %) | 4/25 (16.0 %) | 0/25 (0.0 %) |
| flash | jebakan_kanal | 20 | 17/20 (85.0 %) | 20/20 (100.0 %) | 3/20 (15.0 %) | 0/20 (0.0 %) |
| flash | jebakan_takterjawab | 25 | 6/25 (24.0 %) | 25/25 (100.0 %) | 0/25 (0.0 %) | 6/25 (24.0 %) |
| qwen7b | qt | 225 | 0/225 (0.0 %) | 14/225 (6.2 %) | 4/225 (1.8 %) | 190/225 (84.4 %) |
| qwen7b | hrv | 170 | 0/170 (0.0 %) | 16/170 (9.4 %) | 2/170 (1.2 %) | 138/170 (81.2 %) |
| qwen7b | jebakan_ektopik | 30 | 0/30 (0.0 %) | 5/30 (16.7 %) | 0/30 (0.0 %) | 22/30 (73.3 %) |
| qwen7b | jebakan_laju | 25 | 0/25 (0.0 %) | 4/25 (16.0 %) | 0/25 (0.0 %) | 20/25 (80.0 %) |
| qwen7b | jebakan_kanal | 20 | 0/20 (0.0 %) | 5/20 (25.0 %) | 1/20 (5.0 %) | 16/20 (80.0 %) |
| qwen7b | jebakan_takterjawab | 25 | 17/25 (68.0 %) | 3/25 (12.0 %) | 0/25 (0.0 %) | 17/25 (68.0 %) |
| qwen3b | qt | 225 | 0/225 (0.0 %) | 47/225 (20.9 %) | 6/225 (2.7 %) | 175/225 (77.8 %) |
| qwen3b | hrv | 170 | 0/170 (0.0 %) | 27/170 (15.9 %) | 2/170 (1.2 %) | 121/170 (71.2 %) |
| qwen3b | jebakan_ektopik | 30 | 0/30 (0.0 %) | 7/30 (23.3 %) | 0/30 (0.0 %) | 22/30 (73.3 %) |
| qwen3b | jebakan_laju | 25 | 0/25 (0.0 %) | 5/25 (20.0 %) | 0/25 (0.0 %) | 21/25 (84.0 %) |
| qwen3b | jebakan_kanal | 20 | 0/20 (0.0 %) | 5/20 (25.0 %) | 1/20 (5.0 %) | 14/20 (70.0 %) |
| qwen3b | jebakan_takterjawab | 25 | 17/25 (68.0 %) | 2/25 (8.0 %) | 0/25 (0.0 %) | 17/25 (68.0 %) |
| llama8b | qt | 225 | 0/225 (0.0 %) | 62/225 (27.6 %) | 28/225 (12.4 %) | 24/225 (10.7 %) |
| llama8b | hrv | 170 | 0/170 (0.0 %) | 31/170 (18.2 %) | 10/170 (5.9 %) | 65/170 (38.2 %) |
| llama8b | jebakan_ektopik | 30 | 0/30 (0.0 %) | 7/30 (23.3 %) | 5/30 (16.7 %) | 6/30 (20.0 %) |
| llama8b | jebakan_laju | 25 | 0/25 (0.0 %) | 9/25 (36.0 %) | 5/25 (20.0 %) | 3/25 (12.0 %) |
| llama8b | jebakan_kanal | 20 | 0/20 (0.0 %) | 9/20 (45.0 %) | 6/20 (30.0 %) | 1/20 (5.0 %) |
| llama8b | jebakan_takterjawab | 25 | 6/25 (24.0 %) | 5/25 (20.0 %) | 0/25 (0.0 %) | 6/25 (24.0 %) |

## 3. Taksonomi galat (kode pertama yang cocok, E1 -> E8)

| Model | Jenis | Gagal | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
|---|---|---|---|---|---|---|---|---|---|---|
| flash | qt | 127 | 0 | 3 | 0 | 13 | 111 | 0 | 0 | 0 |
| flash | hrv | 134 | 0 | 3 | 0 | 8 | 1 | 0 | 3 | 119 |
| flash | jebakan_ektopik | 27 | 0 | 1 | 0 | 6 | 0 | 4 | 0 | 16 |
| flash | jebakan_laju | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 3 |
| flash | jebakan_kanal | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| flash | jebakan_takterjawab | 19 | 0 | 0 | 0 | 19 | 0 | 0 | 0 | 0 |
| flash | semua | 314 | 0 | 7 | 0 | 46 | 113 | 4 | 3 | 141 |
| qwen7b | qt | 225 | 211 | 10 | 0 | 0 | 4 | 0 | 0 | 0 |
| qwen7b | hrv | 170 | 154 | 14 | 0 | 1 | 1 | 0 | 0 | 0 |
| qwen7b | jebakan_ektopik | 30 | 25 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen7b | jebakan_laju | 25 | 21 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen7b | jebakan_kanal | 20 | 15 | 4 | 0 | 0 | 1 | 0 | 0 | 0 |
| qwen7b | jebakan_takterjawab | 8 | 6 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen7b | semua | 478 | 432 | 39 | 0 | 1 | 6 | 0 | 0 | 0 |
| qwen3b | qt | 225 | 178 | 41 | 0 | 0 | 6 | 0 | 0 | 0 |
| qwen3b | hrv | 170 | 143 | 25 | 1 | 1 | 0 | 0 | 0 | 0 |
| qwen3b | jebakan_ektopik | 30 | 23 | 7 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3b | jebakan_laju | 25 | 20 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| qwen3b | jebakan_kanal | 20 | 15 | 4 | 0 | 1 | 0 | 0 | 0 | 0 |
| qwen3b | jebakan_takterjawab | 8 | 7 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| qwen3b | semua | 478 | 386 | 82 | 1 | 3 | 6 | 0 | 0 | 0 |
| llama8b | qt | 225 | 163 | 34 | 0 | 0 | 28 | 0 | 0 | 0 |
| llama8b | hrv | 170 | 139 | 21 | 2 | 6 | 2 | 0 | 0 | 0 |
| llama8b | jebakan_ektopik | 30 | 23 | 2 | 0 | 4 | 1 | 0 | 0 | 0 |
| llama8b | jebakan_laju | 25 | 16 | 4 | 1 | 3 | 1 | 0 | 0 | 0 |
| llama8b | jebakan_kanal | 20 | 11 | 3 | 0 | 2 | 4 | 0 | 0 | 0 |
| llama8b | jebakan_takterjawab | 19 | 15 | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| llama8b | semua | 489 | 367 | 66 | 3 | 17 | 36 | 0 | 0 | 0 |

Subjenis E2/E4/E8:

- flash: E8 hf_ms2,lf_hf: 50; E4 jendela: 26; E4 tak terjawab dijawab angka: 19; E8 hf_ms2: 14; E8 lf_hf: 9; E8 rmssd_nn_ms,sdnn_nn_ms: 9; E8 hf_ms2,lf_hf,lf_ms2,rmssd_ms,sdnn_ms: 8; E2 tanpa FINAL: 7; E8 hf_ms2,lf_hf,lf_ms2,pnn50_pct,rmssd_ms,sdnn_ms: 5; E8 rmssd_nn_ms: 5; E8 lf_hf,lf_ms2: 4; E8 rmssd_ms,sdnn_ms: 4; E8 rmssd_ms: 3; E8 hf_ms2,lf_ms2: 3; E8 hf_ms2,lf_hf,rmssd_ms,sdnn_ms: 3; E8 hf_ms2,lf_ms2,rmssd_ms,sdnn_ms: 2; E8 hf_ms2,lf_hf,lf_ms2: 2; E8 hf_ms2,lf_hf,lf_ms2,rmssd_ms: 2; E8 lf_ms2: 2; E8 sdnn_nn_ms: 2; E8 hf_ms2,lf_hf,rmssd_ms: 1; E8 hf_ms2,lf_hf,lf_ms2,pnn50_pct,rmssd_ms: 1; E8 hf_ms2,lf_hf,lf_ms2,pnn50_pct,sdnn_ms: 1; E8 hf_ms2,lf_ms2,pnn50_pct,rmssd_ms,sdnn_ms: 1; E8 lf_hf,pnn50_pct: 1; E8 lf_hf,lf_ms2,rmssd_ms,sdnn_ms: 1; E8 pnn50_pct: 1; E8 hf_ms2,lf_hf,pnn50_pct,rmssd_ms: 1; E8 lf_hf,pnn50_pct,rmssd_ms,sdnn_ms: 1; E8 hf_ms2,pnn50_pct,rmssd_ms: 1; E8 hf_ms2,rmssd_ms: 1; E8 hf_ms2,lf_ms2,pnn50_pct: 1; E8 hf_ms2,lf_hf,lf_ms2,sdnn_ms: 1; E4 kanal: 1; E8 sdnn_ms: 1
- qwen7b: E2 menyerah: 22; E2 tanpa FINAL: 13; E2 FINAL rusak: 3; E4 kanal: 1; E2 besaran bukan angka: 1
- qwen3b: E2 menyerah: 52; E2 tanpa FINAL: 20; E2 besaran bukan angka: 6; E2 FINAL rusak: 4; E4 kanal: 2; E4 tak terjawab dijawab angka: 1
- llama8b: E2 FINAL rusak: 35; E2 besaran bukan angka: 21; E4 kanal: 14; E2 menyerah: 7; E2 tanpa FINAL: 3; E4 tak terjawab dijawab angka: 2; E4 jendela: 1

## 4. Eksploratif: galat eksekusi pertama yang gagal (semua tugas-ulangan)

- flash: tidak ada eksekusi gagal 251; API pustaka (TypeError) 45; AttributeError 44; ValueError 41; NameError 27; FileNotFoundError 20; API pustaka (AttributeError) 19; KeyError 15
- qwen7b: API pustaka (AttributeError) 186; API pustaka (TypeError) 72; SyntaxError 62; API pustaka (ImportError) 47; AttributeError 45; NameError 23; FileNotFoundError 20; TypeError 18
- qwen3b: AttributeError 129; API pustaka (AttributeError) 95; NameError 66; SyntaxError 51; ValueError 33; API pustaka (ImportError) 28; IndexError 25; tidak ada eksekusi gagal 24
- llama8b: API pustaka (ImportError) 389; SyntaxError 51; API pustaka (TypeError) 17; FileNotFoundError 11; tidak ada eksekusi gagal 11; API pustaka (AttributeError) 8; AttributeError 3; API pustaka (ModuleNotFoundError) 3

## 5. Kesepakatan antar-ulangan

| Model | Jenis | Tugas | Kelima ulangan sama (seluruhnya benar atau tidak) | Tugas dengan >= 1 ulangan benar |
|---|---|---|---|---|
| flash | qt | 45 | 8/45 (17.8 %) | 39/45 (86.7 %) |
| flash | hrv | 34 | 11/34 (32.4 %) | 23/34 (67.6 %) |
| flash | jebakan_ektopik | 6 | 4/6 (66.7 %) | 2/6 (33.3 %) |
| flash | jebakan_laju | 5 | 3/5 (60.0 %) | 5/5 (100.0 %) |
| flash | jebakan_kanal | 4 | 3/4 (75.0 %) | 4/4 (100.0 %) |
| flash | jebakan_takterjawab | 5 | 2/5 (40.0 %) | 3/5 (60.0 %) |
| qwen7b | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| qwen7b | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| qwen7b | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| qwen7b | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| qwen7b | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| qwen7b | jebakan_takterjawab | 5 | 1/5 (20.0 %) | 5/5 (100.0 %) |
| qwen3b | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| qwen3b | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| qwen3b | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| qwen3b | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| qwen3b | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| qwen3b | jebakan_takterjawab | 5 | 0/5 (0.0 %) | 5/5 (100.0 %) |
| llama8b | qt | 45 | 45/45 (100.0 %) | 0/45 (0.0 %) |
| llama8b | hrv | 34 | 34/34 (100.0 %) | 0/34 (0.0 %) |
| llama8b | jebakan_ektopik | 6 | 6/6 (100.0 %) | 0/6 (0.0 %) |
| llama8b | jebakan_laju | 5 | 5/5 (100.0 %) | 0/5 (0.0 %) |
| llama8b | jebakan_kanal | 4 | 4/4 (100.0 %) | 0/4 (0.0 %) |
| llama8b | jebakan_takterjawab | 5 | 1/5 (20.0 %) | 4/5 (80.0 %) |

## 6. Uji permutasi berpasangan per tugas (tukar tanda, 10.000 kali, dua sisi)

| Jenis | Model A | Model B | Beda rata-rata proporsi (A − B) | p | Tugas |
|---|---|---|---|---|---|
| qt | flash | qwen7b | +0.473 | 0.0001 | 45 |
| qt | flash | qwen3b | +0.473 | 0.0001 | 45 |
| qt | flash | llama8b | +0.471 | 0.0001 | 45 |
| qt | qwen7b | qwen3b | +0.000 | 1.0000 | 45 |
| qt | qwen7b | llama8b | -0.001 | 1.0000 | 45 |
| qt | qwen3b | llama8b | -0.001 | 1.0000 | 45 |
| hrv | flash | qwen7b | +0.695 | 0.0001 | 34 |
| hrv | flash | qwen3b | +0.695 | 0.0001 | 34 |
| hrv | flash | llama8b | +0.671 | 0.0001 | 34 |
| hrv | qwen7b | qwen3b | +0.000 | 1.0000 | 34 |
| hrv | qwen7b | llama8b | -0.024 | 0.0003 | 34 |
| hrv | qwen3b | llama8b | -0.024 | 0.0003 | 34 |
