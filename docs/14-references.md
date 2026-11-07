# 14 · Annotated Reference Library

[← Glossary](13-glossary.md) · [↑ Documentation home](../README.md)

> **Goal:** Keep primary references visible and separate documented facts from assumptions. External documentation can change; verify versions at the source.

For a **step-by-step program list with official download links**, use [Chapter 15: Essential Software and Tool Directory](15-toolbox.md). For actual usage examples, see [Chapter 16: Practical Workflows](16-practical-workflows.md).

## PlayStation 2 research

### PS2DEV / PS2SDK

- **Repository:** https://github.com/ps2dev/ps2sdk
- **Documentation:** https://ps2dev.github.io/ps2sdk/
- **Purpose:** Public homebrew programming references, EE and IOP APIs, input, storage and audio services.
- **Caution:** It is a PS2 SDK, not an Xbox 360 compatibility library.

### PCSX2

- **Website:** https://pcsx2.net/
- **Source:** https://github.com/PCSX2/pcsx2
- **Purpose:** Execute reference behavior and use emulator-supported diagnostic tooling.
- **Caution:** Timing, bugs and hardware interpretation can differ from a physical PS2.

### Ghidra

- **Website:** https://ghidra-sre.org/
- **Source:** https://github.com/NationalSecurityAgency/ghidra
- **Purpose:** Analyze executable code, data layouts, references and candidate functions.
- **Caution:** Decompiler output is not guaranteed to match original source.

### Splat

- **Source:** https://github.com/ethteck/splat
- **Purpose:** Organize binary segments and assist supported decompilation projects.
- **Caution:** Configuration and game-specific work are still required.

## Xbox 360 homebrew

### XSDK

- **Source:** https://github.com/xenosworks/xsdk
- **Getting started:** https://github.com/xenosworks/xsdk/blob/main/docs/GETTING_STARTED.md
- **API guide:** https://github.com/xenosworks/xsdk/blob/main/docs/GUIDE.md
- **Pitfalls:** https://github.com/xenosworks/xsdk/blob/main/docs/PITFALLS.md
- **Hardware observations:** https://github.com/xenosworks/xsdk/blob/main/docs/HARDWARE.md
- **Purpose:** GCC/newlib PowerPC toolchain, C/C++ runtime, kernel APIs, graphics/audio, samples and XEX packaging.
- **Caution:** Independent and evolving; test its current samples on physical RGH/JTAG hardware before integration.

### Xenia

- **Source:** https://github.com/xenia-project/xenia
- **Purpose:** Useful for some smoke tests of compiled Xbox 360 homebrew.
- **Caution:** Passing Xenia does not guarantee working XEX on physical Xbox 360.

### LibXenon

- **Source:** https://github.com/Free60Project/libxenon
- **Purpose:** Alternative homebrew ecosystem with a different execution and boot model.
- **Caution:** Do not confuse XeLL/ELF workflows with an XSDK retail-kernel XEX.

## How to cite a technical claim

For every important claim, prefer:

1. Official source or open-source implementation reference.
2. Exact source version, branch/tag or commit when possible.
3. Reproducible independent test and environment.
4. Explicit confidence (verified / probable / untested).
5. Links to upstream documentation and known caveats.

Avoid anonymous forum quotes as sole evidence for byte layouts, instruction behavior or build steps.

## Platform independence

All external tools retain their original licenses and attribution requirements. Listing a project here does not imply endorsement, dependency bundling or permission to redistribute its binaries.

[Return to README](../README.md)
