# 09 · Testing, Tracing and Validation

[← Building XEX](08-build-and-xex.md) · [Next: Roadmap →](10-roadmap.md)

> **Goal:** Establish whether a new port behaves like the original, not merely whether it displays a frame.

## Test at three levels

| Test level | What it verifies | Example |
|---|---|---|
| Unit | Isolated algorithms and parsers | Mesh header parser rejects invalid offsets |
| Integration | Modules work together | Loading a level produces correct geometry |
| Hardware | Real Xbox 360 behavior | Controller, draw, audio, storage, exit and performance |

A correct desktop test does not imply the Xbox backend works; a launched XEX does not imply gameplay fidelity.

## Record a source baseline

For each reference sequence, document:

- Version/revision, configuration and hardware/emulator.
- Starting game state and controller input.
- Frame rate/timing and timestamps.
- Camera position and scene state.
- Screenshot or video capture if you have rights to keep it privately.
- Observed animations, sounds and scene transitions.
- Known emulator-specific differences.

## Compare behavior, not instruction counts

Useful pass/fail conditions include:

- Given identical input and starting state, does the player reach the same approximate position?
- Are collision and animation event orders equivalent?
- Do menus transition to the same state?
- Is timing stable under load?
- Are transparent materials, shadows and framebuffer effects visually acceptable?
- Do audio events trigger and loop when expected?

Define tolerances explicitly when comparing floating-point state; require exact equality only where warranted.

## A debug log template

```text
[BOOT] title version=0.1.0 platform=xbox360
[ASSET] loaded scene=example_scene
[INPUT] port=0 ready=true
[FRAME] frame=120 dt_ms=16.67
[AUDIO] voice=example_sfx queued
[TEST] scene_load PASS
[TEST] camera_position FAIL expected=(...) actual=(...)
[EXIT] status=0
```

These are example log lines, not an existing logging API. Reproduce error cases with source version and commit hash.

## Real console first principles

- Test that startup and shutdown are reliable.
- Inspect title logs on device and preserve diagnostic text.
- Watch for byte-order assumptions in loaders.
- Validate graphics and audio timing under memory pressure.
- Check the effect of missing controllers and missing assets.
- Measure CPU/GPU contention rather than assuming a desktop emulator is equivalent.

## Evidence-driven bug reports

A good bug report contains: minimal steps, expected result, actual result, console model and homebrew environment, game/source version, log excerpt, screenshot where appropriate, and evidence that the problem is in the new implementation.

Do not attach copyrighted game binaries, firmware, keys or other restricted content.

## Release readiness

- [ ] Builds reproduce from documented source and toolchain.
- [ ] A real console runs the title reliably.
- [ ] Main interactions meet documented tolerances.
- [ ] Error handling and logs are available.
- [ ] Rights to redistributed source/assets are documented.
- [ ] No claim of general compatibility is made without tests.

[Next: Development milestones](10-roadmap.md)
