#!/usr/bin/env python3
"""Lightweight, non-training validation of the repository and archive."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
PREFIX = "server_official_e200_pan_e30_"
PREFLIGHT = "preflight_BRCA_cv1_fold1_only_omics"
COMMIT = "5856ae72e4462b75eb1c0901911ac2d29f02afab"
RUNNER_SHA256 = "8cd29f0eac2da80c4f4bea2105bd4739d5ade6ff74faa208f73b6bce2903ef8f"
INDIVIDUAL_CANCERS = ["BRCA", "CESC", "COAD", "KIRC", "LAML", "LUAD", "OV", "SKCM"]
CANCERS = INDIVIDUAL_CANCERS + ["pan"]
TASK_TYPES = ["only_omics", "only_kg", "umt", "ume"]
PATTERN = re.compile(
    r"^server_official_e200_pan_e30_.+_cv_[0-9]+_fold_[0-9]+_(only_omics|only_kg|umt|ume)$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the repository against the preserved reproduction archive."
    )
    parser.add_argument(
        "--archive-result",
        type=Path,
        help="Required path to the separately preserved reproduction result directory.",
    )
    args = parser.parse_args()
    if args.archive_result is None:
        parser.error(
            "--archive-result is required because the full reproduction archive "
            "is external to this repository; provide its local result-directory path"
        )
    if not args.archive_result.is_dir():
        parser.error(
            f"archive result directory does not exist or is not a directory: "
            f"{args.archive_result}"
        )
    return args


def expected_experiments() -> set[str]:
    names = set()
    for cancer in CANCERS:
        cvs = [1, 2, 3] if cancer == "pan" else [1, 2]
        for cv in cvs:
            for fold in range(1, 6):
                for task in TASK_TYPES:
                    names.add(
                        f"server_official_e200_pan_e30_{cancer}_cv_{cv}_fold_{fold}_{task}"
                    )
    return names


def check(label: str, condition: bool, detail: str) -> bool:
    print(f"{'PASS' if condition else 'FAIL'}: {label} - {detail}")
    return condition


def main() -> int:
    args = parse_args()
    official = sorted(
        path for path in args.archive_result.iterdir()
        if path.is_dir() and path.name.startswith(PREFIX)
    )
    csv_dirs = [path for path in official if (path / "train_val_evaluate.csv").is_file()]
    json_dirs = [path for path in official if (path / "hyper_parameters.json").is_file()]
    raw_path = REPOSITORY / "results/all_380_official_experiment_results.csv"
    summary_path = REPOSITORY / "results/result_summary.csv"
    completion = REPOSITORY / "evidence/completion_audit.txt"
    source_commit = REPOSITORY / "evidence/server_source_commit.txt"
    analysis = REPOSITORY / "analysis/server_official_analysis.txt"
    runner = REPOSITORY / "experiments/run_full_grid.py"
    notebook = REPOSITORY / "experiments/01_SynLeaF_Verification.ipynb"
    config = REPOSITORY / "experiments/reproduction_config.yaml"
    consistency_note = REPOSITORY / "evidence/analysis_consistency_note.txt"
    runner_provenance = REPOSITORY / "evidence/run_full_grid_sha256.txt"
    notebook_provenance = REPOSITORY / "evidence/verification_notebook_provenance.txt"
    source_fidelity = REPOSITORY / "evidence/source_fidelity.txt"

    passed = [
        check("official directory count", len(official) == 380, str(len(official))),
        check("official train_val_evaluate.csv count", len(csv_dirs) == 380, str(len(csv_dirs))),
        check("official hyper_parameters.json count", len(json_dirs) == 380, str(len(json_dirs))),
        check("official prefix", all(PATTERN.fullmatch(path.name) for path in official), PREFIX),
        check("preflight excluded by prefix", PREFLIGHT not in {path.name for path in official}, PREFLIGHT),
        check("consolidated result exists", raw_path.is_file(), str(raw_path)),
        check("result summary exists", summary_path.is_file(), str(summary_path)),
        check("completion audit exists", completion.is_file(), str(completion)),
        check("source commit file exists", source_commit.is_file(), str(source_commit)),
        check("analysis output exists", analysis.is_file(), str(analysis)),
        check("runner exists", runner.is_file(), str(runner)),
        check("verification notebook exists", notebook.is_file(), str(notebook)),
        check("reproduction configuration exists", config.is_file(), str(config)),
        check("runner provenance exists", runner_provenance.is_file(), str(runner_provenance)),
        check("notebook provenance exists", notebook_provenance.is_file(), str(notebook_provenance)),
        check("source fidelity evidence exists", source_fidelity.is_file(), str(source_fidelity)),
        check("analysis consistency note exists", consistency_note.is_file(), str(consistency_note)),
    ]

    names: list[str] = []
    if raw_path.is_file():
        with raw_path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            names = [row["experiment"] for row in reader]
    official_names = {path.name for path in official}
    represented = set(names)
    unexpected_result_files = [
        path for path in REPOSITORY.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.suffix.lower() in {".pth", ".pt", ".ckpt", ".tar", ".gz", ".zip"}
    ]
    checkpoint_dirs = [
        path for path in REPOSITORY.rglob("*")
        if path.is_dir() and (".ipynb_checkpoints" in path.parts or path.name == "__pycache__")
    ]
    runner_hash = hashlib.sha256(runner.read_bytes()).hexdigest() if runner.is_file() else ""
    summary_rows = []
    if summary_path.is_file():
        with summary_path.open(newline="") as handle:
            summary_rows = list(csv.DictReader(handle))
    passed.extend([
        check("raw CSV contains no preflight", PREFLIGHT not in represented, PREFLIGHT),
        check("raw CSV has 380 distinct experiments", len(represented) == 380, str(len(represented))),
        check("all official experiments represented", official_names == represented, f"{len(official_names & represented)}/380 represented"),
        check("experiment names match expected grid", official_names == expected_experiments(), f"{len(official_names & expected_experiments())}/380 expected names"),
        check("source commit matches", source_commit.is_file() and source_commit.read_text().strip() == COMMIT, COMMIT),
        check("completion says 380/380", completion.is_file() and "Completed: 380 / 380" in completion.read_text(), "completion audit"),
        check("runner SHA-256 matches", runner_hash == RUNNER_SHA256, runner_hash or "missing"),
        check("runner is not the upstream scheduler copy", runner.is_file() and runner.read_bytes() != (REPOSITORY / "src/scheduler.py").read_bytes(), "custom wrapper distinction"),
        check("source fidelity evidence reports all tracked files matched", source_fidelity.is_file() and "All 11 files matched" in source_fidelity.read_text(), "upstream source comparison"),
        check("summary has 76 scenario/task rows", len(summary_rows) == 76, str(len(summary_rows))),
        check("preflight absent from summary", all(PREFLIGHT not in str(row) for row in summary_rows), PREFLIGHT),
        check("no nested src/src directory", not (REPOSITORY / "src/src").exists(), "repository structure"),
        check("no stale experiments/scheduler.py duplicate", not (REPOSITORY / "experiments/scheduler.py").exists(), "repository structure"),
        check("no checkpoint/archive artifacts", not unexpected_result_files, ", ".join(map(str, unexpected_result_files)) or "none"),
        check("no notebook checkpoints or Python caches", not checkpoint_dirs, ", ".join(map(str, checkpoint_dirs)) or "none"),
        check("discrepancy note names CESC CV1 UMT", consistency_note.is_file() and "CESC CV1 UMT" in consistency_note.read_text(), "analysis discrepancy"),
    ])
    print(f"\nValidation result: {'PASS' if all(passed) else 'FAIL'}")
    return 0 if all(passed) else 1


if __name__ == "__main__":
    sys.exit(main())
