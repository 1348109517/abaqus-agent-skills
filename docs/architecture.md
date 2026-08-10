# Architecture

The repository is a documentation-first monorepo. Each `skills/<name>` folder
is an independent capability with a small trigger description and a procedural
body. Heavy detail is loaded only from a directly linked `references/` file.

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

Passing an earlier stage never implies that a later stage passed.
