# Repository Audit

Audit status: completed

## Completion and Scope

- Official experiments: 380
- Official CSV files: 380
- Preflight experiments: 1
- Preflight included in official summary: NO
- Completion: 380/380
- Dataset scope: eight individual cancer types plus one pan-cancer dataset/setting

## Provenance and Integrity

- Source commit: `5856ae72e4462b75eb1c0901911ac2d29f02afab`
- Runner: `experiments/run_full_grid.py`
- Runner SHA-256: `8cd29f0eac2da80c4f4bea2105bd4739d5ade6ff74faa208f73b6bce2903ef8f`
- Verification notebook: `experiments/01_SynLeaF_Verification.ipynb` (15,852 bytes), retained unchanged as the execution/verification record and not executed during this audit
- Authoritative custom runner retained unchanged
- Upstream source distinguished from the reproduction runner
- Upstream source fidelity check passed: 11 tracked source files and retained upstream support files are byte-identical to the local checkout at the recorded commit; see `evidence/source_fidelity.txt`
- Stale `experiments/scheduler.py` duplicate removed
- No nested `src/src` structure

## Repository Contents

- Large checkpoints excluded
- Credentials and secrets excluded; the repository scan found no credential files
- Result summary generated
- Official analysis included
- Validation script included
- Archived-source materials: consolidated results, compact summaries, and traceability metadata were derived from the preserved reproduction archive.

## Results and Size

- Raw consolidated CSV data rows: 49,445
- Compact summary rows: 76
- Repository working-tree size: approximately 29 MB at the time of the audit.
- Largest file: `results/all_380_official_experiment_results.csv` (28,581,529 bytes)
- No files larger than 50 MB
- No files larger than 100 MB

## Unresolved Issues

- The custom runner is server-oriented and contains paths for the original university workspace; it is preserved unchanged and should not be treated as a portable local launcher without recreating that layout.
- The execution record supplied for the server OS and Python version is not accompanied by a standalone OS/Python snapshot file in the archive.
- The upstream checkout contains no license file; redistribution terms for upstream source should be confirmed before publication.
- The preserved official analysis text and the current CSV-derived summary differ for CESC CV1 UMT. Both are preserved unchanged and the generated audit note records the exact values.
