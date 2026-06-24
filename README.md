# Body2Robot

Tools for inspecting human body capture datasets and retargeting motion to robot embodiments.

Body2Robot focuses on **LeRobot-format** datasets that include **PICO body tracking**: per-frame 24-joint poses (`observation.pico.body_joints_pose`), episode metadata, and optional camera video. The current release supports dataset download, skeleton visualization, and experimental bimanual retargeting to the Axol robot.

## Features

- Download and load LeRobot datasets from Hugging Face
- Read PICO body poses from episode parquet files
- Visualize the 24-joint PICO/SMPL skeleton with PyVista
- Solve Axol bimanual IK with Pyroki and visualize results in Viser
- Compare coordinate-axis mappings during retargeting tuning (manual experiments)

## Requirements

- Python 3.12 or 3.13
- [uv](https://docs.astral.sh/uv/) for environment management
- Git LFS skip flag recommended when syncing LeRobot (`GIT_LFS_SKIP_SMUDGE=1`)

## Installation

Clone the repository and install dependencies with the extras you need:

```bash
git clone https://github.com/mbrq13/Body2Robot.git
cd Body2Robot
```

Recommended development setup (dataset tools, viewer, and Axol stack):

```bash
GIT_LFS_SKIP_SMUDGE=1 uv sync --extra lerobot --extra viewer --extra axol
```

Optional dependency groups:

| Extra | Purpose |
| --- | --- |
| `lerobot` | Dataset download and parquet I/O |
| `viewer` | PICO skeleton visualization |
| `axol` | Axol IK, URDF assets, and Viser simulation |

Install only what you need, for example:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv sync --extra lerobot
```

## Usage

All commands below assume you run them from the repository root.

### Download a dataset

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot scripts/download_lerobot_dataset.py \
  --repo-id ORG/YOUR-DATASET \
  --output-dir outputs/datasets/your-dataset \
  --revision main
```

Replace `ORG/YOUR-DATASET` with any Hugging Face dataset repo that exposes PICO body poses in LeRobot layout.

To download metadata and parquet only (no videos):

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot scripts/download_lerobot_dataset.py \
  --repo-id ORG/YOUR-DATASET \
  --output-dir outputs/datasets/your-dataset \
  --revision main \
  --no-videos
```

Downloaded data is stored under `outputs/` and is excluded from version control.

### Visualize PICO body motion

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra viewer scripts/view_pico_skeleton.py \
  --dataset-root outputs/datasets/your-dataset \
  --episode 0 \
  --revision main
```

This renders `observation.pico.body_joints_pose` (shape `(T, 24, 7)`: joint position and orientation) as a moving skeleton.

### Retarget arms to Axol (experimental)

Replay human arm motion on the Axol Viser simulation:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra axol \
  tests/manual/replay_pico_arms_on_axol.py \
  --dataset-root outputs/datasets/your-dataset \
  --episode 0 \
  --revision main
```

The replay loops over the full episode by default. It uses the calibrated
front Axol workspace and the `z,x,y` PICO-to-Axol axis map used by the Dexumi
reference experiment. Open the Viser URL printed in the terminal (default port
`8002`).

To compare against raw URDF rest targets in a single pass:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra axol \
  tests/manual/replay_pico_arms_on_axol.py \
  --dataset-root outputs/datasets/your-dataset \
  --episode 0 \
  --revision main \
  --axol-workspace rest \
  --no-loop \
  --hold-after 10
```

Compare axis-mapping candidates side by side:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra axol \
  tests/manual/compare_axis_maps_axol.py \
  --dataset-root outputs/datasets/your-dataset \
  --episode 0 \
  --revision main \
  --port 8003 \
  --scale 1.0 \
  --loop
```

See [tests/manual/README.md](tests/manual/README.md) for tuning flags and experiment notes.

## Project structure

- `src/body2robot/` — Python package (I/O, skeleton helpers, robot embodiments)
- `src/body2robot/embodiments/axol/` — Axol URDF, IK solver, and Viser simulation
- `src/body2robot/retargeting/` — reserved for shared retargeting logic (in progress)
- `scripts/` — CLI helpers for download and visualization
- `tests/manual/` — experimental retargeting scripts used during development
- `docs/` — design notes

Further details on embodiment layout: [docs/embodiments.md](docs/embodiments.md).

## Embodiments

Robot-specific assets and solvers live under `src/body2robot/embodiments/`. The first supported robot is **Axol**, with bimanual IK (Pyroki/JAXLS), configuration presets, and an offline Viser simulator. Retargeting adapters will remain separate from embodiment code so the human-body pipeline stays reusable across robots.

## Roadmap

- Promote validated retargeting from `tests/manual/` into `src/body2robot/retargeting/`
- Add a SMPL-like intermediate representation after skeleton validation
- Improve calibration, axis mapping, and replay stability

## Supported dataset fields

Body2Robot expects LeRobot episode parquet with at least:

| Field | Description |
| --- | --- |
| `observation.pico.body_joints_pose` | Per-frame body pose, shape `(24, 7)` (24 joints, 7D pose per joint) |
| `episode_index`, `timestamp` | Episode and time indexing (standard LeRobot columns) |
| `meta/info.json` | Feature schema, FPS, and episode counts |

Optional but common: camera observations under `observation.images.*` or `observation.image.*`, plus task metadata in `meta/tasks.*`.

## Notes

- Temporal body motion lives in parquet, not in `meta/stats.json` (stats are useful for range checks only).
- Do not commit local environments (`.venv/`) or downloaded datasets (`outputs/`).
