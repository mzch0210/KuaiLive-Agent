# Secure self-hosted RTX 3090 runner setup

This document provisions the local RTX 3090 server as a **dedicated GitHub Actions execution backend** for the KuaiLive-Agent project while keeping the scientific protocol unchanged.

## Security position

`mzch0210/KuaiLive-Agent` is a public repository. GitHub explicitly warns that self-hosted runners on public repositories carry persistent-host compromise risk. The controls below reduce exposure but do not make a public self-hosted runner risk-free.

The strongest isolation is a dedicated machine or VM with no personal credentials and no access to sensitive internal services. If this server also hosts valuable credentials or services, use a separate VM/user boundary or a private execution repository instead.

The workflows added for this project therefore enforce all of the following:

- `workflow_dispatch` only; no `push`, `pull_request`, or `pull_request_target` trigger;
- exact authorized actor `mzch0210`;
- exact branch `main`;
- dedicated runner label `gpu-3090`;
- read-only repository token (`permissions: contents: read`);
- no repository secrets are required or referenced;
- official Actions are pinned to immutable full commit SHAs;
- checkout credentials are not persisted;
- the runner account must be non-root, without passwordless sudo, and not in the `docker` group;
- the runner HOME must not contain common SSH/cloud credential locations;
- residual downloaded dataset/cache directories are removed after the experiment;
- the P1 GPU workflow remains dev-only and does not inspect Twitch test ranking.

## 1. Create a dedicated Linux account

Use a dedicated unprivileged account such as `kuailive-runner`. Do **not** reuse your personal login.

Example on Ubuntu/Debian, run from an administrative account:

```bash
sudo adduser --disabled-password --gecos '' kuailive-runner
```

Do not grant this account passwordless sudo. Do not add it to the `docker` group. Do not copy personal SSH keys, AWS/Azure/GCP credentials, API tokens, or SSH agent forwarding into this account.

Switch to the account and verify that the GPU is visible:

```bash
sudo -iu kuailive-runner
nvidia-smi
```

The account must be able to see the NVIDIA GeForce RTX 3090 without privilege escalation.

## 2. Prepare the frozen Python CUDA environment

The workflow expects the interpreter at:

```text
$HOME/venvs/kuailive-gpu/bin/python
```

Use Python 3.10 if available to match the previous GitHub-hosted reproduction environment.

```bash
python3.10 -m venv "$HOME/venvs/kuailive-gpu"
source "$HOME/venvs/kuailive-gpu/bin/activate"
python -m pip install --upgrade pip
python -m pip install 'torch==2.4.1' --index-url https://download.pytorch.org/whl/cu124
python -m pip install 'numpy<2' 'pandas<3' tqdm prettytable
```

If the installed NVIDIA driver cannot support the CUDA 12.4 PyTorch wheel, use the official PyTorch 2.4.1 CUDA 12.1 wheel instead; do not change the PyTorch version.

Verify:

```bash
"$HOME/venvs/kuailive-gpu/bin/python" - <<'PY'
import torch
print('torch:', torch.__version__)
print('cuda build:', torch.version.cuda)
print('cuda available:', torch.cuda.is_available())
print('gpu:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
print('vram GiB:', torch.cuda.get_device_properties(0).total_memory / 1024**3 if torch.cuda.is_available() else None)
PY
```

Expected essentials:

- PyTorch starts with `2.4.1`;
- `cuda available: True`;
- GPU name contains `RTX 3090`.

## 3. Register the repository self-hosted runner

In GitHub, open:

`KuaiLive-Agent -> Settings -> Actions -> Runners -> New self-hosted runner`

Choose **Linux / x64** and follow GitHub's generated download commands while logged in as `kuailive-runner`.

When running the generated `config.sh` command, add a dedicated custom label and name, for example:

```bash
./config.sh \
  --url https://github.com/mzch0210/KuaiLive-Agent \
  --token '<ONE-TIME-TOKEN-FROM-GITHUB>' \
  --name kuailive-3090 \
  --labels gpu-3090 \
  --unattended
```

**Do not paste the registration token into ChatGPT, an issue, a commit, a shell-history screenshot, or any shared document.** Use the current one-time token shown by GitHub and let it expire after registration.

The default labels `self-hosted`, `linux`, and `x64` plus custom label `gpu-3090` must be visible in the GitHub runner settings.

## 4. Run it as a service under the dedicated account

From the runner installation directory, an administrator can install the generated service for the dedicated user:

```bash
sudo ./svc.sh install kuailive-runner
sudo ./svc.sh start
sudo ./svc.sh status
```

Alternatively, keep `./run.sh` running in a dedicated terminal for the initial healthcheck before installing the service.

When connected, GitHub should show the runner as **Idle**.

## 5. Network boundary

The runner initiates communication to GitHub. Allow required **outbound HTTPS/443** connectivity; do not expose a new inbound Internet port solely for GitHub Actions.

The experiment additionally downloads:

- the pinned public `JRappaz/liverec` Git repository;
- the public Twitch 100k dataset mirror;
- GitHub Action artifacts.

If this server sits on a sensitive LAN, apply host/network egress controls so the dedicated account cannot reach internal credential services, metadata endpoints, databases, or unrelated administrative interfaces.

Do not disable TLS certificate verification.

## 6. Required healthcheck before any training

After GitHub shows the runner as `Idle`:

1. Open `Actions` in `mzch0210/KuaiLive-Agent`.
2. Select **Secure GPU runner healthcheck**.
3. Choose the `main` branch.
4. Tick the confirmation input.
5. Click **Run workflow**.

The healthcheck will refuse to pass if it detects, among other things:

- root execution;
- passwordless sudo;
- membership in the `docker` group;
- SSH agent forwarding;
- common SSH private keys in the runner HOME;
- common AWS/Azure/GCP credential directories;
- missing RTX 3090;
- missing PyTorch 2.4.1 CUDA environment.

A successful run uploads a small hardware/runtime evidence artifact. This successful workflow run is the canonical signal that setup is complete.

## 7. Only after healthcheck PASS: launch P1 GPU dev freeze

Use the manual workflow:

**LiveRec Twitch P1 GPU dev freeze**

It preserves the frozen scientific protocol:

- official LiveRec commit `27eaf33d258d1c1ea2d6da1da81a5360e8c8ce6b`;
- Twitch 100k benchmark;
- `fr_ctx=true`, `fr_rep=true`;
- seed 42;
- learning rate 0.0005;
- L2 0.1;
- batch size 100;
- sequence length 16;
- embedding dimension 64;
- dev H@1 checkpoint selection;
- early-stop patience 15;
- maximum 150 epochs;
- CUDA execution only;
- **no Twitch test ranking inspection**.

The workflow records GPU/driver/package versions, the Twitch file SHA-256, the selected dev checkpoint, and training log into the GitHub Actions artifact.

## 8. Operational rule for this public repository

Do not modify either GPU workflow to trigger automatically on `push`, `pull_request`, or `pull_request_target` while the runner remains attached to this public repository.

Before merging any future workflow change that targets `[self-hosted, linux, x64, gpu-3090]`, review the exact shell commands first.

If collaborators with write access are added later, re-evaluate actor restrictions before allowing them to trigger the GPU runner.
