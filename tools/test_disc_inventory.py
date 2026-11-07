"""Self-contained tests using ONLY synthetic temporary files."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name("disc_inventory.py")
spec = importlib.util.spec_from_file_location("disc_inventory", MODULE)
assert spec is not None and spec.loader is not None
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class InventoryTests(unittest.TestCase):
    def test_boot_target_and_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "SYSTEM.CNF").write_text(
                "BOOT2 = cdrom0:\\SLUS_123.45;1\nVER = 1.00\n",
                encoding="ascii",
            )
            (root / "SLUS_123.45").write_bytes(b"\x7fELF" + b"\x00" * 12)
            result = inventory.scan_folder(root, calculate_hash=True)
            self.assertEqual(result["file_count"], 2)
            self.assertTrue(result["boot"]["exists"])
            self.assertEqual(result["boot"]["executable_path"], "SLUS_123.45")
            executable = next(e for e in result["files"] if e["path"] == "SLUS_123.45")
            self.assertEqual(executable["type_guess"], "ELF signature")
            self.assertEqual(len(executable["sha256"]), 64)

    def test_missing_boot_config(self):
        with tempfile.TemporaryDirectory() as temp:
            result = inventory.scan_folder(Path(temp), calculate_hash=False)
            self.assertEqual(result["file_count"], 0)
            self.assertIsNone(result["boot"]["config"])

    def test_boot_does_not_accept_parent_traversal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "system.cnf").write_text("BOOT2 = cdrom0:\\..\\outside;1\n")
            result = inventory.scan_folder(root, calculate_hash=False)
            self.assertIsNone(result["boot"]["executable_path"])
            self.assertFalse(result["boot"]["exists"])

    def test_input_must_be_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            file_path = root / "image.iso"
            file_path.write_bytes(b"not an iso")
            with self.assertRaises(ValueError):
                inventory.scan_folder(file_path, calculate_hash=False)


if __name__ == "__main__":
    unittest.main()
