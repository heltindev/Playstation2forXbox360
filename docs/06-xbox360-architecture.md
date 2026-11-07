# 06 · Xbox 360 Hardware and Homebrew Runtime

[← Asset pipeline](05-asset-pipeline.md) · [Next: Porting subsystems →](07-platform-porting.md)

> **Goal:** Understand the target hardware and the platform assumptions that a native port must respect.

## PS2 versus Xbox 360

| Area | PlayStation 2 | Xbox 360 |
|---|---|---|
| Main CPU | MIPS R5900-based Emotion Engine | 3-core PowerPC-based Xenon |
| Hardware threads | PS2-specific CPU/VU arrangement | 2 hardware threads per core (6 total) |
| Graphics | Graphics Synthesizer + vector units | ATI Xenos GPU |
| Memory | 32 MiB main RAM plus separate specialized memories | 512 MiB unified system memory, with GPU eDRAM |
| Data endianness | EE typically little-endian | Native PowerPC software typically big-endian |
| Audio | SPU2 + IOP services | Xbox 360 audio/kernel facilities |
| Main executable | PS2 ELF / boot program | Xbox 360 XEX (for retail-kernel homebrew) |

These are broad architectural characteristics, not full specifications for every feature.

## Xenon CPU: not the same instruction set

A PS2 ELF contains MIPS instructions. The Xbox 360 CPU uses a PowerPC ISA and different calling conventions, stack layout, instruction encoding and vector functionality.

The native port should compile portable source to PowerPC using a suitable Xbox 360 homebrew toolchain. Native libraries built for Windows x86-64, PS2 MIPS or modern game consoles cannot simply be linked into the XEX.

## Xenos GPU: rebuild the renderer

The PS2's GS/GIF pipeline and Xbox 360's Xenos pipeline differ fundamentally. A port needs its own Xbox 360 rendering backend:

- Allocate and upload vertex/index resources.
- Translate texture formats and sampler states.
- Compile or supply shaders suitable for Xenos.
- Configure render targets, depth, alpha, blending and viewport.
- Present frames with correct synchronization and aspect ratio.
- Reproduce PS2-specific visual effects where they affect fidelity.

Do not try to feed raw GS command streams to the Xenos GPU.

## Memory and endian issues

More memory is available than on PS2, but every structure crossing a file or hardware boundary must be checked. Critical issues include:

- Byte order of packed resource fields.
- Alignment and structure padding.
- Pointers accidentally serialized as raw addresses.
- CPU/GPU ownership and cache coherency.
- Lifetimes of staging/upload buffers.
- Streaming behavior and fragmentation.

A portable loader should decode explicit integer types rather than casting a file header directly into a C++ struct.

## Homebrew execution choices

There are two significantly different execution models:

| Option | Use case | Typical artifact |
|---|---|---|
| [XSDK](https://github.com/xenosworks/xsdk) | Independent homebrew targeting the Xbox 360 retail kernel on an RGH/JTAG console | `.xex` |
| [LibXenon](https://github.com/Free60Project/libxenon) | Bare-metal style homebrew via XeLL | ELF / XeLL workflow |

They are **not** interchangeable without redesign. This guide focuses on **XSDK and XEX**, because it aligns with launching homebrew from dashboards such as Aurora on a modified console.

### What XSDK provides

According to its upstream documentation, XSDK includes a custom PowerPC toolchain, newlib C runtime, C++ support, kernel and system APIs, controllers, audio, GPU command submission, XEX packaging and sample titles.

It is an independent, evolving project. API support and build instructions can change, so treat its current [Getting Started](https://github.com/xenosworks/xsdk/blob/main/docs/GETTING_STARTED.md), [Guide](https://github.com/xenosworks/xsdk/blob/main/docs/GUIDE.md) and [Pitfalls](https://github.com/xenosworks/xsdk/blob/main/docs/PITFALLS.md) as authoritative.

## General performance strategy

1. Produce correct output on desktop.
2. Build a minimal Xbox 360 sample.
3. Measure CPU, memory, draw calls, texture uploads and audio buffering.
4. Keep logic tasks independent enough to identify bottlenecks.
5. Reduce streaming stalls and repeated conversions.
6. Optimize only after recording actual bottleneck measurements.

**Do not assume high theoretical performance means a port will run well.** Memory bandwidth, synchronizations, shader behavior and CPU/GPU workloads still matter.

[Next: Platform subsystem mapping →](07-platform-porting.md)
