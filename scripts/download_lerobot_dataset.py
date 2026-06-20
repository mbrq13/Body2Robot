#!/usr/bin/env python3
"""Download a LeRobot dataset through Body2Robot's LeRobot wrapper."""

from __future__ import annotations

import argparse

from body2robot.lerobot_io import download_lerobot_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a LeRobot dataset.")
    parser.add_argument(
        "--repo-id",
        required=True,
        help="Hugging Face dataset repo id, for example NONHUMAN-RESEARCH/dexumi-dataset-v2.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/datasets/lerobot",
        help="Local directory where the dataset will be materialized.",
    )
    parser.add_argument("--revision", default="main", help="Optional branch, tag, or commit.")
    parser.add_argument(
        "--episodes",
        default=None,
        help="Optional comma-separated episode indices, for example 0,2,5.",
    )
    parser.add_argument(
        "--no-videos",
        action="store_true",
        help="Download parquet and metadata only; skip videos.",
    )
    parser.add_argument(
        "--force-cache-sync",
        action="store_true",
        help="Ask LeRobot to refresh local files from the Hub.",
    )
    args = parser.parse_args()

    result = download_lerobot_dataset(
        repo_id=args.repo_id,
        output_dir=args.output_dir,
        revision=args.revision,
        episodes=args.episodes,
        download_videos=not args.no_videos,
        force_cache_sync=args.force_cache_sync,
    )

    print(f"repo_id: {result.repo_id}")
    print(f"root: {result.root}")
    print(f"episodes: {result.num_episodes}")
    print(f"frames: {result.num_frames}")
    print(f"fps: {result.fps}")
    print("features:")
    for feature in result.features:
        print(f"  - {feature}")


if __name__ == "__main__":
    main()
