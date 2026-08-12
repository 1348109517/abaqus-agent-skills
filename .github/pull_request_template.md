## Summary

Describe the smallest reproducible change and the workflow boundary it affects.
Link an issue when one exists.

## Validation

- [ ] `python -m unittest tests.test_repository -v`
- [ ] `python -m unittest discover -s tests -v`
- [ ] For demo changes, `python scripts/run_demo.py --scenario complete --output-dir build/pr-check/complete`
- [ ] For demo changes, `python scripts/run_demo.py --scenario naming-drift --output-dir build/pr-check/naming-drift`
- [ ] For demo changes, `python scripts/run_demo.py --scenario evidence-overreach --output-dir build/pr-check/evidence-overreach`
- [ ] I recorded the exact report paths and summary counts that I inspected.

## Evidence and data boundary

- [ ] All examples, fixtures, screenshots, and logs are synthetic or clean-room.
- [ ] No proprietary manuals, model files, customer data, private paths, credentials, or unlicensed text are included.
- [ ] The change distinguishes static review from solver evidence, physical review, and an engineering claim.
- [ ] The change does not claim solver completion, physical validity, safety, production readiness, or adoption without evidence.

## Public-release hygiene

- [ ] New Markdown links resolve from their containing file.
- [ ] Generated reports and local build output are not staged unless they are intentional fixtures.
- [ ] I explained any behavior that still requires Abaqus or qualified engineering review.
