"""Lengan eksploratif "dokumentasi API" AgenEKG (Prareg_AgenEKG.md, penyimpangan 21 Nov 2026).

Kerangka agen yang sama dengan `agenekg_agen.py`, dengan satu beda: system prompt ditambah ringkasan API
`agenekg_api_ringkas.txt` (dibangkitkan `agenekg_api_ringkas.py` di dalam kontainer). Argumen sama:

    python -X utf8 Riset/EKG/agenekg_agen_api.py --tugas Riset/EKG/agenekg_tugas.json --model <id> \
        --ulang-ke 1 --keluar C:/Data/AgenEKG_runs/api_<nama>
"""
from pathlib import Path

import agenekg_agen

RINGKASAN_API = Path(__file__).with_name("agenekg_api_ringkas.txt")


def main():
    agenekg_agen.SISTEM = agenekg_agen.SISTEM + "\n\n" + RINGKASAN_API.read_text(encoding="utf-8")
    agenekg_agen.main()


if __name__ == "__main__":
    main()
