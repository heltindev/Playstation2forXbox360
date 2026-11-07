# 00 · Start Here

[← Documentation home](../README.md) · [Next: PS2 architecture →](01-ps2-architecture.md)

> **Goal:** Define an achievable target, an evidence notebook and a measurable first experiment.

## What this project is

This is a research handbook for recreating or porting software originally designed for PlayStation 2 so that an independently built native application can run on an Xbox 360 homebrew environment.

It is **not** an emulator, a converter, a game download site or a working commercial game port. It cannot automatically transform PS2 MIPS instructions into a fully functional PowerPC program or transform graphics command packets into an Xbox 360 renderer.

## Select your first target wisely

| Source material | Relative difficulty | Recommended starting point? |
|:--|:--|:--|
| Your own PS2 sample program | Low | **Yes** |
| Open-source PS2 homebrew | Low–medium | **Yes**, subject to license |
| Source-available commercial game with permission | Medium–high | After fundamentals |
| Retail game disc with no source code | Very high | Advanced research |
| Large proprietary 3D game engine | Extremely high | Long-term team project |

A small, legally reusable program can teach the same architectural concepts while eliminating months of binary reconstruction.

## Skills to prepare

- C/C++ fundamentals: pointers, classes, memory layout, compilation, debugging.
- MIPS versus PowerPC: instruction sets, stack, calling conventions, endian behavior, ABI.
- Graphics: transforms, coordinate spaces, vertex buffers, textures and shaders.
- File formats: offsets, headers, bounds checking and compression.
- Reverse engineering: disassembly, call graphs, data references and experimental verification.
- Xbox 360 homebrew: independent toolchains, actual hardware and basic debugging.

**Need programs and download links?** Start with [Chapter 15: Essential Software and Tools](15-toolbox.md), then follow [Chapter 16: Practical Workflows](16-practical-workflows.md). You can run `python tools/check_environment.py` from the repository root to inspect command-line prerequisites.

## Private research layout

```text
private-research/                     # NEVER publish disc data
  original/
  hashes/
  ghidra-project/
  trace-notes/
  screenshots/
public-working-tree/
  docs/
  src/                                 # Independently written code
  tools/                               # Permitted research tools
  tests/                               # Synthetic/redistributable fixtures
```

Do not add a game's ISO or raw executable to Git. Maintain the original bytes privately and document hashes to preserve the research baseline.

## Research notebook template

| Field | Record |
|---|---|
| Observation ID | `OBS-001` |
| Program and revision | Disc ID, region, version and SHA-256 |
| Environment | Console type, emulator version, configuration |
| Reproduction steps | Exact starting state and user input |
| Result | What happened, including timing |
| Hypothesis | A possible explanation |
| Confidence | Low / medium / high |
| Follow-up experiment | One measurable next test |

**Observation is not interpretation.** A white screen might be a missing asset, a blocking read, a graphics pipeline issue or a boot failure. Record what is proven.

## First practical milestone

1. Choose a small permitted program or game.
2. Identify its boot executable and build a metadata inventory.
3. Inspect one format or behavior, not the full engine.
4. Reproduce that behavior in a desktop test harness.
5. Test an independent Xbox 360 XSDK sample to validate toolchain and hardware.
6. Document the behavior, test outcomes and unanswered questions.
7. Plan a **vertical slice**: one scene, one object, one interaction and one graphics frame.

## Completion checklist

- [ ] Source and redistribution permissions documented.
- [ ] Main executable or original source identified.
- [ ] Reproducible observation captured.
- [ ] Platform-neutral behavior described.
- [ ] Desktop test passes.
- [ ] Separate Xbox 360 sample runs on real hardware.
- [ ] Commercial binary assets kept out of the repository.

**Next:** [Understand the PlayStation 2 architecture](01-ps2-architecture.md).
