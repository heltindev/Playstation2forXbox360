# 10 · Development Roadmap

[← Validation](09-testing.md) · [Next: Legal boundaries →](11-legal.md)

> **Goal:** Make progress measurable and prevent the project from turning into an undefined full-game rewrite.

**Choose the tool for the milestone:** [Tool directory](15-toolbox.md) · [Practical workflows](16-practical-workflows.md) · [Local environment check](../tools/check_environment.py).

## Milestone board

| Phase | Objective | Concrete exit condition |
|---|---|---|
| **M0 · Scope** | Choose a legally permitted target | Rights, target version, research baseline documented |
| **M1 · Inventory** | Map binaries and data | Boot executable, asset map, unresolved formats listed |
| **M2 · Behavior** | Recover one subsystem's contract | Reproducible observations and test cases |
| **M3 · Portable prototype** | Implement on PC | Same inputs produce verified outcomes |
| **M4 · XSDK proof** | Compile a separate homebrew sample | Verified `hello.xex` running on real Xbox 360 |
| **M5 · Vertical slice** | One scene and controllable entity | Render, input, timing and sound validated |
| **M6 · Expansion** | Add game features in priority order | Regression suite and performance budget pass |
| **M7 · Distribution** | Produce a responsible release | Licensing, build, install and test notes complete |

> [!NOTE]
> These are suggested **future milestones**, not completed progress. There is no game-specific port in this repository.

## Organize tasks by risk

Work in this order:

1. **Research permissions and source availability.**
2. **Unblock toolchain validation early.** A compiler failure discovered months later is very costly.
3. **Prove a single asset path.** Parse one model, validate its texture and render on a desktop.
4. **Prove one gameplay contract.** Movement or camera logic is often a good early candidate.
5. **Prove the Xenos renderer on hardware.**
6. **Connect input, audio and resource streaming.**
7. **Expand only after one end-to-end feature works.**

## A realistic vertical slice

Example: build one small test arena and one character.

- On startup the XEX initializes display, storage and input.
- A minimal scene is read through a platform-neutral asset service.
- A mesh and texture display in the correct orientation.
- The controller moves a camera or actor using measured logic.
- One action triggers a sound.
- The title exits cleanly and writes a log.
- Two comparison tests match source behavior within defined tolerances.

The first release can be a research demonstration. It does not need to claim the commercial game is “ported.”

## Suggested issue labels

| Label | Use |
|---|---|
| `documentation` | Missing or inaccurate explanation |
| `research` | Fact not yet confirmed |
| `asset-format` | Parser/format investigation |
| `graphics` | Renderer and shader tasks |
| `audio` | Audio data or playback |
| `gameplay` | Reconstructed game behavior |
| `build` | Toolchain and XEX packaging |
| `testing` | Test cases and hardware validation |
| `legal-review` | Permissions and redistribution |

## Definition of done for each task

- A reproducible description exists.
- A test or recorded observation supports its result.
- Documentation links to the implementation or private evidence ID.
- Unsupported claims are clearly marked as hypotheses.
- Memory, ownership and endian issues are considered where relevant.
- No commercial/proprietary files enter public Git history.

## What success looks like

A high-quality result is **a reproducible, rights-respecting implementation of a clearly scoped behavior**, not a screenshot suggesting compatibility. Focus on correctness first, then game completeness, then performance.

[Next: Licensing and ethics](11-legal.md)
