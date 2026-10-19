# SuperJupiter portfolio integration

Optional example using all twenty independently installed libraries. Core SensorReplay has no new dependency.

Two 10 Hz synthetic channels share one caller clock. The run crosses uint32 rollover, injects NaN, a dropped reading and an out-of-range value, preserves raw history, applies quality/calibration, filters and trends, aligns channels and compares agreement. Alarm-triggered capture, machine states, pulse metrics (explicit microseconds), aggregate buckets, integration and health feed a RAM-backed journal and acknowledged retry queue. Configuration and journal regions do not overlap. A conditional battery estimate uses illustrative current assumptions.

Expected synthetic result: 31 emitted observations, 3 acknowledged summaries, 1100 ms integrated coverage and 29.85 value-seconds. Raw history deliberately retains the out-of-range80 reading; invalid measurements never enter derived integration. Source timestamps and anchor revisions are explicit. Event capture retains a pre-trigger NaN for investigation.

Hardware validation pending. No physical device, storage durability, electrical behaviour or measured battery life is asserted. The memory adapter is not persistent. Use externally synchronised durable adapters and persistent stream-scoped IDs in real systems. ESP32 is recommended for this combined example; individual libraries also compile on Uno, subject to capacity/resource limits.

Run `python3 tools/verify_portfolio.py --compiler g++` (or clang++) to fetch the public exact-commit lock and run the host/CMake integration. The lock pins source versions for reproducibility; it does not change core package dependencies. Downloaded dependencies stay in build/ and are excluded from library packages.
