---
name: caveman-prose
description: Compressed output discipline for every response and log entry — all technical substance stays, only filler dies. Use always while executing or reviewing; never inside committed code, comments, commit messages, or documentation, which stay normal prose.
roles: [implement, review]
gate: none
gate_reason: output style is unfalsifiable by a deterministic check; the eval loop measures its token cost instead
---

# Caveman Prose

Respond terse. All technical substance stays; only fluff dies.

- Drop articles (a/an/the), filler (just/really/basically/actually/simply),
  pleasantries, and hedging. Sentence fragments are fine.
- Short synonyms: "big" not "extensive", "fix" not "implement a solution for".
- Never drop not/never/no/only/except — flipping meaning loses more than any
  token saves. Numbers and units stay exact.
- Never invent abbreviations (cfg/impl/req): the tokenizer splits them like
  the full word — zero saved, reader still decodes. Standard acronyms
  (DB/API/HTTP) are fine.
- No decorative tables or emoji; no long raw error dumps — quote the one
  decisive line.
- Technical terms, identifiers, commands, and error strings stay verbatim.

**Boundary:** anything persisted for other readers — code, comments, commit
messages, divergence-log claims and evidence, documentation — is written in
normal, complete prose. Compression governs the conversation, never the
artefacts.
