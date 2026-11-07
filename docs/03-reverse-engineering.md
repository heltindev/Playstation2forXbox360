# 03 · Reverse-Engineering Workflow

[← Disc structure](02-disc-and-formats.md) · [Next: Reconstruction →](04-code-reconstruction.md)

> **Goal:** Turn disassembly and runtime observations into testable, evidence-backed specifications.

**Recommended tools:** [Ghidra](https://ghidra-sre.org/) + the [PCSX2 debugger](https://pcsx2.net/docs/advanced/debugger/), with [Cutter](https://cutter.re/) as an optional alternative. Use [the tool directory](15-toolbox.md#stage-b--understand-the-executable-and-runtime-behavior) and [practical workflow 2](16-practical-workflows.md#workflow-2--identify-what-one-game-function-does).

## Two forms of evidence

**Static analysis:** Inspect executable structure, machine instructions, constants, strings, cross-references, call relationships, data tables and decompiler output.

**Dynamic analysis:** Observe how the game behaves under repeatable input, timing and asset-loading conditions. PCSX2 debugging facilities can help, but emulator behavior is not necessarily equivalent to real PS2 hardware.

Neither is sufficient alone. Use static clues to design dynamic tests, and dynamic tests to validate static hypotheses.

## Tool roles

| Tool | Research use |
|---|---|
| [Ghidra](https://ghidra-sre.org/) | Disassembly, function boundaries, type inference, cross-references |
| [PCSX2](https://pcsx2.net/) | Reference execution, debugger features where supported |
| [Splat](https://github.com/ethteck/splat) | Binary segment mapping for supported projects |
| [PS2SDK](https://github.com/ps2dev/ps2sdk) | Public PS2 system interface examples |
| Python | Inventory scripts, format inspection, test fixtures |
| Desktop C++ debugger | Validate your own replacement modules |

## Ten steps, in order

1. **Freeze the baseline:** game version, hash, emulator version and configuration.
2. **Find the boot ELF:** use `SYSTEM.CNF`, inspect executable headers.
3. **Map code and data:** sections, entrypoint, references, global tables.
4. **Find anchors:** strings, known public API patterns, suspected resource IDs.
5. **Build a call graph:** startup, update loop, asset loader, rendering and input.
6. **Use provisional names:** prefer `candidate_player_update` over confident guesses.
7. **Observe one controlled event:** button press, scene load, camera transition.
8. **Identify state transitions:** what changes before and after the event?
9. **Write a behavioral contract:** inputs, outputs, side effects and timing.
10. **Repeat under new conditions:** prove or reject the hypothesis.

## A function investigation record

| Field | Example |
|---|---|
| Function | `sub_XXXXXXXX` |
| Candidate name | `update_camera` |
| Inputs | Game state pointer, possible time value |
| Outputs | Camera matrix or state |
| Side effects | May write target direction |
| Evidence | Camera follows input during controlled test |
| Confidence | Medium |
| Next test | Idle state versus moving player |

These addresses are illustrative placeholders. Actual findings depend on the title.

## Why decompiled pseudocode is not the original source

Decompilers infer C-like output from assembly. They do not automatically recover the developer's variable names, class boundaries, templates, source files, project configuration or intent. Common pitfalls include:

- Wrong argument or return types.
- Inferred signedness or structure packing errors.
- Inlined functions mistaken for larger operations.
- Switch/jump tables interpreted incorrectly.
- Branch delay slots and hand-written assembly patterns.
- Data mistaken for code (and vice versa).
- Hidden hardware-dependent side effects.

Check hypotheses against multiple call sites and controlled experiments.

## Example behavioral test

```text
Claim: An action triggers only on the rising edge of button A.
Setup: Same saved state, stable frame pacing.
Test A: Tap A for one update.
Test B: Hold A for 20 updates.
Test C: Release and press A again.
Measure: Number and times of events generated.
Outcome: Confirm / reject / insufficient evidence.
```

Turn verified claims into portable automated tests. Save private traces; publish only permitted synthetic fixtures and original written specifications.

## Clean-room consideration

Some projects separate the team that produces behavior specifications from the team writing new source code, reducing direct copying of implementation details. Whether this is necessary or sufficient depends on applicable law, contracts, and the project's rights; legal advice may be appropriate.

## Deliverable

Maintain a versioned function map, observed game states, format notes, tests, evidence references, confidence values and a list of important unknowns.

**Next:** [Rebuild platform-neutral behavior](04-code-reconstruction.md).
