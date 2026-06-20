#!/usr/bin/env python3
"""Visualize PICO body joints from a LeRobot dataset as a 24-joint skeleton."""

from __future__ import annotations

import argparse
import time

from body2robot.lerobot_io import load_pico_body_poses
from body2robot.skeleton import SMPL24_PARENT_INDICES, parent_indices_to_lines


def main() -> None:
    parser = argparse.ArgumentParser(description="View PICO body joints as a skeleton.")
    parser.add_argument(
        "--repo-id",
        default="NONHUMAN-RESEARCH/dexumi-dataset-v2",
        help="Hugging Face dataset repo id.",
    )
    parser.add_argument(
        "--dataset-root",
        default="outputs/datasets/dexumi-dataset-v2",
        help="Local dataset directory downloaded with download_lerobot_dataset.py.",
    )
    parser.add_argument("--episode", type=int, default=0)
    parser.add_argument("--revision", default="main")
    parser.add_argument("--column", default="observation.pico.body_joints_pose")
    parser.add_argument("--stride", type=int, default=1, help="Render every N frames.")
    parser.add_argument("--fps", type=float, default=None, help="Override playback FPS.")
    parser.add_argument("--loop", action="store_true", help="Replay frames until the window closes.")
    parser.add_argument("--point-size", type=float, default=18.0)
    parser.add_argument("--line-width", type=float, default=5.0)
    parser.add_argument("--background", default="white")
    parser.add_argument("--joint-color", default="darkred")
    parser.add_argument("--bone-color", default="black")
    args = parser.parse_args()

    try:
        import numpy as np
        import pyvista as pv
    except ImportError as exc:
        raise RuntimeError(
            "Viewer dependencies are missing. Install with: "
            "GIT_LFS_SKIP_SMUDGE=1 uv sync --extra lerobot --extra viewer"
        ) from exc

    poses, dataset_fps = load_pico_body_poses(
        repo_id=args.repo_id,
        root=args.dataset_root,
        episode=args.episode,
        column=args.column,
        revision=args.revision,
    )

    positions = poses[:, :, :3]
    playback_fps = args.fps if args.fps is not None else dataset_fps
    frame_sleep = 0.0 if playback_fps <= 0 else 1.0 / playback_fps
    lines = np.asarray(parent_indices_to_lines(SMPL24_PARENT_INDICES))

    points_poly = pv.PolyData(positions[0])
    bones_poly = pv.PolyData(positions[0])
    bones_poly.lines = lines

    plotter = pv.Plotter(window_size=(1200, 800))
    plotter.set_background(args.background)
    plotter.add_mesh(
        points_poly,
        color=args.joint_color,
        point_size=args.point_size,
        render_points_as_spheres=True,
    )
    plotter.add_mesh(bones_poly, color=args.bone_color, line_width=args.line_width)
    plotter.add_axes()
    plotter.add_text(
        "PICO body_joints_pose reconstruction",
        position="upper_left",
        font_size=10,
        color="black",
    )
    plotter.show(interactive_update=True, auto_close=False)

    frame_indices = list(range(0, len(positions), max(1, args.stride)))
    while True:
        for frame_idx in frame_indices:
            frame_positions = positions[frame_idx]
            points_poly.points = frame_positions
            bones_poly.points = frame_positions
            plotter.add_text(
                f"episode={args.episode} frame={frame_idx}/{len(positions) - 1}",
                name="frame_text",
                position="lower_left",
                font_size=9,
                color="black",
            )
            plotter.update()
            time.sleep(frame_sleep)

        if not args.loop:
            break

    plotter.show()


if __name__ == "__main__":
    main()
