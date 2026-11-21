# ecg-coding-agents

Code, task set, references, and aggregate results for the manuscript ⬜ *(title pending)* (Halim, in
preparation). The study asks whether code written by small, locally run language-model agents returns QT,
corrected QT, and frequency-domain heart-rate variability (HRV) values within pre-specified tolerances of
references derived from expert annotations.

Three open-weight models (Qwen2.5-Coder-7B-Instruct, Qwen2.5-Coder-3B-Instruct, Llama-3.1-8B-Instruct; 4-bit
GGUF, served by LM Studio 0.4.28) run 99 tasks five times each in a network-free Docker container. A fixed
NeuroKit2 pipeline without a language model is the baseline, and an exploratory arm adds a short reference of the
installed library functions to the system prompt.

**No PhysioNet data are included.** The three databases are open (Open Data Commons Attribution 1.0) and are
downloaded from PhysioNet: QT Database 1.0.0, Fantasia 1.0.0, and the MIT-BIH Arrhythmia Database. The
reference values in `analysis/agenekg_rujukan*.json` are derived from their annotations. Agent transcripts are
archived separately ⬜ (Zenodo DOI).

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
| `analysis/agenekg_nilai.py`, `agenekg_analisis.py` | Scoring against the references, error taxonomy E1–E8, bootstrap CIs clustered by record, paired sign-flip permutation tests |
| `analysis/agenekg_kode_ulang_bahan.py`, `agenekg_kode_ulang_nilai.py` | Blinded recoding material for the 10 % sample, and agreement (Cohen's kappa) with the automatic codes |
| `results/` | Outputs of `agenekg_analisis.py`: main runs (`analisis_utama`), baseline (`analisis_dasar_nk`), API-documentation arm per model (`analisis_api*`) |
| `results/kode_ulang/` | The 145-run sample, the key, the blind LLM recoding with reasons, the codes after the author's adjudication, and both agreement reports |
| `registration/` | Redacted copy of the preregistration (see below) |

Comments, log text, and some identifiers are in Indonesian (*tugas* = task, *rujukan* = reference, *nilai* =
score, *ulang* = repeat, *giliran* = turn, *jebakan* = trap, *menyerah* = gave up, *jalan-tapi-salah* = run but
wrong).

## Reproducing

1. Download the three PhysioNet databases under one folder (default `C:/Data/PhysioNet`; every script takes
   `--data` or a folder argument).
2. Build the container: `docker build -t agenekg-py:1 docker`.
3. References and tasks (already frozen in `analysis/`; regenerating them should give identical files):
   `python -X utf8 analysis/agenekg_rujukan_qt.py <qtdb folder>`, then `agenekg_rujukan_hrv.py` inside the
   container (see its docstring), then `python -I -X utf8 analysis/agenekg_tugas.py`.
4. Agent runs, with a model loaded in LM Studio (context 16,384 tokens):
   `python -X utf8 analysis/agenekg_agen.py --tugas analysis/agenekg_tugas.json --model <id> --ulang 5 --keluar <folder>`.
   The API-documentation arm uses `agenekg_agen_api.py` with `--ulang-ke 1`.
5. Baseline: `python -X utf8 analysis/agenekg_dasar_nk.py --metode dwt --keluar <folder>`.
6. Scoring: `python -X utf8 analysis/agenekg_analisis.py --run <name>=<folder> [--run ...] --json <file>`.

Model files and their SHA-256 hashes are listed in the manuscript's supplementary material (S3).

## Preregistration

The study was preregistered on 7 November 2026, before any main run (first commit of the registration file in
the author's private research repository: 7a6bca8, 2026-11-07); every later change is dated in the file and in
the manuscript (Section 2.9). `registration/Prareg_AgenEKG_disunting.md` is a public copy in Indonesian, as of
21 November 2026, with one redaction: the name of the third-party gateway used for the commercial runs (two
lines in the 7 November deviation). The unredacted file has md5 `6729d7056f26b2089d4b0997489d621d`; files it
names (`Hasil_AgenEKG_*.md`) are internal result notes whose numbers appear in the manuscript.

## Licence

MIT (code). The derived reference values follow the PhysioNet databases' ODC-By 1.0 licence; cite the databases
and PhysioNet when reusing them.
