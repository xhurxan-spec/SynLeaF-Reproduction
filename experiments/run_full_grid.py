
from pathlib import Path
import csv
import json
import os
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
RESULT = ROOT / "result"

CONFIG = (
    Path.home()
    / "research/synleaf_server/workspace/SynLeaF_official/accelerate_config.yaml"
)

PREFIX = "server_official_e200_pan_e30"


CANCERS = [
    "BRCA",
    "CESC",
    "COAD",
    "KIRC",
    "LAML",
    "LUAD",
    "OV",
    "SKCM",
    "pan",
]


TASK_TYPES = [
    "only_omics",
    "only_kg",
    "umt",
    "ume",
]


ACCELERATE = Path(sys.executable).with_name("accelerate")


def cv_list(cancer):
    if cancer == "pan":
        return [1, 2, 3]
    return [1, 2]


def task_name(cancer, cv, fold, task):
    return f"{PREFIX}_{cancer}_cv_{cv}_fold_{fold}_{task}"


def specification(cancer):
    if cancer == "pan":
        return (
            30,
            2048,
            ["cna", "exp", "mut"],
            [2048, 1024, 512, 256],
        )

    return (
        200,
        384,
        ["cna", "exp", "mut", "myl"],
        [512, 256],
    )


def build_tasks():
    tasks = []

    for task in TASK_TYPES:
        for cancer in CANCERS:
            for cv in cv_list(cancer):
                for fold in range(1, 6):
                    epochs, batch_size, omics, vae_dims = specification(cancer)

                    tasks.append(
                        {
                            "task": task,
                            "cancer": cancer,
                            "cv": cv,
                            "fold": fold,
                            "epochs": epochs,
                            "batch_size": batch_size,
                            "omics": omics,
                            "vae_dims": vae_dims,
                        }
                    )

    assert len(tasks) == 380
    return tasks


def task_complete(item):
    task = item["task"]
    cancer = item["cancer"]
    cv = item["cv"]
    fold = item["fold"]
    epochs = item["epochs"]

    output_dir = RESULT / task_name(cancer, cv, fold, task)

    metrics_file = output_dir / "train_val_evaluate.csv"
    parameters_file = output_dir / "hyper_parameters.json"

    if not metrics_file.is_file() or not parameters_file.is_file():
        return False

    try:
        rows = list(
            csv.DictReader(
                metrics_file.open(newline="")
            )
        )

        parameters = json.loads(
            parameters_file.read_text()
        )

    except Exception:
        return False

    expected_rows = 1 if task == "ume" else epochs

    if len(rows) != expected_rows:
        return False

    if parameters.get("task_type") != task:
        return False

    if int(parameters.get("epochs", -1)) != epochs:
        return False

    # UME intentionally has no checkpoint in the official source.
    if task == "ume":
        return True

    return (output_dir / "checkpoint.pth").is_file()


def teacher_checkpoints_exist(item):
    cancer = item["cancer"]
    cv = item["cv"]
    fold = item["fold"]

    omics_checkpoint = (
        RESULT
        / task_name(cancer, cv, fold, "only_omics")
        / "checkpoint.pth"
    )

    kg_checkpoint = (
        RESULT
        / task_name(cancer, cv, fold, "only_kg")
        / "checkpoint.pth"
    )

    return (
        omics_checkpoint.is_file()
        and kg_checkpoint.is_file()
    )


def build_command(item):
    task = item["task"]
    cancer = item["cancer"]
    cv = item["cv"]
    fold = item["fold"]
    epochs = item["epochs"]
    batch_size = item["batch_size"]
    omics = item["omics"]
    vae_dims = item["vae_dims"]

    output_name = task_name(
        cancer,
        cv,
        fold,
        task,
    )

    command = [
        str(ACCELERATE),
        "launch",
        "--config_file",
        str(CONFIG),
        "train.py",
        "--cancer_type",
        cancer,
        "--metric",
        str(cv),
        "--train_fold",
        str(fold),
        "--epochs",
        str(epochs),
        "--batch_size",
        str(batch_size),
        "--task_type",
        task,
        "--omics_types",
        *omics,
        "--vae_hidden_dims",
        *[str(value) for value in vae_dims],
        "--specify_result_saving_folder",
        output_name,
    ]

    if task in ("umt", "ume"):
        omics_name = task_name(
            cancer,
            cv,
            fold,
            "only_omics",
        )

        kg_name = task_name(
            cancer,
            cv,
            fold,
            "only_kg",
        )

        command.extend(
            [
                "--omics_ckpt_path",
                f"../result/{omics_name}/checkpoint.pth",
                "--kg_ckpt_path",
                f"../result/{kg_name}/checkpoint.pth",
            ]
        )

    return command


def main():
    RESULT.mkdir(exist_ok=True)

    tasks = build_tasks()

    print(
        f"Generated {len(tasks)} tasks.",
        flush=True,
    )

    for index, item in enumerate(
        tasks,
        start=1,
    ):
        task = item["task"]
        cancer = item["cancer"]
        cv = item["cv"]
        fold = item["fold"]

        name = task_name(
            cancer,
            cv,
            fold,
            task,
        )

        if task_complete(item):
            print(
                f"[{index}/380] SKIP {name}",
                flush=True,
            )
            continue

        if (
            task in ("umt", "ume")
            and not teacher_checkpoints_exist(item)
        ):
            raise RuntimeError(
                f"Required teacher checkpoint is missing "
                f"before {name}"
            )

        output_dir = RESULT / name
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        log_file = output_dir / "train.log"

        print(
            f"[{index}/380] RUN {name}",
            flush=True,
        )

        with log_file.open(
            "a",
            buffering=1,
        ) as log:

            completed = subprocess.run(
                build_command(item),
                cwd=SRC,
                stdout=log,
                stderr=subprocess.STDOUT,
                env={
                    **os.environ,
                    "PYTHONUNBUFFERED": "1",
                },
            )

        if completed.returncode != 0:
            raise RuntimeError(
                f"{name} failed. "
                f"Inspect {log_file}"
            )

        if not task_complete(item):
            raise RuntimeError(
                f"{name} ended without valid expected output. "
                f"Inspect {log_file}"
            )

        print(
            f"[{index}/380] DONE {name}",
            flush=True,
        )

    print(
        "380-task reproduction pass complete.",
        flush=True,
    )


if __name__ == "__main__":
    main()
