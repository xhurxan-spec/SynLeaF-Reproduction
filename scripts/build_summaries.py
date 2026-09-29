#!/usr/bin/env python3
"""Build GitHub-sized result tables from the archival official run.

This script reads only the 380 directories with the official result prefix.
It never reads or modifies checkpoints and deliberately excludes the preflight
directory. The summary follows src/analysis.py: select the row with the
largest validation AUC in each fold, then compute population mean/std over the
five folds.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
OUTPUT_RESULT = REPOSITORY / "results"
PREFIX = "server_official_e200_pan_e30"
TASK_RE = re.compile(
    rf"^{re.escape(PREFIX)}_(?P<cancer>.+)_cv_(?P<cv>[0-9]+)_fold_(?P<fold>[0-9]+)_"
    r"(?P<task_type>only_omics|only_kg|umt|ume)$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build compact result tables from the preserved reproduction archive."
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


def parse_experiment(name: str) -> dict[str, str | int]:
    match = TASK_RE.fullmatch(name)
    if not match:
        raise ValueError(f"Unexpected official experiment name: {name}")
    values = match.groupdict()
    return {
        "experiment": name,
        "cancer": values["cancer"],
        "cv": int(values["cv"]),
        "fold": int(values["fold"]),
        "task_type": values["task_type"],
    }


def population_std(values: list[float]) -> float:
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def fmt(value: float) -> str:
    return f"{value:.10g}"


def main() -> None:
    args = parse_args()
    OUTPUT_RESULT.mkdir(parents=True, exist_ok=True)
    directories = sorted(
        path
        for path in args.archive_result.iterdir()
        if path.is_dir() and path.name.startswith(PREFIX + "_")
    )
    if len(directories) != 380:
        raise RuntimeError(f"Expected 380 official directories, found {len(directories)}")

    raw_rows: list[dict[str, str]] = []
    selected: dict[tuple[str, int, int, str], dict[str, str]] = {}
    source_columns: list[str] = []

    for directory in directories:
        metadata = parse_experiment(directory.name)
        csv_path = directory / "train_val_evaluate.csv"
        with csv_path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise RuntimeError(f"Missing CSV header: {csv_path}")
            for column in reader.fieldnames:
                if column not in source_columns:
                    source_columns.append(column)
            rows = list(reader)

        if not rows:
            raise RuntimeError(f"Empty result CSV: {csv_path}")
        for row in rows:
            raw_rows.append(
                {
                    **{key: str(value) for key, value in metadata.items()},
                    "source_result_dir": f"result/{directory.name}",
                    "source_result_csv": f"result/{directory.name}/train_val_evaluate.csv",
                    **row,
                }
            )

        best = max(rows, key=lambda row: float(row["val_AUC"]))
        selected[tuple(metadata[key] for key in ("cancer", "cv", "fold", "task_type"))] = {
            **{key: str(value) for key, value in metadata.items()},
            "source_result_dir": f"result/{directory.name}",
            **best,
        }

    raw_columns = [
        "experiment",
        "cancer",
        "cv",
        "fold",
        "task_type",
        "source_result_dir",
        "source_result_csv",
        *source_columns,
    ]
    raw_path = OUTPUT_RESULT / "all_380_official_experiment_results.csv"
    with raw_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=raw_columns)
        writer.writeheader()
        writer.writerows(raw_rows)

    summary_columns = [
        "cancer",
        "cv",
        "task_type",
        "fold_count",
        "mean_val_AUC",
        "std_val_AUC",
        "mean_test_AUC",
        "std_test_AUC",
        "mean_test_AUPR",
        "std_test_AUPR",
        "mean_test_F1",
        "std_test_F1",
        "selected_model_by_mean_val_AUC",
        "source_prefix",
    ]
    cancers = ["BRCA", "CESC", "COAD", "KIRC", "LAML", "LUAD", "OV", "SKCM", "pan"]
    summary_rows: list[dict[str, str | int]] = []
    for cancer in cancers:
        for cv in ([1, 2, 3] if cancer == "pan" else [1, 2]):
            for task_type in ("only_omics", "only_kg", "umt", "ume"):
                folds = [selected[(cancer, cv, fold, task_type)] for fold in range(1, 6)]
                metrics = {
                    metric: [float(row[metric]) for row in folds]
                    for metric in ("val_AUC", "test_AUC", "test_AUPR", "test_F1")
                }
                summary_rows.append(
                    {
                        "cancer": cancer,
                        "cv": cv,
                        "task_type": task_type,
                        "fold_count": 5,
                        **{
                            f"mean_{metric}": fmt(sum(values) / len(values))
                            for metric, values in metrics.items()
                        },
                        **{
                            f"std_{metric}": fmt(population_std(values))
                            for metric, values in metrics.items()
                        },
                        "selected_model_by_mean_val_AUC": "pending"
                        if task_type in ("umt", "ume")
                        else "not_applicable",
                        "source_prefix": PREFIX,
                    }
                )

    # The official analysis compares UMT and UME by mean validation AUC.
    for row in summary_rows:
        if row["task_type"] not in ("umt", "ume"):
            continue
        peer = next(
            candidate
            for candidate in summary_rows
            if candidate["cancer"] == row["cancer"]
            and candidate["cv"] == row["cv"]
            and candidate["task_type"] in ("umt", "ume")
            and candidate["task_type"] != row["task_type"]
        )
        current = float(row["mean_val_AUC"])
        other = float(peer["mean_val_AUC"])
        row["selected_model_by_mean_val_AUC"] = "UMT" if current > other else "UME"

    summary_path = OUTPUT_RESULT / "result_summary.csv"
    with summary_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_columns)
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Wrote {raw_path} ({len(raw_rows)} rows)")
    print(f"Wrote {summary_path} ({len(summary_rows)} rows)")


if __name__ == "__main__":
    main()
