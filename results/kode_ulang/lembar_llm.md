# Kode ulang LLM (sub-agen tersamar), 21 Nov 2026

| ID | Kode | Alasan |
|---|---|---|
| R001 | E1 | Satu-satunya eksekusi gagal: AttributeError record.annotations; tidak ada keluar 0 |
| R002 | E1 | Sembilan giliran semua keluar 1 (ValueError truth value of array) |
| R003 | E1 | Sembilan giliran gagal (ImportError, AttributeError wfdb, TypeError, FileNotFoundError) |
| R004 | E1 | Semua giliran keluar 1 (record.p_signals, NameError ecg, kanal string) |
| R005 | E1 | Semua eksekusi SyntaxError (recording.d Signals); tidak ada keluar 0 |
| R006 | E1 | Satu eksekusi gagal: TypeError nama kanal string di rdrecord |
| R007 | E3 | Keluar 0; QT = selisih sampel ×1000, RR = sampel/1000 (asumsi 1000 Hz, rekaman 250 Hz) |
| R008 | E1 | Satu eksekusi gagal: wfdb.processing tidak ada |
| R009 | E1 | Sembilan giliran gagal (AttributeError ecg_find_peaks, TypeError signal_smooth); tanpa FINAL |
| R010 | E1 | Semua giliran keluar 1; FINAL nol tanpa eksekusi sukses |
| R011 | E1 | Satu eksekusi gagal: TypeError indeks tuple 'Rpeaks' dari nk.ecg_peaks |
| R012 | E1 | Semua eksekusi gagal (ImportError ecg_qtc, rdsamp diindeks string) |
| R013 | E1 | Semua eksekusi gagal (FileNotFoundError .atr, record.annotations) |
| R014 | E1 | Sembilan giliran ImportError neurokit2; tidak ada keluar 0 |
| R015 | E2 | Giliran 4 keluar 0, tetapi FINAL "unanswerable: too few R peaks" pada tugas QT yang bisa dijawab |
| R016 | E1 | Semua eksekusi keluar 1; FINAL nol tidak berasal dari kode yang jalan |
| R017 | E1 | Semua eksekusi gagal; tanpa FINAL |
| R018 | E1 | Satu eksekusi gagal: wfdb.read_record tidak ada |
| R019 | E1 | Satu eksekusi gagal: neurokit2.peak_detection tidak ada |
| R020 | E1 | Sembilan giliran keluar 1; FINAL semua nol |
| R021 | E1 | Tiga eksekusi semua keluar 1; FINAL unanswerable |
| R022 | E4 | Tugas tak terjawab (jendela di luar rekaman) dijawab angka qt/qtcb/qtcf = 0 dari giliran 9 keluar 0 |
| R023 | E1 | Satu eksekusi gagal; FINAL unanswerable soal __array__ |
| R024 | E1 | Satu eksekusi gagal; FINAL mengklaim NeuroKit tak terpasang |
| R025 | E5 | Keluar 0; QT dihitung sebagai selisih amplitudo sinyal, bukan waktu antar batas gelombang (QT 1,87) |
| R026 | E2 | FINAL memuat NaN untuk LF/HF/LF-HF; juga sampel ×1000 tanpa fs (salah satuan) |
| R027 | E2 | Tanpa FINAL; giliran 4 mencetak unanswerable, giliran 7 keluaran kosong |
| R028 | E1 | Semua eksekusi keluar 1; FINAL HR 75 dan sisanya None |
| R029 | E1 | Satu eksekusi gagal: nn_interval tidak ada di neurokit2 |
| R030 | E1 | Sepuluh giliran semua keluar 1; tanpa FINAL |
| R031 | E1 | Semua eksekusi keluar 1; FINAL nol |
| R032 | E2 | Giliran 6 keluar 0 tetapi FINAL qt_ms = nan (bukan angka), QTc 0 |
| R033 | E1 | Sembilan giliran keluar 1; FINAL angka karangan (HR 60, nol) |
| R034 | E1 | Enam eksekusi gagal; FINAL unanswerable |
| R035 | E1 | Satu eksekusi gagal; FINAL salah klaim kanal ECG tidak ada |
| R036 | E1 | Satu eksekusi gagal (SyntaxError) |
| R037 | E1 | Semua eksekusi keluar 1; FINAL semua None |
| R038 | E1 | Sembilan giliran keluar 1; FINAL nol |
| R039 | E1 | Satu eksekusi gagal; ecg_delineate dicari di wfdb |
| R040 | E1 | Semua eksekusi keluar 1 (berkas tidak ditemukan) |
| R041 | E1 | Sepuluh giliran keluar 1; tanpa FINAL |
| R042 | E2 | Giliran 6 keluar 0 mencetak nilai, tetapi tidak ada FINAL objek JSON |
| R043 | E1 | Sembilan giliran keluar 1 (syntax error); FINAL unanswerable |
| R044 | E2 | Giliran 7 keluar 0 tetapi FINAL hr_bpm, LF, HF, LF/HF = NaN |
| R045 | E1 | Semua eksekusi keluar 1; FINAL angka nol/NaN tanpa kode sukses |
| R046 | E1 | Semua eksekusi keluar 1 (impor neurokit2 gagal) |
| R047 | E1 | Sepuluh giliran keluar 1; tanpa FINAL |
| R048 | E1 | Satu eksekusi gagal (nama berkas/kanal) |
| R049 | E1 | Sepuluh giliran keluar 1; tanpa FINAL |
| R050 | E1 | Empat eksekusi keluar 1; FINAL klaim butuh jaringan |
| R051 | E1 | Satu eksekusi gagal; FINAL unanswerable soal anotasi |
| R052 | E1 | Satu eksekusi gagal; FINAL klaim neurokit2 tak terpasang |
| R053 | E1 | Semua eksekusi keluar 1; FINAL HR 75 dan nol |
| R054 | E1 | Tiga eksekusi keluar 1; FINAL nol |
| R055 | E2 | Beberapa giliran keluar 0 (mean of empty slice) tetapi tidak ada FINAL |
| R056 | E2 | Giliran 10 keluar 0 dengan keluaran kosong; tidak ada FINAL |
| R057 | E1 | Satu eksekusi gagal (atribut record) |
| R058 | E1 | Satu eksekusi gagal; neurokit2 tidak diimpor |
| R059 | E1 | Semua eksekusi keluar 1; FINAL semua None |
| R060 | E1 | Satu eksekusi gagal (sintaks Python tidak sah) |
| R061 | E1 | Satu eksekusi gagal: wfdb.process_record tidak ada |
| R062 | E2 | Giliran 9 keluar 0 "No signal found"; FINAL semua None |
| R063 | E1 | Satu eksekusi gagal; FINAL klaim wfdb tak terpasang |
| R064 | E1 | Satu eksekusi gagal; metode multilead tidak didukung ecg_process |
| R065 | E1 | Satu eksekusi gagal: wfdb.read_record tidak ada |
| R066 | E1 | Satu eksekusi gagal: wfdb.rdrec tidak ada |
| R067 | E1 | Sepuluh giliran keluar 1; tanpa FINAL |
| R068 | E1 | Tiga eksekusi keluar 1 (atribut info) |
| R069 | E1 | Satu eksekusi gagal; rpeak_detection tidak ada |
| R070 | E2 | Giliran 1 keluar 0 tetapi FINAL unanswerable (tak ada R) pada tugas QT yang bisa dijawab |
| R071 | E1 | Semua eksekusi keluar 1; FINAL nol |
| R072 | E1 | Dua eksekusi keluar 1; tanpa FINAL |
| R073 | E2 | Giliran 5 keluar 0 tetapi FINAL unanswerable (R kurang) pada tugas HRV yang bisa dijawab |
| R074 | E1 | All 9 executed turns exit 1 (wfdb/neurokit2 attribute and key errors); none exit 0 |
| R075 | E2 | Turn 4 exits 0 but no FINAL given |
| R076 | E1 | All turns exit 1 with the same SyntaxError on print(FINAL: ...) |
| R077 | E1 | All executed turns exit 1 (wfdb.ecg_findpeaks, find_peaks import/name errors) |
| R078 | E2 | Turn 5 exits 0; FINAL holds "<calculated value>" placeholders, not numbers |
| R079 | E1 | Only turn exits 1: wfdb.read_record AttributeError |
| R080 | E1 | Turns 1 and 3 exit 1; no exit-0 run |
| R081 | E1 | All turns exit 1 (ImportError, FileNotFound, SyntaxError); zeros FINAL never computed |
| R082 | E1 | All turns exit 1 (neurokit2 ImportErrors, rdrecord unpack TypeErrors) |
| R083 | E2 | Turns 2-3 exit 0, yet FINAL says unanswerable on an answerable rate-trap task |
| R084 | E1 | All turns exit 1; FINAL all None |
| R085 | E1 | All turns exit 1 on p_signal AttributeErrors |
| R086 | E1 | All executed turns exit 1 (wfdb annotation AttributeErrors) |
| R087 | E2 | Turns 3-10 exit 0 (nan warnings) but no FINAL given |
| R088 | E1 | Single turn exits 1: Record has no attribute 'ecg' |
| R089 | E1 | All turns exit 1 on nonexistent wfdb peak functions |
| R090 | E1 | Single turn exits 1: wfdb.processing missing |
| R091 | E1 | Single turn exits 1: string channel name passed to rdrecord |
| R092 | E1 | Both turns exit 1 with neurokit2 ImportErrors |
| R093 | E1 | All executed turns exit 1; zeros FINAL not from a run |
| R094 | E1 | Single turn exits 1: wfdb.io.read_record missing |
| R095 | E1 | All executed turns exit 1; zeros FINAL not from a run |
| R096 | E1 | All turns exit 1 (wfdb.ecg_findpeaks, heartpy missing) |
| R097 | E4 | Exit 0, but sample window applied to channel axis, no beats selected; outputs zeros |
| R098 | E1 | Single turn exits 1: wfdb.ecg_findpeaks missing |
| R099 | E1 | Single turn exits 1: neurokit2 time_domain ImportError |
| R100 | E1 | All executed turns exit 1; zeros FINAL not from a run |
| R101 | E1 | All turns exit 1 (ImportError, prose pasted as code) |
| R102 | E1 | All executed turns exit 1 (wfdb/neurokit2 import and TypeErrors) |
| R103 | E2 | Turns 7-8 exit 0 but FINAL unanswerable (missing .atr) on answerable QT task |
| R104 | E1 | Single turn exits 1: Record has no findpeaks |
| R105 | E1 | All turns exit 1 (read_record, then NameError 'true') |
| R106 | E1 | Single turn exits 1: wfdb.read_record missing |
| R107 | E1 | Executed turns exit 1: neurokit2 not imported (NameError) |
| R108 | E1 | All turns exit 1 with SyntaxError on FINAL placeholder line |
| R109 | E5 | Exit 0; QT bounds assumed fixed (R-50, R+200 samples), no delineation; zeros output |
| R110 | E1 | All turns exit 1 (channel str TypeError, then NameError 'true') |
| R111 | E1 | All executed turns exit 1; numeric FINAL not from a successful run |
| R112 | E1 | All turns exit 1 (SyntaxError, wfdb.processing missing) |
| R113 | E1 | All executed turns exit 1 (neurokit2 ImportErrors); FINAL None |
| R114 | E1 | Single turn exits 1: wfdb.io.read_record missing |
| R115 | E1 | All executed turns exit 1; FINAL None |
| R116 | E1 | Executed turns exit 1 (nonmax_suppression, NameError 'true') |
| R117 | E1 | All executed turns exit 1 (annsamp AttributeError, FileNotFound) |
| R118 | E1 | Single turn exits 1: np not defined |
| R119 | E1 | Single turn exits 1: ecg_findpeaks method 'default' not implemented |
| R120 | E1 | All executed turns exit 1 (imports, rdrecord kwargs, findpeaks kwargs) |
| R121 | E1 | Single turn exits 1: wfdb.process_record missing |
| R122 | E2 | Exit-0 runs exist; FINAL gives no qt/qtc numbers, only no_beats_in_window flag |
| R123 | E2 | Turn 4 exits 0; FINAL qt_ms is null, not a number |
| R124 | E3 | Exit 0; RR left in samples labelled seconds, fs never used, /1000 then *1000; qt 0.96 |
| R125 | E1 | Single turn exits 1: tuple has no attribute 'ppg' |
| R126 | E1 | All executed turns exit 1; zeros FINAL not from a run |
| R127 | E1 | All turns exit 1 (imports, rdrecord kwargs, Record attributes) |
| R128 | E1 | Single turn exits 1: sel52.atr not found |
| R129 | E2 | Turns 6 and 9 exit 0 but no FINAL given |
| R130 | E1 | All turns exit 1 (read_record, then NameError 'true') |
| R131 | E1 | All executed turns exit 1; FINAL not from a run |
| R132 | E1 | Single turn exits 1: cannot import rpeaks from neurokit2 |
| R133 | E1 | All executed turns exit 1 (ImportErrors, .hea.hea FileNotFound) |
| R134 | E2 | Turns 3,5,7,9 exit 0 with empty output; no FINAL given |
| R135 | E1 | Single turn exits 1: wfdb.processing missing |
| R136 | E1 | All executed turns exit 1; -1/0 FINAL not from a run |
| R137 | E1 | All turns exit 1 (ImportError nn, NameError 'true') |
| R138 | E1 | Single turn exits 1: string channel passed to rdrecord |
| R139 | E2 | Turn 8 exits 0 but FINAL unanswerable on answerable HRV task |
| R140 | E2 | Turn 9 exits 0; FINAL has nan for lf_ms2, hf_ms2, lf_hf (not numbers, invalid JSON) |
| R141 | E1 | All turns exit 1 (channel str TypeError, NameError 'true') |
| R142 | E1 | All turns exit 1 (sampto AttributeError, NameError, SyntaxError) |
| R143 | E1 | All executed turns exit 1 with neurokit2 ImportErrors |
| R144 | E1 | All turns exit 1 (KeyError 'RR', NameError 'true') |
| R145 | E1 | All executed turns exit 1 (wfdb attributes, sel39.atr not found) |
