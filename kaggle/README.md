# Sharing on Kaggle / Kaggle'da paylaşım

The notebooks in this folder are the Colab notebooks adapted for Kaggle: the file-upload step is replaced by a cell that finds `train_FDxxx.txt`, `test_FDxxx.txt` and `RUL_FDxxx.txt` under `/kaggle/input` and copies them to the working directory. Everything else is unchanged. (Notebook text is Turkish.)

## Steps

1. On Kaggle: **Create → New Notebook → File → Import Notebook**, and upload e.g. `NASA_RUL_FD001_Solution_Kaggle.ipynb`.
2. In the right panel choose **Add Input** and search for a NASA C-MAPSS dataset (e.g. `nasa-cmaps`, which contains `CMaps/train_FD001.txt` and the other files). The cell finds the files wherever they are, so the folder layout does not matter.
3. **Run All**, check there are no errors, then **Save Version → Save & Run All (Commit)**.
4. In the notebook's **Share** settings make it Public, and fill in the title, subtitle, description and tags below.

Tip: publish `FD001_Solution` first as the main notebook, then add the other three as follow-ups, or publish all four.

## Suggested post text

**Title:** RUL Prediction on NASA C-MAPSS (FD001–FD004) with Linear Regression and Random Forest

**Subtitle:** Entry-level predictive maintenance: no pipelines, step-by-step, NASA score and maintenance alarm included

**Description:**

Predicts how many cycles a turbofan engine has left before failure (RUL) from sensor data, using plain pandas and scikit-learn. Steps: drop constant sensors, compute RUL, cap it at 125, MinMax-scale (fit on train only), train Linear Regression and Random Forest, evaluate with RMSE / MAE / R² and the NASA score, plus a bonus "fails within 30 cycles?" classifier and an alarm-threshold analysis.

Random Forest test RMSE: FD001 17.18, FD002 18.82, FD003 20.18, FD004 20.82. Capping RUL at 125 gave the biggest single improvement. Linear Regression beats Random Forest on the NASA score for FD002–FD004 even though its RMSE is worse, so "best model" depends on the metric. Limits: single seed, single split, no cross-validation; the NASA score uses capped RUL and is not comparable with published scores. Notebook text is in Turkish.

**Tags:** predictive maintenance, regression, random forest, time series, aerospace, beginner

**Data attribution:** A. Saxena and K. Goebel (2008). Turbofan Engine Degradation Simulation Data Set, NASA Ames Prognostics Data Repository.

---

## Türkçe özet

Bu klasördeki defterler Colab defterlerinin Kaggle uyarlamasıdır. Veri yükleme adımı, `/kaggle/input` altında üç dosyayı bulup çalışma klasörüne kopyalayan bir hücreyle değiştirildi. Kaggle'da: Create → New Notebook → File → Import Notebook ile defteri yükle, **Add Input** ile NASA C-MAPSS veri setini ekle, Run All ile çalıştır, **Save Version** ile kaydet ve notebook'u Public yap.
