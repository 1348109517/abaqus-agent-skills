# Quickstart

This is the three-minute path from a clean clone to a reproducible, static
review report. It uses Python 3.10 or newer and the standard library only.

## 1. Clone and run the complete scenario

```bash
git clone https://github.com/1348109517/abaqus-agent-skills.git
cd abaqus-agent-skills
python scripts/run_demo.py
```

On Windows, use a short working directory close to the filesystem root if Git
reports `Filename too long`; see the [compatibility guide](compatibility.md).

The command audits the synthetic `complete` contract and writes:

```text
build/demo/complete/report.json
build/demo/complete/report.md
```

The current command prints the following summary before the report paths:

```text
Scenario: complete
Summary:
PASS: 8
WARNING: 0
REVIEW_REQUIRED: 0
```

The report also states: `Static contract review only. No Abaqus solver
execution or physical engineering validation was performed.`

## 2. Run all three scenarios

```bash
python scripts/run_demo.py --scenario complete
python scripts/run_demo.py --scenario naming-drift
python scripts/run_demo.py --scenario evidence-overreach
```

`complete` repeats the default eight-pass audit. `naming-drift` records one `C-REF-001` finding at
`loads.Gravity.region`. `evidence-overreach` records one `C-EVIDENCE-001`
finding at `evidence.engineering_claim`. These commands complete with status 0;
an expected teaching finding is not a runner failure.

To preview a safe skill copy, use the dry-run installer:

```bash
python scripts/install_skill.py abaqus-mesh --target build/install-check
```

It prints a plan and `DRY RUN: abaqus-mesh` without creating the destination.
Use `--apply` only after reviewing the plan and selecting an explicit target.

## 3. Choose a workflow and ask a bounded question

1. Choose a skill with the [selection matrix](skill-selection.md).
2. Copy its complete directory from `skills/` into your agent's skills directory,
   preserving the `SKILL.md` filename.
3. Check the [compatibility boundary](compatibility.md) for your Abaqus/CAE and
   embedded Python release.
4. Ask the agent a concrete question with model name, units, region names, step
   names, and intended evidence.
5. Review the proposed contract before authorizing model edits or solver execution.
6. Preserve logs and outputs needed to distinguish static checks, solver status,
   physical review, and any engineering claim.

Example request:

> Review why my named pressure surface becomes empty after partitioning. Diagnose only. Report the failing dependency, the evidence inspected, and the smallest reversible fix; do not run the solver.

The [demo guide](demo.md) explains the input contract, finding codes, and
report boundary. The [synthetic scenario README](../examples/synthetic-tunnel-review/README.md)
lists the committed inputs and expected non-pass findings.

Validate a clone with:

```bash
python -m unittest discover -s tests -v
```

These checks do not run Abaqus or certify model physics. A passing static report
must remain separate from solver evidence, physical review, and an engineering
claim.

