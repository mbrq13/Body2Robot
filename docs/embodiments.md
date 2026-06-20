# Embodiments

Body2Robot separates human-body data from robot-specific logic.

Each robot embodiment should own only the assets and code needed to solve and
visualize that robot:

```text
src/body2robot/embodiments/<robot_name>/
├── config.py        # Solver and embodiment-specific configuration
├── shared.py        # Joint names, link names, URDF helpers
├── solver.py        # IK/FK or robot-specific motion solver
├── sim.py           # Offline visualizer/simulator
└── urdf/            # Robot description and meshes
```

Retargeting code should live outside the embodiment package:

```text
src/body2robot/retargeting/
```

That keeps the data pipeline reusable:

```text
human dataset -> body representation -> retargeting adapter -> embodiment solver/sim
```

The first embodiment is `axol`, copied from the base `almond-bot/axol` IK and
simulation stack.
