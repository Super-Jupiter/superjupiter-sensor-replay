# SuperJupiter SensorReplay

Deterministic timed sensor replay with explicit dropped and replaced readings.

**Version 0.1.1: evolving preview. Hardware validation pending.**

Original MIT-licensed portable C++11 by [SuperJupiter](https://www.superjupiter.net).
No mandatory service, hidden clock reads, network calls or heap allocation in the core.

## What it does

Caller-owned samples have nondecreasing offsets below 2^31 ms and may share timestamps across channels.
Caller arrays must remain alive and unchanged. Faults identify source indices and either drop or replace raw values.
At most one fault per source index; invalid configurations are rejected before start. Raw NaN/Inf values are allowed.
next(nowMs) emits at most one due observation, with its scheduled timestamp, never the polling timestamp.
Polling clocks must advance by less than 2^31 ms from start and never backwards. A run finishes after all source entries are consumed.
No hidden clock, sleep, network, parsing, looping or hardware. Reset/start is explicit and reproducible.

## Install

PlatformIO exact release (after registry publication):

```ini
lib_deps = superjupiter/SuperJupiterSensorReplay@0.1.2
```

Arduino: use the versioned [GitHub release ZIP](https://github.com/Super-Jupiter/superjupiter-sensor-replay/releases/tag/v0.1.2).
Library Manager registration and index propagation are separate steps; check the official index before relying on IDE availability.

## Example

```cpp
#include <SuperJupiterSensorReplay.h>
using namespace superjupiter::sensor_replay;
int main() {
Sample samples[]={{20,0,0},{21,100,0},{22,200,0}};
SensorReplay replay(samples,3);
replay.start(0);Output reading={};
replay.next(100,reading);
return 0;
}

```

For Arduino, open `examples/Minimal`. It uses synthetic data only.
Results are deliberately local so applications can inspect outcomes before adding I/O.

## CMake

```cmake
add_subdirectory(path/to/superjupiter-sensor-replay)
target_link_libraries(your_app PRIVATE SuperJupiter::SensorReplay)
```

For an installed package use `find_package(SuperJupiterSensorReplay 0.1 CONFIG REQUIRED)`.
Top-level CMake builds tests/examples; a subproject does not enable developer tools by default.

## Documentation and verification

- [API and boundaries](https://github.com/Super-Jupiter/superjupiter-sensor-replay/blob/v0.1.2/docs/API.md)
- [Tests](https://github.com/Super-Jupiter/superjupiter-sensor-replay/blob/v0.1.2/tests/test.cpp)
- [Validation status](https://github.com/Super-Jupiter/superjupiter-sensor-replay/blob/v0.1.2/docs/VALIDATION.md)
- [Shared conventions](https://github.com/Super-Jupiter/superjupiter-sensor-replay/blob/v0.1.2/docs/CONVENTIONS.md)
- [Migration policy](https://github.com/Super-Jupiter/superjupiter-sensor-replay/blob/v0.1.2/docs/MIGRATION.md)

```sh
cmake -S . -B build/cmake
cmake --build build/cmake
ctest --test-dir build/cmake --output-on-failure
python3 tools/check_release.py --tag v0.1.2
```

Keep raw observations and their provenance in your application. Derived results are not physical truth.
Do not use fast-math or finite-math-only compiler assumptions. AVR double may have float precision.
Software tests, board compilation and physical validation are reported separately.

## Fits the SuperJupiter measurement portfolio

Complements [SensorQuality](https://github.com/Super-Jupiter/superjupiter-sensor-quality) and
[SampleWindow](https://github.com/Super-Jupiter/superjupiter-sample-window) without a required dependency.
Each component can be used independently. Domain models, customer data and proprietary applications are excluded.

## Support and licence

MIT. Report reproducible bugs through repository issues; private security reports: info@superjupiter.net.
Include version, configuration, inputs, expected and observed behaviour. No credentials or private customer data.


## Compatibility review 0.1.1

This patch includes independent regression tests and a reviewed [interoperability contract](https://github.com/Super-Jupiter/superjupiter-sensor-replay/blob/v0.1.2/docs/INTEROPERABILITY.md). Hardware validation pending.

- Removed unused duplicated math helpers and unnecessary includes.


## Complete optional portfolio example

[PortfolioPipeline](https://github.com/Super-Jupiter/superjupiter-sensor-replay/tree/v0.1.2/extras/PortfolioPipeline) exercises all twenty components, including two channels, rollover, invalid data, durable-adapter protocols and acknowledgements. The example uses synthetic RAM storage, not real persistence. Its exact-commit dependency lock is separate from the dependency-free core. Hardware validation pending.
