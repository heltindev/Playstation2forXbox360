# 12 · Troubleshooting by Evidence

[← Legal and ethics](11-legal.md) · [Next: Glossary →](13-glossary.md)

> **Goal:** Debug the smallest observable failure before rewriting whole subsystems.

## Diagnostic table

| Symptom | Common possibilities | First useful experiment |
|---|---|---|
| Program will not boot | Incorrect target ABI, missing imports, invalid XEX or unsupported dashboard | Run unmodified XSDK `hello.xex` first |
| Black screen | Renderer never initializes, shader failure, no presentation | Clear to a known color and log each step |
| Texture colors are wrong | Endianness, pixel channel order, CLUT conversion | Decode a synthetic two-color texture |
| Mesh is inverted | Coordinate handedness, winding, matrix order | Render axes and a labeled test triangle |
| Input is ignored | Controller initialization, port selection, wrong mapping | Show/log raw controller state |
| Player moves too fast | Fixed timestep, delta-time assumptions | Compare displacement per simulated tick |
| No sound | Buffer setup, codec, sample rate, streaming thread | Play an SDK sample tone |
| Long stalls | Blocking reads, CPU/GPU sync, decompression | Timestamp individual load stages |
| Assets are missing | Path map, filename case, archive index | Log exact logical path and error result |
| Desktop works, console fails | Architecture-dependent behavior | Check big endian, alignment and hardware APIs |
| XEX only works in emulator | Xenia-to-console differences | Inspect target logs and upstream XSDK pitfalls |

## Debug sequence

1. Reproduce the problem in a minimal scenario.
2. Note the last reliable observation.
3. Identify which layer is responsible: input, game, asset, platform, OS or GPU.
4. Instrument boundaries with logs and timestamped outcomes.
5. Compare with a previously working reference implementation.
6. Change one variable.
7. Record whether the test supports or rejects the hypothesis.
8. Add a regression test before proceeding.

## Endianness example

On PS2 EE, typical integer data is little-endian; Xbox 360 native code commonly operates in big-endian mode. If a file encodes `0x12345678` in little-endian, its bytes are `78 56 34 12`. Interpreting those bytes directly as a native big-endian integer gives a different result.

Decode with explicit byte operations rather than directly casting file bytes to a native C++ structure:

```cpp
#include <cstdint>

std::uint32_t readU32LE(const unsigned char* p) {
    return std::uint32_t(p[0])
         | (std::uint32_t(p[1]) << 8)
         | (std::uint32_t(p[2]) << 16)
         | (std::uint32_t(p[3]) << 24);
}
```

This example assumes the caller already proved that at least four bytes remain in the input.

## Rendering test order

Before loading real geometry:

1. Clear the screen to a known color.
2. Render one triangle.
3. Render a cube with known winding.
4. Apply a simple checkerboard texture.
5. Enable depth and blending in isolation.
6. Load one permitted mesh and one texture.
7. Add the original scene's effects one at a time.

## Useful upstream troubleshooting

- [XSDK Pitfalls](https://github.com/xenosworks/xsdk/blob/main/docs/PITFALLS.md)
- [XSDK Hardware notes](https://github.com/xenosworks/xsdk/blob/main/docs/HARDWARE.md)
- [PCSX2 documentation](https://pcsx2.net/)
- [Ghidra](https://ghidra-sre.org/)

[Next: Glossary →](13-glossary.md)
