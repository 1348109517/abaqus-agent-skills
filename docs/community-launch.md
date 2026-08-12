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

## Verified v0.3.0 launch facts

The tagged release is
<https://github.com/1348109517/abaqus-agent-skills/releases/tag/v0.3.0>.
Post-merge validation reproduced the three documented summaries: `complete`
reported 8 `PASS`, 0 `WARNING`, and 0 `REVIEW_REQUIRED`; both `naming-drift`
and `evidence-overreach` reported 7 `PASS`, 0 `WARNING`, and 1
`REVIEW_REQUIRED`. The default-branch workflow passed on Ubuntu and Windows
with Python 3.10 and 3.12.

Channel-specific drafts and gates are recorded separately:

- [SIMULIA Community draft](launch/v0.3.0-simulia-draft.md)
- [DEV Community tutorial draft](launch/v0.3.0-devto-draft.md)
- [Open-source community draft](launch/v0.3.0-oss-community-draft.md)
- [Show HN readiness review](launch/v0.3.0-show-hn-readiness.md)

These files are review artifacts, not publication authorization. An intended
account value of `REVIEW_REQUIRED` or a rule state of `SOURCE_UNAVAILABLE`
blocks the related external action.

## Four launch stages

Promotion proceeds one channel at a time:

1. **Specialist communities.** Publish a technical walkthrough to the SIMULIA
   Community. Check the current rules before posting. If promotional status is
   unclear, use the separate moderator-inquiry action below before preparing a
   final post. Disclose the maintainer relationship, early-stage status, and
   independent-project status.
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

## Separate external-action approval gates

Moderator contact and public publication are two different external actions.
Neither action is sent automatically, and approval for one action never
authorizes the other.

### Action A: moderator inquiry

Use this action only when a site's current rules do not make promotional status
clear. Prepare an exact-action approval packet containing:

- the exact site and channel;
- the account that would send the inquiry;
- the intended moderator or other exact recipient;
- the complete inquiry text, including any links or attachments; and
- the proposed time to send it.

The maintainer must approve this exact inquiry packet before the inquiry is
sent. The approval authorizes only that inquiry; it does not authorize a public
post or a cross-post. After a response, record the response date, recipient,
exact rule evidence or response text, and any resulting posting constraint.

### Action B: final public post

After Action A when an inquiry was needed, prepare a second exact-post approval
packet containing every item below:

- exact site, channel, and current rule source;
- intended account and maintainer disclosure;
- exact title and complete body, including all links and image descriptions;
- verified release or stable-branch URL;
- exact runnable command and a reproduced output excerpt;
- allowed call to action (run the demo, report a reproducible issue, or propose
  a synthetic case);
- the recorded moderator response evidence, when Action A was used; and
- proposed publication time.

The maintainer must approve this second exact destination and exact copy after
the Action A response evidence is included. Editing the site, account,
recipient, title, body, links, images, or timing creates a new approval
requirement. Only the approved final post may be sent; no moderator inquiry,
publication, or cross-post is automatic.

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

- [x] A clean clone runs `python scripts/run_demo.py` with no third-party
      dependency or Abaqus installation.
- [x] The three scenarios produce their documented deterministic summaries and
      both report formats.
- [x] Repository tests, link checks, and sensitive-text checks pass for the
      tagged release and the launch-draft branch.
- [ ] The post identifies the maintainer, early-stage status, and independent
      project boundary.
- [ ] If rules were unclear, the Action A moderator-inquiry packet named the
      site, sending account, exact recipient, exact inquiry text, and time;
      the maintainer approved it before it was sent.
- [ ] If Action A was used, its response date, recipient, and exact rule
      evidence or response text are recorded.
- [ ] The Action B final-post packet records the exact destination, account,
      title, body, links, images, command, output excerpt, rule source,
      response evidence when applicable, and time.
- [ ] The maintainer gave a second approval for that exact Action B post after
      the response evidence was included.
- [ ] No moderator inquiry, publication, or cross-post was sent automatically.
- [ ] No star, vote, comment, follower, or adoption request appears in the copy.

For contribution routes after launch, use [CONTRIBUTING](../CONTRIBUTING.md)
and the structured [issue forms](../.github/ISSUE_TEMPLATE/). Citation metadata
is in [CITATION.cff](../CITATION.cff).
