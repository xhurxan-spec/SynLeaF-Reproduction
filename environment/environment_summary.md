# Environment Summary

The following values are the recorded official server environment for the completed run.

| Component | Recorded value | Evidence |
|---|---|---|
| Operating system | Ubuntu 22.04.5 LTS | Execution record supplied with the reproduction; no OS snapshot was preserved in the archive |
| Python | 3.10.21 | Execution record supplied with the reproduction |
| Conda environment | `research-gpu` | Execution record and package freeze context |
| PyTorch | 2.7.1+cu118 | `evidence/research-gpu-freeze_after_synleaf.txt` |
| CUDA build | 11.8 | PyTorch package suffix and execution record |
| Accelerate | 0.34.2 | `evidence/research-gpu-freeze_after_synleaf.txt` |
| Distributed mode | `MULTI_GPU`, 2 processes, GPU IDs 0,1 | `experiments/accelerate_config.yaml` |
| Mixed precision | no | `experiments/accelerate_config.yaml` |
| GPUs | 2 x NVIDIA Tesla P40 | `evidence/nvidia-smi_after_synleaf.txt` |
| Driver-reported CUDA | 12.4 | `evidence/nvidia-smi_after_synleaf.txt` |

`environment/requirements.txt` is the recorded package freeze. It is evidence of the completed environment, not a promise that installing the freeze alone recreates the university server.
