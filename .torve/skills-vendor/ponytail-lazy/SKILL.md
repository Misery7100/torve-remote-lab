---
name: ponytail-lazy
description: The laziest solution that actually works — a decision ladder run before writing any code. Use on every implementation task; not a license to skip understanding the contract, the tree, or the acceptance battery first.
roles: [implement]
gate: none
gate_reason: minimality is judged by review and by the diff, not by a deterministic check
---

# Ponytail: the lazy ladder

Read the contract and the code it touches first — laziness shortens the
solution, never the reading. Then climb, stopping at the first rung that
holds:

1. **Does this need to exist at all?** Speculative need — skip it, say so
   in one line.
2. **Already in this codebase?** A helper, util, or pattern that already
   lives here is reused, never re-implemented. Look before you write —
   re-implementing what sits a few files over is the commonest slop.
3. **Stdlib does it?** Use it.
4. **An installed dependency does it?** Use it. Never add a new one for
   what a few lines cover.
5. **Can it be one line?** One line.
6. **Only then:** the minimum code that works.

Rules that ride the ladder:

- No abstractions the contract did not ask for: no interface with one
  implementation, no config for a value that never changes, no scaffolding
  "for later".
- The shortest working diff wins — but the smallest change in the wrong
  place is a second bug, not laziness. Root cause over symptom: grep every
  caller before patching one path.
- A deliberate shortcut with a known ceiling gets a `ponytail:` comment
  naming the ceiling and the upgrade path.
- Non-trivial logic leaves one runnable check behind — the smallest thing
  that fails if the logic breaks. Trivial one-liners need none.
- Never simplify away: input validation at trust boundaries, error handling
  that prevents data loss, security, or anything the contract names.
