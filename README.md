Remaining Useful Life (RUL) Prediction for NASA Turbofan Engines

English · Türkçe

A data analysis / machine learning project that predicts, from sensor readings, how many cycles an aircraft engine has left before failure (RUL, Remaining Useful Life), using plain Python and scikit-learn. The four subsets of NASA's C-MAPSS dataset (FD001–FD004) were analysed separately. Built as a graduation project.

The goal was not an advanced model. It was to keep every step explainable, reproducible and readable at an entry-level analyst's skill: no pipelines, one step per notebook cell.

Language note: the notebooks, report and slides are written in Turkish. This README, data/README.md and kaggle/README.md are available in English.

Interactive pages

If you enable GitHub Pages from the docs/ folder (Settings → Pages → Branch: main, Folder: /docs):

docs/index.html: all nine notebook charts, interactive (four datasets, hover values, alarm-threshold slider)
docs/demo.html: web demo (precomputed Random Forest predictions, maintenance warning, selectable sensor charts)
What was done
Files were read and given column names.
Constant columns were dropped (standard deviation < 0.01): 10 / 1 / 9 / 1 columns for FD001 / FD002 / FD003 / FD004.
On the training set, RUL = engine's last cycle − current cycle, then capped at 125.
Sensors were scaled with MinMaxScaler (fitted on the training set only, so no data leakage).
Linear Regression (baseline) and Random Forest (n_estimators=100, max_depth=10, random_state=42) were trained.
RMSE, MAE, R² and the NASA score were computed.
Bonus: a logistic-regression classifier for "will the engine fail within 30 cycles?" and a maintenance alarm threshold analysis (30 / 40 / 50).
A live demo (Gradio) and interactive charts.

On the test set only each engine's last row is evaluated, because the true RUL in RUL_FDxxx.txt is given only for that moment.

Results

Test set, with RUL capped at 125.

Dataset	Conditions / fault modes	RF RMSE	RF MAE	RF R²	LR RMSE (capped)	LR RMSE (uncapped)
FD001	1 / 1	17.18	12.18	0.82	20.82	31.95
FD002	6 / 1	18.82	14.28	0.81	21.30	33.94
FD003	1 / 2	20.18	14.86	0.73	20.48	57.32
FD004	6 / 2	20.82	15.31	0.77	24.55	47.77
Random Forest has the lowest RMSE on all four datasets; on FD003 its edge over Linear Regression is tiny (20.18 vs 20.48).
Capping RUL at 125 was the single biggest improvement. The test ground truth is capped as well, so that comparison is not strictly like-for-like.
NASA score (lower is better, Linear Regression / Random Forest): FD001 1251 / 898, FD002 2802 / 3584, FD003 1242 / 1710, FD004 4591 / 5240. Although Random Forest has the better RMSE, Linear Regression scores better on FD002–FD004: a few large over-predictions inflate Random Forest's score. "Best model" depends on the metric.
Classification (RUL ≤ 30), precision / recall: FD001 0.95 / 0.72, FD002 0.96 / 0.87, FD003 0.94 / 0.75, FD004 0.92 / 0.68.
Difficulty rises from FD001 to FD004. On FD003 the train–test RMSE gap is clear (12.85 → 20.18), which hints at overfitting.

FD001 Random Forest: actual vs predicted

All nine Colab charts for each dataset are in figures/FD001/ … figures/FD004/.

Open in Colab
Dataset	Challenge	Solution
FD001	Colab	Colab
FD002	Colab	Colab
FD003	Colab	Colab
FD004	Colab	Colab

Live Gradio demo: Colab · Web demo: https://canberkeken-bit.github.io/nasa-rul-turbofan-prediction/demo.html

Repository layout
notebooks/
  FD001 … FD004/   Challenge (fill-in-the-blanks) and Solution notebooks (Colab)
  NASA_RUL_Gradio_Canli_Demo.ipynb   live model UI with Gradio
kaggle/            the same notebooks adapted for Kaggle (see kaggle/README.md)
data/              data download instructions (raw data is not in the repo)
docs/              interactive charts and web demo (GitHub Pages)
reports/           graduation report, explanatory PDF, slides (PPTX and PDF)
figures/           all 36 charts (9 per dataset)
space/             Hugging Face Space (Gradio) for all four datasets: see space/README.md
How to run
Download the data and prepare train_FDxxx.txt, test_FDxxx.txt, RUL_FDxxx.txt (data/README.md).
Open a notebook in Google Colab (File → Upload notebook, or open from GitHub), then drag the three data files into Colab's Files panel. For Kaggle, see kaggle/README.md.
Run the cells in order. The Challenge notebook is for learning by filling the blanks; the Solution notebook shows the answers.
For the live demo run NASA_RUL_Gradio_Canli_Demo.ipynb; its last cell prints a gradio.live link (the link changes on every run).

To run locally: pip install -r requirements.txt and Jupyter.

Limitations
Results come from a single random seed (random_state=42) and a single train/test split; no cross-validation. Small differences should not be read as clear superiority.
The NASA score was computed against RUL capped at 125, so it is not directly comparable with scores in the literature.
The web demo shows precomputed predictions and does not run the model in the browser. The real live model is the Gradio notebook.
No formal statistical hypothesis test was run; the comparisons are presented as open research questions in the report's "Research questions and findings" section.
Next steps

Hyper-parameter tuning, GradientBoosting, time-window features for the sensors, choosing the alarm threshold from maintenance costs, cross-validation.

Data and citation

Data: NASA Prognostics Data Repository, Turbofan Engine Degradation Simulation Data Set (C-MAPSS). A. Saxena and K. Goebel (2008), NASA Ames Prognostics Data Repository. The data is not included in this repository.

License

Code and notebooks are released under the MIT license (LICENSE). The NASA data is subject to its own terms of use.
