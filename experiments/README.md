# Experiments

`experiments/run_full_grid.py` is the authoritative reproduction-specific runner used for the university-server pass. It was recovered from the original university-server workspace and copied unchanged. Its SHA-256 is recorded in `evidence/run_full_grid_sha256.txt` and is `8cd29f0eac2da80c4f4bea2105bd4739d5ade6ff74faa208f73b6bce2903ef8f`.

The runner constructs the 380-task grid using prefix `server_official_e200_pan_e30`, eight individual cancer types (`BRCA`, `CESC`, `COAD`, `KIRC`, `LAML`, `LUAD`, `OV`, `SKCM`) plus the `pan` cancer setting, CV1/CV2 for individual cancers, CV1/CV2/CV3 for pan-cancer, five folds, and task types `only_omics`, `only_kg`, `umt`, and `ume`. It verifies task outputs and teacher checkpoints before continuing. The runner is preserved unchanged as part of the reproduction record.

The file is preserved at the repository's requested `experiments/` path, but its unchanged relative paths (`ROOT / "src"`, `ROOT / "result"`, and the server home-directory Accelerate configuration) reflect the original server workspace where it ran. These paths reflect the original server workspace, so the copied runner is preserved for provenance and should not be treated as a turnkey launcher from the repository root.

`01_SynLeaF_Verification.ipynb` is the recovered execution/verification record. It contains the data checks, the code used to write the runner, and the final result audit workflow. It is retained for provenance and is not the primary reusable experiment runner. It was not executed during this repository audit.

`reproduction_config.yaml` records the verified task grid, source commit, environment, and per-dataset training parameters. The upstream implementation files remain under `src/`, including the upstream `src/scheduler.py`; that file is distinct from the custom `experiments/run_full_grid.py`.

The official run was already completed. Repository validation does not require rerunning the training experiments. The archival master contains the full logs and checkpoints; this repository intentionally contains neither.
