# Architecture

The repository is a documentation-first monorepo. Each `skills/<name>` folder
is an independent capability with a small trigger description and a procedural
body. Heavy detail is loaded only from a directly linked `references/` file.

The v0.4.0 runnable layer is deliberately small. The synthetic contracts under
`examples/synthetic-tunnel-review/` are read by `abaqus_agent_demo.contract`,
checked by `abaqus_agent_demo.checks`, and rendered by
`abaqus_agent_demo.report`. The repository-root [demo command](../scripts/run_demo.py)
and [installer command](../scripts/install_skill.py) are thin entry points; they
do not import Abaqus or third-party packages.

Repository-level tests enforce the public contract: exact release membership,
front matter, required guidance sections, valid relative links, absence of
release-sensitive text, and bounded text-only files. These checks validate
packaging and safety hygiene; they do not validate finite-element physics.
Release portability and the boundary between static `abqpy` lookup and runtime
Abaqus/CAE behavior are documented in [compatibility.md](compatibility.md).

The workflow boundary is:

```text
approved intent -> explicit inputs -> static review -> optional execution
-> solver evidence -> physical review -> engineering claim
```

The demo stops after static review. Its `PASS` findings cover only declared
contract shape, names, references, steps, mesh intent, output coverage, the
declared evidence gate, and the optional schema-1.1 staged-construction and
mapped-load provenance sections when present. `REVIEW_REQUIRED` identifies a
broken dependency, staged conflict, mapping gap, or evidence shortcut;
`WARNING` identifies incomplete static information.
Neither status is a solver or physics result.

Passing an earlier stage never implies that a later stage passed. In
particular, a generated report cannot prove solver completion, convergence,
ODB interpretation, physical validity, safety, or approval of an engineering
claim.
