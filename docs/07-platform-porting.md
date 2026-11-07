# 07 · Replacing PS2-Specific Subsystems

[← Xbox 360 hardware](06-xbox360-architecture.md) · [Next: XEX build →](08-build-and-xex.md)

> **Goal:** Convert platform-specific behavior into small, testable Xbox 360 implementations.

## Responsibility map

| PS2 concern | Proposed portable boundary | Xbox 360 implementation |
|---|---|---|
| GS/GIF rendering | `IRenderer` | Xenos/XSDK graphics operations |
| VU math | `IMathOps` or game logic | Correct C++ math, optional Xenon vector optimization |
| IOP pad services | `IInput` | XSDK controller services |
| SPU2 services | `IAudio` | XSDK audio backend |
| CD/DVD and IOP file services | `IFileSystem` | XSDK file access / game directory |
| Frame timer and interrupts | `IClock` | Target timing and synchronization |
| Save cards | `ISaveStorage` | Target storage and serialization |
| PS2-specific engine code | `Game` modules | Reimplemented portable C++ |

**These interface names are proposed design abstractions, not official XSDK APIs.**

## Graphics replacement plan

1. Record a known reference scene and screenshot.
2. Recover camera projection, matrices, geometry and material metadata.
3. Render the same mesh on desktop using a known conventional pipeline.
4. Port the display initialization and resource creation to XSDK.
5. Verify vertex layouts, winding and texture uploads.
6. Implement shader logic for visible PS2 material effects.
7. Compare transparency, Z-buffering, motion and presentation timing.
8. Profile and optimize on hardware.

A PS2 effect may require multiple Xenos passes instead of a direct register mapping. Preserve **appearance and behavior**, not the original command packet structure.

## Controller mapping

A DualShock 2 and Xbox 360 controller have different layouts and button identities. Define actions by meaning:

| Game action | Possible PS2 input | Possible Xbox 360 mapping |
|---|---|---|
| Confirm / interact | Cross | A |
| Cancel | Circle | B |
| Pause | Start | Start |
| Player movement | Left analog stick | Left analog stick |
| Camera | Right analog stick | Right analog stick |

This table is an **illustrative default**, not a universal mapping. Original games can assign any button. Normalize analog ranges, apply dead zones consistently and preserve differences between a press event and a held button.

## Audio replacement

Keep game events separate from codec playback. Create commands such as `playSound(id)`, `stopSound(id)`, `setVolume(id,v)` and `startMusic(track)`. The Xbox 360 backend handles file loading, decoding (if required), mixing, buffers, looping and playback.

XSDK's audio implementation, supported sample formats and threading model should be verified against its current upstream docs. Aim for reliable underflow-free playback before adding effects.

## File and streaming layer

Avoid hard-coding `cdrom0:` paths or assuming data lives in memory. Map virtual asset paths to the Xbox 360 title's game directory or other authorized storage.

- Normalize separators without changing logical resource identifiers.
- Validate paths to avoid traversal.
- Use buffered asynchronous loading where needed.
- Avoid loading enormous archives in full.
- Decouple source archive offsets from runtime file paths.
- Handle missing/corrupted files gracefully.

## Physics and animation

Recreate update sequencing, units, collision callbacks, interpolation and temporal behavior. A game that renders correctly but updates physics twice as often is not equivalent.

Suggested checks include running, jumping, moving platforms, repeated collisions, cutscene-to-gameplay transitions and animation root motion.

## Save system

A PS2 memory card structure is not a native Xbox 360 save format. Rebuild logical save data using versioned serialization. Include upgrade/migration decisions, checksum or integrity checks and careful handling of incomplete writes.

## Vertical-slice acceptance criteria

A useful first slice should:

- Start cleanly from a dashboard.
- Load and render a scene.
- Respond to controller input.
- Play one correct sound.
- Update gameplay at a measured pace.
- Exit safely.
- Produce logs for failed tests.
- Reproduce at least one verified original behavior.

[Next: Build a native XEX →](08-build-and-xex.md)
