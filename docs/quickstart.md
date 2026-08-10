# Quickstart

1. Choose a skill with the [selection matrix](skill-selection.md).
2. Copy its complete directory from `skills/` into your agent's skills directory.
3. Check the [compatibility boundary](compatibility.md) for your Abaqus/CAE and
   embedded Python release.
4. Ask the agent a concrete question with model name, units, region names, step
   names, and intended evidence.
5. Review the proposed contract before authorizing model edits or solver execution.
6. Preserve logs and outputs needed to distinguish static checks, solver status,
   and physical review.

Example request:

> Review why my named pressure surface becomes empty after partitioning. Diagnose only. Report the failing dependency, the evidence inspected, and the smallest reversible fix; do not run the solver.

Validate a clone with:

```bash
python -m unittest discover -s tests -v
```

