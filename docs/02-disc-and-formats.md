# 02 · PS2 Disc Structure and File Formats

[← Hardware architecture](01-ps2-architecture.md) · [Next: Investigation →](03-reverse-engineering.md)

> **Goal:** Create a trustworthy inventory of the executable, modules, assets and data layouts before writing a port.

## No universal PS2 game layout

A PlayStation 2 game disc often includes a filesystem, a startup configuration and some combination of EE executables, IOP modules, cutscenes, sound archives, textures, models and proprietary resource packs. Names and extensions vary from title to title.

**Illustrative example only:**

```text
GAME_DISC/
├── SYSTEM.CNF
├── SLUS_123.45                 # Main EE executable (example)
├── MODULES/
│   └── EXAMPLE.IRX             # IOP module (example)
├── DATA/
│   ├── LEVEL00.BIN
│   ├── MODELS.PAK
│   └── TEXTURES.DAT
├── AUDIO/
│   ├── VOICE.AFS
│   └── EFFECT.VAG
└── MOVIE/
    └── INTRO.PSS
```

Do not assume every game uses this structure or that file extensions are always accurate.

## Understand SYSTEM.CNF

On many discs, `SYSTEM.CNF` includes a `BOOT2` entry:

```ini
BOOT2 = cdrom0:\SLUS_123.45;1
VER = 1.00
VMODE = NTSC
```

The text above is **synthetic**. Read the actual game's boot configuration to identify the exact executable. Regional serial prefixes can differ.

## Common file categories

| Name / extension | General use | Porting investigation |
|---|---|---|
| `SYSTEM.CNF` | Boot configuration | Locate entry executable |
| PS2 ELF or serial-named executable | EE machine code | Sections, entrypoint, functions |
| `.IRX` | IOP modules | Service APIs and EE communication |
| `.BIN`, `.DAT`, `.PAK` | Game-dependent data/archives | Signatures, offsets, compression |
| `.VAG` or `.ADS` | Possible audio formats | Codec, sampling, loops |
| `.AFS` | Often audio/resource archive | Table and contained resources |
| `.PSS` | Common PS2 cutscene container | Demuxing and playback timing |

## Inventory process

1. Make a permitted backup of your disc and keep it offline or private.
2. Record the SHA-256 hash, disc identifier, region and revision.
3. Extract or list the filesystem with a suitable ISO tool.
4. Read `SYSTEM.CNF` and identify main executable(s).
5. Identify other ELF/IRX-like files, tables, compressed sections and archives.
6. Record paths, lengths and header signatures.
7. Write down hypotheses without claiming they are verified.
8. Compare resource changes against observed events in the actual game.

Example **metadata-only** worksheet:

| Path | Size | Header bytes | Guess | Confidence |
|---|---:|---|---|---|
| `DATA/LEVEL00.BIN` | TBD | TBD | Level data | Low |
| `AUDIO/VOICE.AFS` | TBD | TBD | Audio archive | Medium |
| `MOVIE/INTRO.PSS` | TBD | TBD | Video stream | Medium |

## How to reverse engineer an unknown archive

A typical learning sequence is:

1. Compare multiple files of the same type.
2. Look for magic/version/count fields.
3. Interpret candidate integers in both endian modes.
4. Test whether offsets are relative to the beginning of the archive or entry.
5. Check alignment, compression headers and checksums.
6. Create a read-only parser with strict bounds checks.
7. Test it against **synthetic fixtures** that may be redistributed.
8. Open one extracted resource in an appropriate viewer, if permitted.

**Illustrative structure, not a real format claim:**

```text
MAGIC (4 bytes) | VERSION (u32) | COUNT (u32)
ENTRY[0]: OFFSET (u32) | LENGTH (u32)
ENTRY[1]: OFFSET (u32) | LENGTH (u32)
...
DATA BYTES
```

Every parser should reject offsets outside the file, lengths exceeding remaining bytes, overflow and unsupported versions. Never trust an asset merely because it came from a disc.

## What should be rewritten?

Usually **executable code and platform interfaces** require substantial reimplementation; original asset data can sometimes be read or converted by a compatible tool. A model, texture, soundtrack or animation does not automatically need hand-rewriting, but custom loaders and formats may require conversion.

## Chapter deliverable

A file inventory, format hypotheses, boot target, list of IOP services, risk register and no redistributed copyrighted resources.

[Next: Reverse-engineering workflow →](03-reverse-engineering.md)
