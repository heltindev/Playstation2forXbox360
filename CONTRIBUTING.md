# Contributing to Playstation2forXbox360

Thanks for helping make this reverse-engineering and porting research guide clearer and more accurate.

## What we welcome

- Corrections to technical terminology, CPU/GPU architecture or toolchain instructions.
- New examples that are original, self-contained and reproducible.
- Diagrams and UX improvements to the documentation.
- Better legal and security boundaries.
- Links to trustworthy upstream public technical references.
- Small synthetic test fixtures and independently authored parsers.

## What we do not accept

Do not contribute copyrighted PS2 game code, ISOs, extracted game assets, BIOS dumps, Xbox 360 keys, leaked proprietary SDKs, console secrets or circumvented-license content. Do not paste copyrighted decompiler output as a substitute for original explanations.

## Documentation standards

1. **English only.**
2. Use neutral, accurate wording — clearly distinguish verified behavior from hypothesis.
3. Prefer complete sentences, short sections, helpful tables, examples and practical exit criteria.
4. Link to upstream documentation for changing toolchains or APIs.
5. Keep the existing chapter numbering and previous/next navigation consistent.
6. Ensure every internal Markdown link resolves.
7. Do not claim a working game port or verified hardware result without evidence.
8. Keep examples small and label pseudocode or synthetic examples explicitly.

## Contribution workflow

1. Open an issue describing the problem and evidence.
2. Fork or branch the project.
3. Edit the relevant chapters and link dependent pages.
4. Run `python tools/check_docs.py` from the repository root.
5. Review your diff for copyrighted material, private paths and accidental binary files.
6. Submit a pull request with an explanation and the sources used.

## Recommended PR format

```markdown
### Summary
What changed?

### Evidence
Source links, tests and versions.

### Validation
Documentation checker output and any manual checks.

### Legal review
Confirmation that no third-party proprietary assets were added.
```

## Conduct

Be respectful, technically rigorous and open to correction. Focus on the evidence and the quality of the method.
