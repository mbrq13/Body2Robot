# Manual Axol Retargeting Tests

This folder contains experimental scripts used to validate body-to-robot
retargeting before moving the logic into `src/body2robot/retargeting`.

## PICO Body To Axol Arms

The current test maps relative PICO/SMPL24 arm motion to Axol end-effector and
elbow targets, solves Axol IK, and streams the resulting joint angles to the
Viser simulation.

Install the optional dependencies first:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv sync --extra lerobot --extra axol
```

Run the replay from the repository root:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra axol \
  tests/manual/replay_pico_arms_on_axol.py \
  --dataset-root outputs/datasets/dexumi-dataset-v2 \
  --episode 0 \
  --revision main \
  --scale 1.0 \
  --max-frames 300
```

Open the Viser URL printed by the script, usually:

```text
http://localhost:8002
```

The most important tuning flags are:

- `--scale`: changes how much human arm motion is applied to Axol.
- `--axis-map`: maps PICO deltas to Axol deltas. Default is `z,y,-x`.
- `--max-joint-delta`: allows more or less joint motion per dataset frame.
- `--left-only` / `--right-only`: isolates one arm while tuning.

## Compare Axis Maps

To compare the current finalist mappings across the full episode:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra axol \
  tests/manual/compare_axis_maps_axol.py \
  --dataset-root outputs/datasets/dexumi-dataset-v2 \
  --episode 0 \
  --revision main \
  --port 8003 \
  --scale 1.0
```

The scene shows these candidates around the most promising `z,x,y` mapping:

- `[1] z,x,y`
- `[2] z,x,-y`
- `[3] z,-x,y`
- `[4] z,-x,-y`
- `[5] -z,x,y`
- `[6] -z,x,-y`
- `[7] -z,-x,y`
- `[8] -z,-x,-y`

Pick the one where vertical motion stays vertical, forward motion goes forward,
and left/right are not mirrored.

For a faster smoke test, limit the replay:

```bash
GIT_LFS_SKIP_SMUDGE=1 uv run --extra lerobot --extra axol \
  tests/manual/compare_axis_maps_axol.py \
  --dataset-root outputs/datasets/dexumi-dataset-v2 \
  --episode 0 \
  --revision main \
  --port 8003 \
  --scale 1.0 \
  --max-frames 180
```
