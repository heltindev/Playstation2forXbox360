# Security and Responsible Disclosure

This repository is **documentation**, not a supported commercial software distribution.

## Reporting vulnerabilities

If you find a vulnerability in a script or fixture added to this project, please open a GitHub issue **only if the report does not expose secrets or enable immediate harm**. For sensitive cases, contact the maintainer privately using a secure channel listed in their GitHub profile or repository settings, if available.

## Scope

- Parser bounds, integer overflow and memory-safety problems.
- Unexpected command execution in build or documentation tools.
- Malicious paths, unsafe archive extraction or unsafe network use.
- Accidental exposure of secrets, proprietary assets or personal data.

## Out of scope

Exploit instructions against commercial consoles or online services, copied account data, keys, BIOS files and proprietary SDK binaries are not requested or needed.

## Defensive practices

- Validate all lengths, offsets, versions and counts in binary parsers.
- Use synthetic test inputs for public reproduction.
- Never commit credentials or copyrighted disc assets.
- Treat external code, scripts and dependencies as untrusted until reviewed.

No formal response-time SLA or security warranty is offered.
