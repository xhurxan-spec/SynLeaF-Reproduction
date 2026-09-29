# SynLeaF Reproduction Report

## 1. Introduction

This report documents a completed reproduction of the SynLeaF training and evaluation workflow. It is based on the preserved reproduction evidence and result records and does not modify the original result records.

## 2. Background

SynLeaF is a dual-stage multimodal framework for synthetic lethality prediction. The upstream paper describes fusion of four omics modalities with a knowledge-graph representation and feature-level distillation. The upstream source is retained in `src/`, and the paper metadata is recorded in `CITATION.cff`.

## 3. Reproduction Objective

The objective was to execute the full configured grid across eight individual cancer types and one pan-cancer dataset/setting, with five folds and four task types per CV scenario.

## 4. Original Study

The original study is identified as arXiv:2603.22369. The original authors' reported results are conceptually distinct from the reproduced results in this repository.

## 5. Source Code Version

The official source commit was `5856ae72e4462b75eb1c0901911ac2d29f02afab`. The tracked source files from that commit are copied under `src/`; the source commit is also preserved in `evidence/server_source_commit.txt`.

## 6. Dataset

The provided processed archive was used. Its recorded SHA-256 is `73a9fa252ab75c609ff76ecacc3ea5fa4dabc0204d4117e17c4362767b0400d1`. The archive is not included in this repository.

## 7. Computational Environment

The recorded server used Ubuntu 22.04.5 LTS, Python 3.10.21, Conda `research-gpu`, PyTorch 2.7.1+cu118, Accelerate 0.34.2, and two Tesla P40 GPUs. Full evidence is under `environment/` and `evidence/`.

## 8. Experimental Configuration

Single-cancer tasks used 200 epochs and batch size 384. Pan-cancer tasks used 30 epochs and batch size 2048 with three omics inputs and VAE hidden dimensions `[2048, 1024, 512, 256]`. The remaining reproduction parameters are recorded in `experiments/reproduction_config.yaml` and the preserved per-task reproduction records.

## 9. Experimental Grid

There are 19 cancer/CV scenarios, five folds, and four task types, giving 380 official tasks. The prefix is `server_official_e200_pan_e30`.

## 10. Training Procedure

The custom `experiments/run_full_grid.py` constructs the task order, checks resumable outputs and teacher checkpoints, and launches the released training script through Accelerate. Its verified SHA-256 is recorded in `evidence/run_full_grid_sha256.txt`. Single-modal tasks precede UMT and UME so their teacher checkpoints are available. The verification notebook is retained as a supporting execution and verification record; it is not the reusable runner.

## 11. Completion Verification

The preserved reproduction records contain 380 official result directories, 380 official `train_val_evaluate.csv` files, and 380 `hyper_parameters.json` files. The completion audit states `Completed: 380 / 380` and `All 380 tasks are complete.`

## 12. Official Analysis

The preserved analysis output follows the upstream analysis implementation. Each fold contributes the epoch with highest validation AUC; test AUC, AUPR, and F1 are then averaged across folds. UMT and UME are compared by mean validation AUC.

The preserved text output and the current CSV-derived calculation differ for CESC CV1 UMT. This is retained as an unresolved evidence discrepancy rather than silently reconciled; see `evidence/analysis_consistency_note.txt`.

## 13. Reproduced Results

The full compact metric table is `results/all_380_official_experiment_results.csv`; the 76-row scenario summary is `results/result_summary.csv`. These files are derived only from official-prefix directories.

## 14. Comparison with Original Study

This repository does not provide a numerical comparison with the original paper. A defensible comparison requires extracting the original paper or supplementary tables and defining matching metrics, splits, and selection rules. No such comparison is asserted here.

## 15. Reproducibility Evidence

Evidence includes the source commit, package freeze, GPU report, Accelerate configuration, data checksum, processed-data size, result manifest, runner log, completion audit, and official analysis output.

## 16. Limitations

The full result/checkpoint archive and processed dataset are not included in this repository. The custom runner retains server-oriented paths and should be run only in the corresponding server workspace or a deliberately recreated layout. Earlier Colab/Mac attempts are not interchangeable with the final server run. The upstream source tree and custom runner must be treated as separate provenance categories.

## 17. Future Work

Future work may add a separately verified comparison against the paper's supplementary numerical tables and may publish a small, license-compliant release of additional derived plots. Such work should not alter the preserved reproduction results.

## 18. Conclusion

The evidence supports the precise statement that the official university-server reproduction completed 380/380 configured tasks. It does not, by itself, prove identity with the original paper's results or validate broader biological claims.
