# Methodology

The authoritative completed run is defined by the prefix `server_official_e200_pan_e30`, the source commit recorded in `evidence/server_source_commit.txt`, the custom runner recorded in `experiments/run_full_grid.py`, the 380-task runner log, and the completion audit. The reproduction covers eight individual cancer types (BRCA, CESC, COAD, KIRC, LAML, LUAD, OV, SKCM) using CV1/CV2 plus one pan-cancer dataset/setting using CV1/CV2/CV3; every scenario has five folds and four task types.

The two single-modal tasks (`only_omics`, `only_kg`) provide teacher checkpoints for UMT and UME. The official analysis then selects each fold's best validation-AUC epoch, reports its held-out test metrics, aggregates across folds, and compares UMT with UME by mean validation AUC. This repository preserves that method and does not add statistical tests or claims beyond the recorded output.

The one-epoch `preflight_BRCA_cv1_fold1_only_omics` run is an environment/distributed-GPU validation. It is historical evidence only and is excluded from all official counts and summaries.

The verification notebook is retained as an execution record. The reusable runner is the custom `experiments/run_full_grid.py`, not the upstream `src/scheduler.py`.
