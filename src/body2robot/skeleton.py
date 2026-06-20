"""Skeleton definitions used by Body2Robot viewers."""

from __future__ import annotations

# SMPL-like 24-joint parent chain used by SONIC's live visualizer.
# Joint i connects to parent[i]. Joint 0 is the root.
SMPL24_PARENT_INDICES = [
    -1,
    0,
    0,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    9,
    9,
    12,
    13,
    14,
    16,
    17,
    18,
    19,
    20,
    21,
]


def parent_indices_to_lines(parent_indices: list[int]) -> list[int]:
    """Convert a parent-index skeleton to PyVista line-cell format."""
    cells: list[int] = []
    for child, parent in enumerate(parent_indices):
        if parent < 0:
            continue
        cells.extend([2, parent, child])
    return cells
