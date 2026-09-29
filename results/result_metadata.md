# Result Metadata

- Source: preserved reproduction archive
- Included prefix: `server_official_e200_pan_e30_`
- Official experiment directories: 380
- Official metric CSV files: 380
- Preflight excluded: `preflight_BRCA_cv1_fold1_only_omics`
- Raw consolidated rows: 49,445 data rows (plus header)
- Summary rows: 76 (19 cancer/CV scenarios x 4 task types)

The raw file preserves the original metric values and adds deterministic metadata derived from the directory name. The original metric schemas differ by task type, so the raw table uses the union of observed metric columns and leaves a cell blank only when that column was absent from the corresponding source CSV. No numerical value was imputed or rounded in the raw file.

The compact summary follows the upstream `analysis.py`: within each fold, select the row with maximum `val_AUC`; collect `test_AUC`, `test_AUPR`, and `test_F1` plus the selected validation AUC; then calculate the arithmetic mean and population standard deviation over folds 1-5. For UMT and UME, the `selected_model_by_mean_val_AUC` field records the higher mean validation AUC, with ties resolving to UME as in the upstream implementation.

Consistency note: the preserved `server_official_analysis.txt` differs from the current CSV-derived summary for CESC CV1 UMT. The discrepancy is documented in `evidence/analysis_consistency_note.txt`; neither original artifact was modified.
