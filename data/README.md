# Data / Veri

**English** — Put the NASA C-MAPSS (Turbofan Engine Degradation Simulation) files in this folder. The raw data is not included in the repository.

**Source:** NASA Prognostics Data Repository, "Turbofan Engine Degradation Simulation" section.
Citation: A. Saxena and K. Goebel (2008). *Turbofan Engine Degradation Simulation Data Set*, NASA Ames Prognostics Data Repository, NASA Ames, Moffett Field, CA.

For each subset (FD001, FD002, FD003, FD004) three files are needed:

| File | Content |
|---|---|
| `train_FDxxx.txt` | Training engines, run until failure |
| `test_FDxxx.txt` | Test engines, cut before failure |
| `RUL_FDxxx.txt` | True remaining life of each test engine at its last cycle |

Each row has 26 columns: engine id, cycle, 3 operating settings, 21 sensors. Files are whitespace-separated with no header row.

---

**Türkçe** — NASA C-MAPSS (Turbofan Engine Degradation Simulation) dosyalarını bu klasöre koy. Ham veri depoya dahil değildir.

**Kaynak:** NASA Prognostics Data Repository, "Turbofan Engine Degradation Simulation" bölümü.
Atıf: A. Saxena ve K. Goebel (2008). *Turbofan Engine Degradation Simulation Data Set*, NASA Ames Prognostics Data Repository, NASA Ames, Moffett Field, CA.

Her alt veri seti için `train_FDxxx.txt`, `test_FDxxx.txt` ve `RUL_FDxxx.txt` dosyaları gerekir. Her satır 26 sütundur: motor numarası, çevrim, 3 çalışma ayarı, 21 sensör. Dosyalar boşlukla ayrılmıştır, başlık satırı yoktur.
