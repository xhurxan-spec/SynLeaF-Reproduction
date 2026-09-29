# Results

Only compact, GitHub-safe result summaries are stored here. The full per-task folders, training logs, and checkpoints are preserved separately from this repository and are not included in the public archive.

`all_380_official_experiment_results.csv` contains all rows from the 380 official metric files. Its metadata columns identify the experiment, cancer, CV, fold, task type, and source-result provenance. Metric columns are copied as source text; heterogeneous task-specific loss columns are represented as blank when they are absent from a source CSV.

`result_summary.csv` contains 76 rows: 19 cancer/CV scenarios multiplied by four task types. It uses the official maximum-validation-AUC row per fold and population mean/std across five folds. The preflight directory is excluded.
