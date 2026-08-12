<!--
Sync Impact Report
- Version change: (template placeholders) → 1.0.0
- Modified principles:
  - [PRINCIPLE_1_NAME] → I. Do Not Distribute by Default
  - [PRINCIPLE_2_NAME] → II. Optimize for Deletion, Not Extension
  - [PRINCIPLE_3_NAME] → III. Make Dependencies Explicit
  - [PRINCIPLE_4_NAME] → IV. Contract at the Boundary, Not in the Middle
  - [PRINCIPLE_5_NAME] → V. Test the Transformation, Not the Plumbing
  - (added) VI. Emit Structured Events, Derive Everything Else
- Added sections:
  - Domain Scope
  - Review Checklist
  - Governance (concrete amendment/compliance rules)
- Removed sections: none (replaced template placeholders)
- Follow-up TODOs: none
-->

# mono2 Constitution

## Core Principles

### I. Do Not Distribute by Default

A single deployable process is the default architecture. Vertical scaling is the
first response to load. A new process, service, queue, or network hop MUST NOT
appear in a change unless the PR description cites exactly one of these
justifications and names the measured constraint:

1. Working-set overflow (memory/CPU that cannot fit one machine)
2. Genuinely independent compute (failure/isolation boundary required by the
   workload, not by team preference)
3. Geographic latency (users or data that require regional placement)
4. Organizational independence (separate release, ownership, or trust boundary)

Coordination cost MUST be counted in round trips and failure modes, not in
claimed millisecond savings. A diff that adds a service split, message queue,
RPC client, or multi-process deploy WITHOUT that written justification violates
this principle.

### II. Optimize for Deletion, Not Extension

Every module MUST be small enough that one engineer can delete and rewrite it
in one day. Speculative abstractions (generic base classes, plugin frameworks,
premature interfaces, "for future use" indirection) MUST be rejected.

Inline until duplication hurts, then extract. Duplication below three
occurrences is cheaper than the wrong abstraction; extracting a shared helper
on the first or second occurrence violates this principle unless the
abstraction already exists and is proven.

A diff that introduces an unused extension point, a one-implementation
interface, or a framework "to make it flexible later" violates this principle.

### III. Make Dependencies Explicit

No hidden coupling. No implicit global state. No import-time side effects.
A reader MUST be able to see every dependency of a function in its signature
or at the top of its file.

Prefer dependency injection over singletons. A diff that reads or writes
process-global mutable state, performs I/O or configuration binding at import
time, or reaches into another module's private internals without declaring the
dependency violates this principle.

### IV. Contract at the Boundary, Not in the Middle

Every producer/consumer boundary — HTTP, queue, file, database, or external
API — MUST have a versioned schema. Semantic reconciliation happens only at
the boundary and is owned by the side that understands both contexts.

Shared mutable schemas across internal middle layers are forbidden. A diff
that adds or changes a cross-boundary payload without a schema and version,
or that mutates a shared schema in place for multiple consumers without an
owned boundary adapter, violates this principle.

### V. Test the Transformation, Not the Plumbing

Unit tests MUST cover pure transformation logic. Integration tests MUST cover
boundaries (I/O, schemas, external systems). Do not mock what you own; do mock
what you do not.

A bug fix without a failing regression test that first reproduces the bug is
not complete. A green CI that lacks that failing-then-passing test for the
fixed bug violates this principle. Tests that only assert mocked call graphs
of owned code, without asserting transformed outputs or boundary contracts,
violate this principle.

### VI. Emit Structured Events, Derive Everything Else

Logs, metrics, and traces are projections of one primitive: the structured
event. New code MUST emit structured events (not free-form strings). High-
cardinality fields — at minimum `user_id` / `request_id` / `tenant_id` /
feature-flag state when applicable — are REQUIRED on request-path events, not
optional.

Unstructured log lines in new code violate this principle. Adding a metric or
trace that cannot be derived from the same structured event stream without a
justified exception in the PR description violates this principle.

## Domain Scope

These principles are the first-principles baseline across five domains. Reviews
MUST apply the matching principle when the diff touches that domain:

| Domain | Primary principles |
| --- | --- |
| Distributed systems | I, IV |
| Software design | II, III |
| Data engineering | IV, V |
| DevOps | I, III, V |
| Observability | VI |

A change may be constrained by more than one principle. When principles
conflict, prefer the more restrictive rule and document the trade-off in the
PR.

## Review Checklist

Every PR review MUST be able to cite a principle by number without
interpretation. Use these mechanical checks:

- **I**: Does this diff add a process, service, queue, or RPC? If yes, where
  is the written justification naming one allowed reason?
- **II**: Can one engineer rewrite each touched module in a day? Is there a
  new abstraction with fewer than three call sites?
- **III**: Are all dependencies visible in signatures or file-top imports?
  Any globals, singletons, or import-time side effects?
- **IV**: Every new/changed boundary have a versioned schema? Any shared
  mutable schema in the middle?
- **V**: Pure logic covered by unit tests? Boundaries by integration tests?
  Bug fixes include a reproducing regression test?
- **VI**: New telemetry is structured events with required high-cardinality
  fields? No new unstructured log lines?

A reviewer pointing at a hunk and saying "this violates principle X" MUST be
sufficient. If a rule cannot be applied that way, the constitution itself is
defective and MUST be amended.

## Governance

This constitution supersedes informal practice, style preference, and ad-hoc
architecture decisions. Ambiguity is resolved in favor of the stricter reading.

Amendments MUST:

1. Update `.specify/memory/constitution.md` with a Sync Impact Report
2. Bump `CONSTITUTION_VERSION` using semver (MAJOR: remove/redefine; MINOR:
   add/expand; PATCH: clarify)
3. Set `Last Amended` to the amendment date (ISO `YYYY-MM-DD`)
4. Land through PR review that cites the changed principles

Compliance:

- PR authors MUST self-check the Review Checklist before requesting review
- Reviewers MUST reject changes that violate a principle unless the PR
  records an explicit, time-bounded exception with an owner and removal plan
- Complexity, distribution, and new abstractions require justification in the
  PR body; silence is non-compliance

**Version**: 1.0.0 | **Ratified**: 2026-08-12 | **Last Amended**: 2026-08-12
