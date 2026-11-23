# ecg-coding-agents

Code, task set, references, and aggregate results for the manuscript *Four Coding Agents Measuring QT and
HRV Against Expert Annotations: Better Than a Constant Answer for HRV, Not for QT* (in preparation). The study asks whether code written by language-model coding agents returns
QT, corrected QT, and frequency-domain heart-rate variability (HRV) values within pre-specified tolerances of
references derived from expert annotations.

Three open-weight models run locally (Qwen2.5-Coder-7B-Instruct, Qwen2.5-Coder-3B-Instruct,
Llama-3.1-8B-Instruct; 4-bit GGUF, served by LM Studio 0.4.28) and one commercial model (DeepSeek-V4-flash,
through an OpenAI-compatible gateway) run 99 tasks five times each; the agent's code runs in a network-free
Docker container. A fixed NeuroKit2 pipeline without a language model is the baseline, and an exploratory arm
adds a short reference of the installed library functions to the system prompt of the three local models.

**No PhysioNet data are included.** The three databases are open (Open Data Commons Attribution 1.0) and are
downloaded from PhysioNet: QT Database 1.0.0, Fantasia 1.0.0, and the MIT-BIH Arrhythmia Database. The
reference values in `analysis/agenekg_rujukan*.json` are derived from their annotations. Every agent and
baseline transcript used in the manuscript is in `transcripts/` (one JSON file per task run); they contain the
agents' code and its output, not the recordings.

## Layout

| Path | Contents |
|---|---|
| `docker/Dockerfile` | Execution container `agenekg-py:1`: Python 3.12, numpy 2.3.4, scipy 1.16.3, pandas 2.3.3, wfdb 4.3.1, neurokit2 0.3.0 |
| `analysis/agenekg_rujukan_qt.py` | QT, QTcB, and QTcF references from the manual `.q1c` annotations; inter-annotator spread from `.q2c` |
| `analysis/agenekg_rujukan_hrv.py` | HRV references from the Fantasia beat annotations (window rule, Welch reference, NeuroKit2 second implementation) |
| `analysis/agenekg_tugas.py`, `agenekg_tugas_pilot.py` | Generate the 99 main tasks and 5 pilot tasks (seed 20261107), the derived trap recordings, and the reference file |
| `analysis/agenekg_tugas.json`, `agenekg_rujukan.json` | The frozen task list (what the agent sees) and the references with tolerances (never copied into the sandbox) |
| `analysis/agenekg_agen.py` | Agent harness: one Python block per turn, run in the container, ten turns, `FINAL: {json}` |
| `analysis/agenekg_agen_api.py`, `agenekg_api_ringkas.py`, `agenekg_api_ringkas.txt` | API-documentation arm: the same harness with the library reference appended to the system prompt; the generator runs inside the container |
| `analysis/agenekg_dasar_nk.py` | Library-only NeuroKit2 baseline (DWT, peak, CWT delineation) |
| `analysis/agenekg_analisis.py`, `analysis/penilaian/` | Scoring against the references (`skor`), error taxonomy E1–E8 (`taksonomi`), bootstrap CIs clustered by record and paired sign-flip permutation tests (`statistik`), and the printed report (`laporan`) |
| `analysis/agenekg_nilai.py` | Per-quantity scoring table for one run folder (used for the pilot) |
| `analysis/agenekg_kode_ulang_bahan.py`, `agenekg_kode_ulang_nilai.py` | Blinded recoding material for the 10 % sample, and agreement (Cohen's kappa) with the automatic codes |
| `results/` | Outputs of `agenekg_analisis.py`: main runs of the local models (`analisis_utama`), the four models together (`analisis_flash`), DeepSeek-V4-flash against the three baseline methods (`analisis_flash_vs_nk`), baseline (`analisis_dasar_nk`), API-documentation arm per model (`analisis_api*`) |
| `results/kode_ulang/` | The 145-run sample, the key, the blind LLM recoding with reasons, the codes after the author's adjudication, and both agreement reports |
| `transcripts/` | One zip per run: `main_*` (four models, 495 task runs each), `baseline_nk_*` (94 answerable tasks per delineation method), `apidoc_*` (API-documentation arm, 99 per local model) |
| `registration/` | Redacted copy of the preregistration, and the confirmatory plan (see below) |
| `analysis/agenekg_cek_e1.py`, `agenekg_hrv_toleransi_tetap.py` | Post hoc: numbers answered in runs coded E1, and the HRV baseline comparison at a fixed 20 % frequency tolerance |
| `analysis/agenekg_tambahan_jiki.py` | Post hoc: constant-answer baseline (leave-one-out median), provenance of answered numbers, HRV split by domain |
| `analysis/agenekg_qt_lantai.py`, `agenekg_asal_ulang.py` | Post hoc: intervals for agent minus constant, per-task QT agreement, constant from records outside the tasks; provenance with unit and derived-value rules and a random-run control, spectral method in the HRV code |
| `analysis/agenekg_qt_per_run.py` | Post hoc: run-level QT agreement (Bland–Altman bias and limits of agreement, Spearman, Theil–Sen), constant and RR-model baselines |
| `analysis/agenekg_tugas_konfirmasi.py`, `agenekg_tugas_konfirmasi.json`, `agenekg_rujukan_konfirmasi.json`, `agenekg_konfirmasi_nilai.py` | Confirmatory QT test: the 31 held-out tasks and references, and the analysis fixed before the runs |
| `results/post_hoc/`, `results/confirmatory/` | Printed outputs of the post hoc scripts and of the confirmatory analysis; `audit_asal.md` is the reading of 30 unmatched QT numbers |
| `transcripts/confirm_*` | Confirmatory runs: DeepSeek-V4-flash, 31 tasks × 5 (155), and the NeuroKit2 DWT baseline on the same 31 tasks |

Identifiers, printed output, and log fields are in Indonesian (*tugas* = task, *rujukan* = reference, *nilai* =
score, *ulang* = repeat, *giliran* = turn, *jebakan* = trap, *menyerah* = gave up, *jalan-tapi-salah* = run but
wrong); docstrings and comments are in English.

**Scripts as run, and the tidied versions here.** The scripts were tidied for release on 22 November 2026, after
all analyses: comments and docstrings translated to English, and `agenekg_analisis.py` split into the
`penilaian/` package, with no change in what they compute. The versions that produced every result are in
commit `48c2fee` of this repository (the preregistration records their md5, e.g. `agenekg_agen.py`
`0a751ebb…`, `agenekg_analisis.py` `67dad0a3…`). The tidied scripts were checked against them: the scoring,
recoding, task, pilot, and QT-reference scripts reproduce the earlier outputs byte for byte (including every
file in `results/` and the frozen reference file; the frozen task file differs only in line endings), and the harness, baseline, API-summary, and
HRV-reference scripts differ only in docstrings, comments, and help text (identical syntax trees). The
in-container baseline script (`DALAM` in `agenekg_dasar_nk.py`) is unchanged.

## Reproducing

1. Download the three PhysioNet databases under one folder (default `C:/Data/PhysioNet`; every script takes
   `--data` or a folder argument).
2. Build the container: `docker build -t agenekg-py:1 docker`. Run the scripts from the repository root;
   `agenekg_analisis.py` finds `penilaian/` next to it.
3. References and tasks (already frozen in `analysis/`; regenerating them should give identical files):
   `python -X utf8 analysis/agenekg_rujukan_qt.py <qtdb folder>`, then `agenekg_rujukan_hrv.py` inside the
   container (see its docstring), then `python -I -X utf8 analysis/agenekg_tugas.py`.
4. Agent runs, with a model loaded in LM Studio (context 16,384 tokens):
   `python -X utf8 analysis/agenekg_agen.py --tugas analysis/agenekg_tugas.json --model <id> --ulang 5 --keluar <folder>`.
   The API-documentation arm uses `agenekg_agen_api.py` with `--ulang-ke 1`. For a hosted model add
   `--url <OpenAI-compatible endpoint> --kunci <environment variable holding the key>`; `--luar-puncak` waits
   out DeepSeek's peak-price hours. Existing `<task>_u<repeat>.json` files are skipped, so an interrupted run
   resumes where it stopped.
5. Baseline: `python -X utf8 analysis/agenekg_dasar_nk.py --metode dwt --keluar <folder>`.
6. Scoring: `python -X utf8 analysis/agenekg_analisis.py --run <name>=<folder> [--run ...] --json <file>`.
   To rescore without rerunning the agents, unzip `transcripts/` and pass the extracted folders, e.g.
   `--run flash=transcripts/main_deepseek-v4-flash --run qwen7b=transcripts/main_qwen25coder7b
   --run qwen3b=transcripts/main_qwen25coder3b --run llama8b=transcripts/main_llama31_8b`, which reproduces
   `results/analisis_flash.md`.

Model files and their SHA-256 hashes are listed in the manuscript's supplementary material (S3).

## Preregistration

The study was preregistered on 7 November 2026, before any main run (first commit of the registration file in
the author's private research repository: 7a6bca8, 2026-11-07); every later change is dated in the file and in
the manuscript (Section 3.9). `registration/Prareg_AgenEKG_disunting.md` is a public copy in Indonesian, as of
22 November 2026 (last change: commit f3d746a, the DeepSeek-V4-flash runs completed to 495), with one redaction:
the name of the third-party gateway used for the commercial runs (two lines in the 7 November deviation). The
unredacted file has md5 `6cd8e42d2c287aeed89cfcf149f8346c`; files it names (`Hasil_AgenEKG_*.md`,
`jalan_flash.ps1`) are internal notes and a launch script whose numbers and settings appear in the manuscript.

## Version 1.1.0: post hoc checks and the confirmatory QT test

Version 1.1.0 (23 November 2026) adds the scripts, outputs, and transcripts behind the exploratory checks made
after all results (manuscript Sections 3.7–3.9, 4.6, 4.8) and the confirmatory test (Sections 3.10, 4.7). The
post hoc scripts are released exactly as they were run (their md5 are recorded in the author's results notes, e.g.
`agenekg_qt_per_run.py` `3a0772a8…`), with English docstrings; the two scipy warning lines at the top of
`results/post_hoc/qt_lantai.txt`, which printed a local path, were removed. Each takes the `analysis/` folder and a
folder of unzipped transcripts, as in its docstring.

`registration/Prareg_AgenEKG_Konfirmasi.md` (Indonesian, unredacted, md5 `a2cab1c333b497d857f67aaddf13a186`) is
the confirmatory plan. It was committed in the private research repository (commit a694076, 2026-11-22 16:45 UTC+7)
together with `agenekg_tugas_konfirmasi.py` and `agenekg_konfirmasi_nilai.py`, before the 31 tasks were generated
and before any run; its three dated deviations (a memory stop, and gateway rejections with HTTP 413, one run
scored as no answer: `qt_sel31_u1.json` is a hand-written marker that says so) were committed before scoring
(a42798f, 98d14f6). Its hypotheses H1 and H2 were not supported and H3 was:

```
python -X utf8 analysis/agenekg_konfirmasi_nilai.py analysis transcripts/confirm_deepseek-v4-flash transcripts/confirm_baseline_nk_dwt
```

reproduces `results/confirmatory/konfirmasi.txt` after unzipping. The confirmatory tasks reuse the main task text and
rule, and can be regenerated with `python -I -X utf8 analysis/agenekg_tugas_konfirmasi.py`, which checks that the
seeded draw of the 45 main tasks is reproduced first.

## Licence

MIT (code). The derived reference values follow the PhysioNet databases' ODC-By 1.0 licence; cite the databases
and PhysioNet when reusing them.
