# SynLeaF Reproduction

This repository documents and summarizes a completed university-server reproduction of SynLeaF, a dual-stage multimodal framework for synthetic lethality prediction across single-cancer and pan-cancer settings. This repository contains the source code, configuration, analysis output, audit evidence, and compact result tables from the reproduction. The complete result/checkpoint archive is approximately 130 GB. It is preserved separately from the GitHub repository.

## Overview

The reproduction used the upstream SynLeaF source at commit `5856ae72e4462b75eb1c0901911ac2d29f02afab` and the provided processed data archive. The reproduction was completed on the university server, with all 380 configured tasks completed successfully. The separate one-epoch BRCA preflight is retained in the archival master but is excluded from every official result summary.

## Reproduction Objective

The objective was to run the released training and evaluation workflow across 19 cancer/CV scenarios: eight individual cancer types (`BRCA`, `CESC`, `COAD`, `KIRC`, `LAML`, `LUAD`, `OV`, `SKCM`) using CV1/CV2 and one pan-cancer dataset/setting using CV1/CV2/CV3. Each scenario contains five folds and four task types.

## Source Version

- Upstream repository: SynLeaF official source checkout
- Commit: `5856ae72e4462b75eb1c0901911ac2d29f02afab`
- The tracked upstream implementation files under `src/` are byte-identical to this commit. The upstream README and configuration files are also retained for reference. No upstream license file was present in the checkout; see `LICENSE` before redistributing the upstream source.

## Computational Environment

The recorded server environment was Ubuntu 22.04.5 LTS, Python 3.10.21, Conda environment `research-gpu`, PyTorch 2.7.1+cu118, CUDA build 11.8, Accelerate 0.34.2, and two NVIDIA Tesla P40 GPUs. Accelerate was configured for two processes, GPU IDs 0 and 1, multi-GPU, with no mixed precision. See `environment/environment_summary.md` and `evidence/`.

## Dataset

The run used the provided processed archive, not an independently reconstructed raw-data pipeline. The verified archive SHA-256 is `73a9fa252ab75c609ff76ecacc3ea5fa4dabc0204d4117e17c4362767b0400d1`. The extracted datasets are BRCA, CESC, COAD, KIRC, LAML, LUAD, OV, SKCM, and pan. The archive and extracted data are intentionally not included here.

## Experimental Design

Single-cancer tasks used 200 epochs, batch size 384, and omics `cna exp mut myl`. Pan-cancer tasks used 30 epochs, batch size 2048, omics `cna exp mut`, and VAE hidden dimensions `2048 1024 512 256`. Other training parameters are recorded in `experiments/reproduction_config.yaml` and the per-task `hyper_parameters.json` files in the archival master.

## Official 380-Task Grid

The official experiments use the prefix `server_official_e200_pan_e30`.
There are 95 cancer/CV/fold combinations, with four task types (`only_omics`, `only_kg`, `umt`, and `ume`) giving 380 official tasks in total.

The reproduction was launched using `experiments/run_full_grid.py`. Its SHA-256 hash is recorded in `evidence/run_full_grid_sha256.txt`. The verification notebook used during the reproduction is preserved as `experiments/01_SynLeaF_Verification.ipynb`. The runner log and completion audit are included in `evidence/`.

## Completion Status

The archival audit reports `Completed: 380 / 380` and `All 380 tasks are complete.` There is one separate `preflight_BRCA_cv1_fold1_only_omics` directory used for environment validation; it is not an official result.

## Result Files

- `results/all_380_official_experiment_results.csv` contains every row from the 380 official `train_val_evaluate.csv` files, together with experiment metadata and paths to the corresponding archival results.
- `results/result_summary.csv` contains one row per cancer/CV/task type. It selects each fold's maximum-validation-AUC row and computes population mean/std across five folds, following the upstream `analysis.py` logic.
- `results/result_metadata.md` and `results/TRACEABILITY.md` describe provenance and lookup rules.

## Official Analysis

The official analysis output from the university-server reproduction is included in `analysis/server_official_analysis.txt`. The corresponding `analysis.py` file is the analysis implementation from the upstream SynLeaF source.

The analysis selects the epoch with the highest validation AUC for each fold and reports the corresponding test AUC, AUPR, and F1 scores. For UMT and UME, the analysis compares their mean validation AUC across the five folds.

## Reproducibility

Use the source commit, processed-data archive checksum, `experiments/reproduction_config.yaml`, `experiments/accelerate_config.yaml`, and the upstream source under `src/`. The complete result/checkpoint archive and associated training logs are preserved separately from this repository and are not included in the GitHub repository.

## Repository Structure

```text
src/                 Upstream tracked SynLeaF source files
experiments/         Runner implementation, configuration, and execution notes
analysis/             Upstream analysis code and official analysis output
results/              Compact official CSV summaries only
environment/          Environment summary and package freeze
evidence/             Small audit, hardware, manifest, checksum, and runner files
documentation/        Technical report, methodology, and history of earlier attempts
data/                Dataset provenance and retrieval notes
scripts/              Summary-generation and lightweight validation scripts
```

## Limitations

The repository does not contain the full result/checkpoint archive, the processed data archive, or server credentials/private data. The custom runner is preserved, but it retains server-oriented paths and should be treated as an execution record unless the expected server workspace is recreated. The reproduced metrics are not claimed to be identical to the original paper's metrics unless a separate numerical comparison is performed. The preserved official analysis text and the current CSV-derived recomputation have one documented CESC CV1 UMT discrepancy; neither artifact was overwritten.

## Citation

The paper metadata is recorded in `CITATION.cff`. Cite the original SynLeaF paper and identify this repository as a reproduction when using the summarized results.
