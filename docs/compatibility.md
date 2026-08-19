# Compatibility and public-use boundary

This repository contains clean-room workflow guidance for Abaqus/CAE
automation. The skills are written to be useful across releases, but an API
signature, keyword, output variable, or solver behavior can still be
release-specific and must be checked in the target environment.

## Compatibility layers

| Layer | What this repository supports | What it does not claim |
|---|---|---|
| Skill documents | Planning and reviewing workflows around named regions, steps, fields, loads, mapped-load provenance, staged construction, meshes, interactions, outputs, and ODBs | Equivalent runtime behavior across every Abaqus/CAE release |
| Abaqus Python and abqpy | Static lookup, type hints, and version-aware authoring when the installed reference matches the target release | That an external type hint can execute inside every embedded solver Python |
| Repository tests | Python 3.10+ structural, link, privacy, routing, contract, and documentation checks without Abaqus | Solver convergence, physical correctness, or mesh independence |
| Runtime actions | Read-only inspection and dry-run planning before an approved mutation | Implicit CAE/ODB writes, job submission, or engineering sign-off |

## Porting a skill to a new release

1. Record the Abaqus/CAE release, embedded Python version, and optional abqpy
   reference used for static checks.
2. Verify object names, arguments, output-variable availability, and region
   behavior in the target environment.
3. Keep read-only checks and dry-run descriptions separate from authorized
   model changes.
4. Run the repository tests, including the schema-1.1 synthetic contract
   scenarios, and document any release-specific exception in a review note or
   pull request.
5. Obtain an independent engineering review before using a result as evidence.

## Windows checkout paths

Some Windows Git installations still enforce the traditional path-length
limit. If checkout reports `Filename too long`, clone the repository into a
short working directory close to the filesystem root, or enable long-path
support through your organization's approved Windows and Git policy. Moving
to a short parent is the smallest reversible workaround and does not change
repository content. The v0.4.0 checkout is clean-clone tested from a short Windows
path.

## Public-data boundary

Examples and documentation must remain synthetic or intentionally shareable.
Do not add real CAE/ODB files, private project paths, credentials, API keys,
manuscripts, proprietary geometry, or unreviewed engineering data.
