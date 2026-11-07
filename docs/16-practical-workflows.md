# 16 · Practical Workflows: From Disc Inventory to Xbox 360 Sample

[← Tool directory](15-toolbox.md) · [↑ Documentation home](../README.md)

> **Goal:** Use the programs together in repeatable exercises. These workflows produce a research baseline, format specification, tested code and a separate XSDK sample; they do **not** automatically port a commercial game.

## Workflow 1 · Build a safe inventory

**Tools:** 7-Zip or another appropriate local disc-file reader, Python, ImHex.

**Inputs:** A legally permitted PS2 research disc/image and a private folder containing the **already extracted files**.

1. Open the disc or image using a tool that supports its filesystem. If the image cannot be read, use a legitimate alternate reader and verify its format rather than assuming corruption.
2. Record the actual `SYSTEM.CNF` and its `BOOT2` line; this typically names the main program.
3. Create a metadata-only inventory from the extracted folder:

   ```bash
   python tools/disc_inventory.py "/path/to/extracted-disc" --sha256 > "/private/inventory.json"
   ```

4. Check the `boot.executable_path` field in the output, and whether the referenced executable exists in your inventory.
5. Privately open a few file headers in ImHex. Compare suspected magic values, endian interpretations, lengths and repeated records.
6. Add a short note with assumptions and unknowns using [the notebook template](../templates/research-notebook.md).

**Deliverable:** a private JSON inventory, known boot executable, hashes and an explicit list of unknown resource formats.

**What this does not do:** decompress unknown archives, extract data directly from ISO files, recover source code or create Xbox executables.

## Workflow 2 · Identify what one game function does

**Tools:** Ghidra and PCSX2's official debugger.

1. Import the **privately held** EE executable into Ghidra and confirm the detected file format / processor settings.
2. Inspect strings and cross-references to find a suspected input, scene or loading function.
3. Name it `candidate_update_function`, not `update_function`, until evidence supports its identity.
4. In PCSX2, enable **Tools → Show Advanced Settings** and open **Debug → Open Debugger**.
5. Choose the **R5900** debugging layout for the main EE processor, or **R3000** for IOP investigation.
6. Start from a repeatable scene and perform one controlled action (e.g., a short button press).
7. Compare memory/code state and observed behavior across the action.
8. Write a behavioral contract: preconditions, inputs, outputs, side effects, timing and confidence.
9. Reproduce the same behavior in a small PC C++ test module instead of pasting decompiler pseudocode.

**Deliverable:** one verified behavior with a repeatable test. **Reality check:** emulator tracing is supporting evidence, not automatic proof of physical PS2 behavior.

See [Chapter 03](03-reverse-engineering.md) and [the official PCSX2 debugger documentation](https://pcsx2.net/docs/advanced/debugger/).

## Workflow 3 · Research a mysterious game archive

**Tools:** ImHex, Kaitai Struct, optionally Binwalk or QuickBMS.

1. Create two private examples of the same suspected format, preferably from different scenes.
2. Compare the headers in ImHex and note candidate magic, version, counts and entry offsets.
3. If the data contains recognizable signatures, **optionally** use Binwalk; remember that false positives are common.
4. If a trustworthy, matching QuickBMS script exists, read it and use it in a restricted environment on a disposable copy. Do not blindly run arbitrary scripts.
5. Translate the discovered structure into a small Kaitai `.ksy` description **or** an independently written read-only parser.
6. Validate file boundaries and offsets. Build synthetic malformed fixtures to test overflow and truncation.
7. Export one permitted resource to a neutral test format and compare it against reference observations.

**Deliverable:** a format specification, parser and unit tests. **Not a guarantee:** generic tools will not decode every title-specific pack.

## Workflow 4 · Check 3D, audio and video assets

**Tools:** Blender, vgmstream and FFmpeg/ffprobe.

- **3D:** after the archive format is understood and a model has been converted, load it into Blender. Check axes, winding, normals, UVs, materials, bone transforms and animation sampling.
- **Audio:** try vgmstream for a **supported** file. Compare decoded duration, rate, looping metadata and pitch with observed gameplay. vgmstream does not encode back into game formats.
- **Video:** use `ffprobe -hide_banner "input-file"` to determine whether a stream is recognized. Only attempt FFmpeg conversion if the demuxer and codec are supported. A PS2 PSS file may require title-specific handling.

**Deliverable:** one verified model, one verified audio sample, and video metadata where supported. Keep rights-bearing converted resources out of the public repository.

## Workflow 5 · Build a native Xbox 360 XEX

**Tools:** WSL 2/Debian, Git, CMake, Ninja, XSDK, glslang-xenon (when required), Xbox 360 RGH/JTAG.

The current source of truth is [XSDK's Getting Started guide](https://github.com/xenosworks/xsdk/blob/main/docs/GETTING_STARTED.md).

1. Install a supported Linux/WSL environment and the prerequisites listed upstream.
2. Clone XSDK and build its **PowerPC-targeted** compiler/runtime using the upstream `tools/toolchain/build.sh`.
3. Build required shader tools and verify at least the `hello`/`template` sample.
4. Use the sample template to build an independently written Xbox 360 program:

   ```bash
   cp -r ~/xsdk/samples/template ~/mytitle
   cd ~/mytitle
   cmake -S . -B build -G Ninja \
     -DCMAKE_TOOLCHAIN_FILE=$HOME/xsdk/cmake/xsdk.cmake \
     -DXSDK_TOOLCHAIN=$HOME/xsdk-gcc \
     -DCMAKE_BUILD_TYPE=RelWithDebInfo
   cmake --build build
   ```

5. Transfer the resulting `build/title.xex` to your RGH/JTAG console using the dashboard's authorized file-transfer workflow.
6. Run it, inspect `title.log` if generated, and confirm graphics, input and clean exit.
7. Only then start replacing the template's behavior with the tested **portable game code** and your Xbox 360 platform implementation.

**Deliverable:** an **original** sample XEX that runs on Xbox 360 hardware. This is still **not a PS2 game port** until reconstructed gameplay and assets have been integrated and verified.

## Workflow 6 · Verify a vertical slice

**Tools:** PC-side test runner, XSDK hardware logs, PCSX2 reference execution, optional Xenia smoke tests.

A valid first slice is a single scene containing one textured mesh, controllable camera/actor, one sound and stable frame pacing.

| Test | Reference observation | Native test |
|:--|:--|:--|
| Scene load | Known object placement | Same placement and bounds |
| Input | One button/stick action | Equivalent state change |
| Rendering | Camera and lighting | Matching axes, textures and alpha |
| Audio | Playback start and loop | Equivalent timing and loop |
| Performance | Reference pacing | Measured frame time, no stalls |
| Exit | Stable return path | Clean XEX termination and logs |

Treat Xenia as a preliminary check only: XSDK itself documents limitations where emulator behavior differs from real Xbox 360 hardware.

## Short path for absolute beginners

1. Learn to navigate **PCSX2 debugger** without changing game code.
2. Open a **synthetic** binary file in **ImHex** and define its header.
3. Create a simple parser using **Kaitai** or **Python**.
4. Recreate a basic movement rule in a PC **C++** executable.
5. Build the **XSDK hello sample** and run it on your own RGH/JTAG console.
6. Connect one portable C++ module to the Xbox sample.
7. Only then tackle a game-specific subsystem.

## Documentation and tool links

Browse [Chapter 15: Tool Directory](15-toolbox.md), [Chapter 08: Building XEX](08-build-and-xex.md), [Chapter 10: Roadmap](10-roadmap.md), and [Chapter 11: Legal Boundaries](11-legal.md).
