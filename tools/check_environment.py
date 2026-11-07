#!/usr/bin/env python3
"""Report command-line prerequisites for PS2 research and XSDK builds.

No installation, downloads, remote requests or hardware probes are performed.
A missing PATH entry is not proof that a GUI app is uninstalled.
"""
from __future__ import annotations

import platform
import shutil
import sys
from pathlib import Path

CHECKS = [
    ("Git", "git", "https://git-scm.com/"),
    ("CMake", "cmake", "https://cmake.org/"),
    ("Ninja", "ninja", "https://ninja-build.org/"),
    ("FFmpeg", "ffmpeg", "https://ffmpeg.org/"),
    ("ffprobe", "ffprobe", "https://ffmpeg.org/"),
    ("Binwalk", "binwalk", "https://github.com/ReFirmLabs/binwalk"),
    ("Kaitai compiler", "ksc", "https://kaitai.io/"),
    ("PowerPC XSDK compiler", "powerpc-xsdk-elf-gcc", "https://github.com/xenosworks/xsdk"),
]


def check_tools() -> list[tuple[str, str, str]]:
    return [(name, shutil.which(program) or "not on PATH", link)
            for name, program, link in CHECKS]


def main() -> int:
    print("PS2 -> Xbox 360 local tool readiness")
    print(f"Host: {platform.system()} {platform.release()}, Python {sys.version.split()[0]}")
    print("Results inspect command-line PATH only. Nothing is installed or executed.\n")
    for name, executable, link in check_tools():
        print(f"{name:<24} {executable}")
        if executable == "not on PATH":
            print(f"{'':24} Source: {link}")
    print("\nGUI tools (PCSX2, Ghidra, ImHex) may be installed outside PATH.")
    if platform.system() == "Windows":
        print("For XSDK, run this checker inside WSL/Linux; the compiler is usually not on Windows PATH.")
    else:
        xsdk_default = Path.home() / "xsdk-gcc" / "bin" / "powerpc-xsdk-elf-gcc"
        print(f"Common Linux XSDK prefix: {xsdk_default}")
        print(f"Present at expected prefix: {'yes' if xsdk_default.is_file() else 'not detected'}")
    print("Successful detection does not prove a program works or supports your target.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
