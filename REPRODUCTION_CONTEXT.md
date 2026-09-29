# Reproduction Context

Project: SynLeaF reproduction and evidence repository.

- Source commit: `5856ae72e4462b75eb1c0901911ac2d29f02afab`.
- Official prefix: `server_official_e200_pan_e30`.
- Official grid: eight individual cancer types (BRCA, CESC, COAD, KIRC, LAML, LUAD, OV, SKCM) with CV1/CV2; one pan-cancer dataset/setting with CV1/CV2/CV3; folds 1-5; task types only_omics, only_kg, umt, ume.
- Completion: 380/380 official tasks; 380 official result directories; 380 official metric CSVs.
- Preflight: `preflight_BRCA_cv1_fold1_only_omics`, one environment-validation/preflight run, excluded from official summaries.
- Archive: A read-only archival copy of the complete university-server reproduction results is maintained separately from this repository. Checkpoints are not included in the public repository.
- Dataset: provided processed archive; SHA-256 `73a9fa252ab75c609ff76ecacc3ea5fa4dabc0204d4117e17c4362767b0400d1`.
- Environment: Ubuntu 22.04.5 LTS, Python 3.10.21, Conda `research-gpu`, PyTorch 2.7.1+cu118, Accelerate 0.34.2, two Tesla P40 GPUs, Accelerate MULTI_GPU with two processes and no mixed precision.
- Analysis: upstream `analysis.py`; selects the best validation-AUC row per fold, reports mean/std of test AUC, AUPR, and F1, and compares UMT and UME by mean validation AUC.
- Generated results: raw all-row CSV and 76-row summary CSV under `results/`.
- Evidence: completion audit, source commit, package freeze, GPU report, data checksum, processed-data size, manifest, runner log, and official analysis output.
- Runner: `experiments/run_full_grid.py` is the recovered custom university-server runner, SHA-256 `8cd29f0eac2da80c4f4bea2105bd4739d5ade6ff74faa208f73b6bce2903ef8f`; `experiments/01_SynLeaF_Verification.ipynb` is the supporting verification record.

This repository does not include training checkpoints or the full processed dataset. The official result files and archived reproduction evidence should be treated as preserved records and should not be modified. The preflight run is kept separate from the 380 official tasks.
