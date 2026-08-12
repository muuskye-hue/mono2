<!--
Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- Modified principles:
  - I–VI retained; each rewritten into Rationale / Rule / How To Apply
  - (added) VII. Recovery Over Prevention
  - (added) VIII. Attention Is Finite
  - (added) IX. Value Is Realized at the User, Not at Merge
  - (added) X. Commands Are Discoverable; Local Dev Matches CI
- Added sections: none (Domain Scope + Review Checklist retained, expanded)
- Removed sections: none
- Follow-up TODOs: none
-->

# mono2 Constitution

## Core Principles

### I. Do Not Distribute by Default

**Rationale**: Distribution multiplies failure modes. Every new process,
service, or queue adds coordination cost measured in round trips, partial
failure, and operational surface — not in claimed milliseconds. Vertical
scaling and a single deployable remain cheaper until a named constraint
forces otherwise.

**Rule**: A single deployable process is the default. Vertical scaling is
the first response to load. A change MUST NOT introduce a new process,
service, queue, RPC client, or network hop unless the PR description cites
exactly one justification and names the measured constraint:

1. Working-set overflow (memory/CPU that cannot fit one machine)
2. Genuinely independent compute (workload-required failure/isolation
   boundary, not team preference)
3. Geographic latency (users or data that require regional placement)
4. Organizational independence (separate release, ownership, or trust
   boundary)

Coordination cost MUST be counted in round trips and failure modes.

**How To Apply**: Reject any diff that adds a service split, message queue,
RPC boundary, or multi-process deploy without that written justification.
Point at the new process/queue/client and say "violates I — no allowed
justification." Prefer one binary, one deploy unit, one machine until the
PR proves otherwise.

### II. Optimize for Deletion, Not Extension

**Rationale**: Speculative abstractions outlive their authors and resist
removal. A module small enough to delete and rewrite in a day keeps the
codebase malleable. Duplication below three occurrences is cheaper than the
wrong shared layer.

**Rule**: Every module MUST be small enough that one engineer can delete
and rewrite it in one day. Speculative abstractions — generic base classes,
plugin frameworks, premature interfaces, "for future use" indirection —
MUST be rejected. Inline until duplication hurts, then extract. Extracting
a shared helper on the first or second occurrence violates this principle
unless the abstraction already exists and is proven.

**How To Apply**: Reject unused extension points, one-implementation
interfaces, and frameworks "to make it flexible later." Point at the new
abstraction with fewer than three call sites and say "violates II —
premature extraction." Prefer deletion of the module over extending it.

### III. Make Dependencies Explicit

**Rationale**: Hidden coupling and import-time side effects make behavior
non-local. A reader who cannot see dependencies in the signature or file
header cannot reason about blast radius, testability, or ownership.

**Rule**: No hidden coupling. No implicit global state. No import-time side
effects. A reader MUST be able to see every dependency of a function in its
signature or at the top of its file. Prefer dependency injection over
singletons.

**How To Apply**: Reject diffs that read/write process-global mutable
state, perform I/O or configuration binding at import time, or reach into
another module's private internals without declaring the dependency. Point
at the global, singleton, or import side effect and say "violates III —
dependency not explicit."

### IV. Contract at the Boundary, Not in the Middle

**Rationale**: Semantic drift between producers and consumers is inevitable.
Versioned schemas at the edge localize that drift. Shared mutable schemas
in the middle couple unrelated callers and make safe evolution impossible.

**Rule**: Every producer/consumer boundary — HTTP, queue, file, database,
or external API — MUST have a versioned schema. Semantic reconciliation
happens only at the boundary and is owned by the side that understands both
contexts. Shared mutable schemas across internal middle layers are
forbidden.

**How To Apply**: Reject a new or changed cross-boundary payload without a
schema and version. Reject in-place mutation of a shared schema consumed by
multiple parties without an owned boundary adapter. Point at the unversioned
payload or shared middle schema and say "violates IV — contract missing or
misplaced."

### V. Test the Transformation, Not the Plumbing

**Rationale**: Tests that assert mocked call graphs of owned code prove
nothing about behavior. Pure transformations and real boundaries are where
defects live. A "green" CI without a regression for the bug just fixed is
theater.

**Rule**: Unit tests MUST cover pure transformation logic. Integration
tests MUST cover boundaries (I/O, schemas, external systems). Do not mock
what you own; do mock what you do not. A bug fix without a failing
regression test that first reproduces the bug is incomplete.

**How To Apply**: Reject tests that only verify owned mocks were called.
Reject bug-fix PRs that lack a failing-then-passing regression test.
Point at the mock-heavy unit test or missing regression and say "violates
V — tested plumbing, not transformation" or "violates V — no reproducing
test."

### VI. Emit Structured Events, Derive Everything Else

**Rationale**: Unstructured logs cannot be aggregated, joined, or audited
reliably. Logs, metrics, and traces that diverge become three truths.
One structured event stream keeps observability coherent and searchable.

**Rule**: Logs, metrics, and traces are projections of one primitive: the
structured event. New code MUST emit structured events, not free-form
strings. High-cardinality fields — at minimum `user_id`, `request_id`,
`tenant_id`, and feature-flag state when applicable — are REQUIRED on
request-path events.

**How To Apply**: Reject unstructured log lines in new code. Reject a
metric or trace that cannot be derived from the structured event stream
without a justified exception in the PR. Point at the string log or missing
high-cardinality field and say "violates VI — not a structured event."

### VII. Recovery Over Prevention

**Rationale**: Prevention fails under novel conditions. Systems that cannot
revert fast accumulate irreversible risk. Expand-then-contract migrations
and tested rollbacks keep production recoverable when assumptions break.

**Rule**: Every change MUST be revertible in under five minutes without a
code change. Feature flags MUST gate risky paths. Migrations MUST follow
expand-then-contract. Rollback MUST be tested as part of the deploy, not
assumed.

**How To Apply**: Reject deploys that require a hotfix commit to undo.
Reject schema changes that are not expand-then-contract. Reject risky
paths shipped without a feature flag. Point at the irreversible migration
or unflagged risky path and say "violates VII — not revertible in five
minutes without a code change."

### VIII. Attention Is Finite

**Rationale**: Alerts without user impact train teams to ignore pages.
Decorative dashboards consume attention without decision value. Unused
signals are liability, not coverage.

**Rule**: Every alert MUST correspond to a user-visible symptom and a
runbook. Dashboards are saved queries, not decoration. Delete signals that
have not fired a useful page in 90 days.

**How To Apply**: Reject new alerts that lack a user-visible symptom and a
linked runbook. Reject dashboard-only "monitoring" without an actionable
signal. Point at an alert or dashboard widget with no runbook / no useful
page in 90 days and say "violates VIII — attention without action."

### IX. Value Is Realized at the User, Not at Merge

**Rationale**: Merge is an internal milestone. Users experience deployed,
instrumented, monitored behavior. A change that is merged but not shipped
and observable delivers no value and cannot be validated.

**Rule**: A PR is not done until the change is in users' hands, observable,
and revertible. "Shipped" means deployed, instrumented, and monitored —
not merged.

**How To Apply**: Reject "done" claims that stop at merge. Require evidence
of deploy, instrumentation (structured events per VI), and monitoring
before closing the work. Point at a merged-but-undeployed or
uninstrumented change and say "violates IX — not shipped."

### X. Commands Are Discoverable; Local Dev Matches CI

**Rationale**: Hidden arguments and CI-only steps create "works on my
machine" gaps. A single, listed command interface makes build, test, lint,
migrate, deploy, and seed reproducible for every contributor.

**Rule**: Every repeatable action (build, test, lint, migrate, deploy,
seed) MUST be a single named command listed in one place and runnable with
no hidden arguments. The command a developer runs locally MUST be the same
command CI runs. No CI-only shell steps. No undocumented makefile targets.
If a new contributor cannot list every command in 30 seconds, the interface
is broken.

**How To Apply**: Reject CI steps that are not exposed as the same local
command. Reject new scripts that are not listed in the single command
catalog. Point at a CI-only step or undocumented target and say "violates
X — command not discoverable / local≠CI."

## Domain Scope

These principles are the first-principles baseline across five domains.
Reviews MUST apply the matching principle when the diff touches that domain:

| Domain | Primary principles |
| --- | --- |
| Distributed systems | I, IV, VII |
| Software design | II, III |
| Data engineering | IV, V |
| DevOps | I, VII, IX, X |
| Observability | VI, VIII |

A change may be constrained by more than one principle. When principles
conflict, prefer the more restrictive rule and document the trade-off in
the PR.

## Review Checklist

Every PR review MUST be able to cite a principle by number without
interpretation. Use these mechanical checks:

- **I**: Does this diff add a process, service, queue, or RPC? If yes,
  where is the written justification naming one allowed reason?
- **II**: Can one engineer rewrite each touched module in a day? Is there
  a new abstraction with fewer than three call sites?
- **III**: Are all dependencies visible in signatures or file-top imports?
  Any globals, singletons, or import-time side effects?
- **IV**: Does every new/changed boundary have a versioned schema? Any
  shared mutable schema in the middle?
- **V**: Pure logic covered by unit tests? Boundaries by integration
  tests? Bug fixes include a reproducing regression test?
- **VI**: Is new telemetry structured events with required high-cardinality
  fields? No new unstructured log lines?
- **VII**: Is the change revertible in under five minutes without a code
  change? Risky paths flagged? Migrations expand-then-contract? Rollback
  tested in deploy?
- **VIII**: Does every new alert map to a user-visible symptom and a
  runbook? Any signal unused for 90 days that should be deleted?
- **IX**: Is the change deployed, instrumented, and monitored — not merely
  merged?
- **X**: Is every repeatable action a single listed command identical in
  local and CI?

A reviewer pointing at a hunk and saying "this violates principle X" MUST
be sufficient. If a rule cannot be applied that way, the constitution
itself is defective and MUST be amended.

## Governance

This constitution supersedes informal practice, style preference, and
ad-hoc architecture decisions. Ambiguity is resolved in favor of the
stricter reading.

Amendments MUST:

1. Update `.specify/memory/constitution.md` with a Sync Impact Report
2. Bump `CONSTITUTION_VERSION` using semver (MAJOR: remove/redefine;
   MINOR: add/expand; PATCH: clarify)
3. Set `Last Amended` to the amendment date (ISO `YYYY-MM-DD`)
4. Land through PR review that cites the changed principles

Compliance:

- PR authors MUST self-check the Review Checklist before requesting review
- Reviewers MUST reject changes that violate a principle unless the PR
  records an explicit, time-bounded exception with an owner and removal
  plan
- Complexity, distribution, and new abstractions require justification in
  the PR body; silence is non-compliance

**Version**: 1.1.0 | **Ratified**: 2026-08-12 | **Last Amended**: 2026-08-12
