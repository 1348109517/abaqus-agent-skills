# Contributing

Contributions are welcome when they improve a reproducible Abaqus workflow.

1. Open an issue describing the task, evidence boundary, and intended users.
2. Keep each skill self-contained and use only `name` and `description` in its front matter.
3. Start descriptions with `Use when` and describe triggering conditions.
4. Use synthetic or clean-room examples. Do not contribute proprietary manuals,
   model files, customer data, local paths, credentials, or unlicensed text.
5. Keep examples reproducible with the documented Python standard-library
   commands. Do not require Abaqus, a license, network access, or private files
   for repository tests.
6. Add or update tests and run `python -m unittest discover -s tests -v`.
7. For a demo change, run all three scenarios and state the exact report paths
   and finding summaries that you inspected.
8. Explain in the pull request what was verified and what still requires
   Abaqus, solver evidence, physical review, or qualified engineering review.

## Evidence and data boundary

The runnable demo performs deterministic static contract checks only. A
`PASS` finding does not establish solver completion, numerical convergence,
physical validity, or an approved engineering claim. Keep those stages
separate in issue descriptions, reports, examples, and pull requests. Do not
turn a synthetic contract or generated report into evidence about a real
project.

Before opening a pull request, use the [pull-request template](.github/pull_request_template.md)
and complete its clean-room and validation checkboxes. The [issue forms](.github/ISSUE_TEMPLATE/)
provide separate routes for bugs, skill proposals, and synthetic examples.

## Synthetic examples

New contracts should use invented identifiers and values, document their
expected static findings, and include a short explanation of the intended
workflow boundary. Remove real paths and project-specific data before sharing.
If a proposed example needs a solver, ODB, field interpretation, or engineering
decision, describe that as a follow-up evidence gate rather than claiming it is
covered by the demo.

## Compatibility evidence

When a contribution discusses a release-specific Abaqus/CAE API, identify the
release and separate documentation lookup from runtime behavior. Preserve the
read-only and dry-run boundaries described in [compatibility.md](docs/compatibility.md).
Do not state that a static check, unit test, or demo run validates finite-element
physics.

By contributing, you agree that your contribution is licensed under Apache-2.0.
