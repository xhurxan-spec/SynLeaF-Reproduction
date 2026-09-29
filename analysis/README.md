# Official Analysis

`analysis.py` is the upstream analysis implementation copied without logic changes. It reads the `train_val_evaluate.csv` files from the result directory using a task prefix, loops over CV1/CV2 for the eight single-cancer datasets and CV1/CV2/CV3 for pan-cancer, and processes five folds per scenario.

For each fold and task type it selects the row with maximum `val_AUC`, then reports that row's `test_AUC`, `test_AUPR`, and `test_F1`. It computes the arithmetic mean and population standard deviation across the five folds. For UMT and UME, the analysis compares their mean validation AUC and reports the model with the higher value. Ties resolve to UME because the upstream code uses the condition `UMT > UME`.

`server_official_analysis.txt` is the preserved output for prefix `server_official_e200_pan_e30`. It is evidence of the official analysis output, not a new interpretation or a comparison with the original paper.

The reusable experiment runner is the custom `experiments/run_full_grid.py`; the upstream `src/scheduler.py` is a separate upstream implementation. The verification notebook is retained under `experiments/` as execution provenance.

A comparison with the current archival CSVs identified one exact mismatch: the preserved CESC CV1 UMT line differs from values recomputed using the same selection rule. Both artifacts are retained unchanged, while `results/result_summary.csv` is derived from the current CSV files. See `evidence/analysis_consistency_note.txt`.
