# Kotak pasir eksekusi kode agen AgenEKG: tanpa jaringan saat dijalankan (--network none).
FROM python:3.12-slim
RUN pip install --no-cache-dir numpy==2.3.4 scipy==1.16.3 pandas==2.3.3 wfdb==4.3.1 neurokit2==0.3.0 \
 && useradd -m agen
USER agen
WORKDIR /work
