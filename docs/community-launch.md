# Community launch guide

This guide describes a staged, evidence-based launch for v0.3.0. It is a
planning and approval document, not permission to publish. The project is an
early-stage independent repository maintained under the public alias
`1348109517`; every external post must disclose that maintainer relationship.
Do not claim adoption, production readiness, solver validation, or official
SIMULIA support unless a later release has evidence for that exact claim.

## Preconditions

Begin promotion only after a tagged release or stable default branch provides
the runnable artifacts. Before drafting a post, confirm that a fresh visitor
can clone the repository, run the standard-library demo, read both report
formats, and see the explicit boundary between static review, solver evidence,
physical review, and an engineering claim. The [quickstart](quickstart.md) and
[demo guide](demo.md) are the canonical command and output references.

Each post must link to a public release or stable default branch, never an
unmerged work branch. A post may invite a reproducible bug report, technical
feedback, or a new synthetic scenario. It may not imply that download counts,
stars, or a single static report prove engineering value.

## Four launch stages

Promotion proceeds one channel at a time:

1. **Specialist communities.** Publish a technical walkthrough to the SIMULIA
   Community. Before posting to an Abaqus or FEA subreddit, check the current
   rules and ask moderators when promotional status is unclear. Disclose the
   maintainer relationship, early-stage status, and independent-project status.
2. **Reproducible English tutorial.** Publish an original DEV Community article
   showing the synthetic contract, the naming-drift finding, and the evidence
   boundary. Ask for technical feedback, bug reports, and additional synthetic
   scenarios.
3. **Open-source and agent communities.** Share a concise, channel-specific
   version only where free open-source project posts or a self-promotion thread
   is allowed. Disclose the maintainer relationship and avoid copied mass posts.
4. **Show HN, only when ready.** Consider a Show HN submission only after a
   fresh visitor can run the nontrivial demo without signup. Follow the current
   title and participation rules. Do not ask readers or friends to upvote or
   comment.

No automatic cross-posting is in scope. Each site is a separate public action.

## Exact-post approval gate

Before any external post, prepare an approval record containing every item
below:

- exact site, channel, and current rule source;
- intended account and maintainer disclosure;
- exact title and complete body, including all links and image descriptions;
- verified release or stable-branch URL;
- exact runnable command and a reproduced output excerpt;
- allowed call to action (run the demo, report a reproducible issue, or propose
  a synthetic case); and
- proposed publication time and any moderator response.

The maintainer must approve that exact destination and exact copy after this
record is complete. Editing the site, account, title, body, links, or images
creates a new approval requirement. Do not log in, contact a moderator, publish,
or cross-post before exact-post approval.

## Engagement and evidence boundary

Allowed work includes original tutorials, specialist discussion, transparent
maintainer posts, issue responses, contributor support, and submissions to
directories that accept project proposals. The following are prohibited:

- buying, trading, or coordinating stars, votes, comments, or followers;
- fake or secondary accounts used to simulate adoption;
- unsolicited mass messages or identical cross-post spam;
- hiding the maintainer relationship;
- asking for a star as a condition of access, support, or reciprocity; and
- describing downloads, usage, ecosystem impact, or adoption without evidence.

The demo's reports are static contract-review artifacts. They do not prove that
a solver ran, that an ODB was inspected, that the model is physically valid, or
that an engineering claim is approved. Promotion copy must preserve that
boundary and must not present a synthetic example as a production result.

## Fourteen-day measurement log

The first launch cycle lasts fourteen days. Keep a short public or maintainer-
reviewed launch log with the release URL, channels, publication dates, and
corrections. Measure the following without manufacturing activity:

- reproducible bug reports and substantive comments;
- new synthetic use cases or contribution proposals;
- forks and pull requests;
- release or repository traffic when GitHub makes it available; and
- stars as one secondary discovery signal, never as proof of engineering value.

Report results factually, including zero activity. A quiet channel is a signal
to improve fit or documentation, not permission to create artificial
engagement. Do not convert measurements into adoption claims.

## Release and launch checklist

- [ ] A clean clone runs `python scripts/run_demo.py` with no third-party
      dependency or Abaqus installation.
- [ ] The three scenarios produce their documented deterministic summaries and
      both report formats.
- [ ] Repository tests, link checks, and sensitive-text checks pass.
- [ ] The post identifies the maintainer, early-stage status, and independent
      project boundary.
- [ ] The exact destination, account, title, body, links, images, command,
      output excerpt, rule source, and time are recorded.
- [ ] The maintainer approved that exact post after the record was completed.
- [ ] No star, vote, comment, follower, or adoption request appears in the copy.

For contribution routes after launch, use [CONTRIBUTING](../CONTRIBUTING.md)
and the structured [issue forms](../.github/ISSUE_TEMPLATE/). Citation metadata
is in [CITATION.cff](../CITATION.cff).
