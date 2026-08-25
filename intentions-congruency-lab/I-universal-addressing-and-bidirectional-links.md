# Universal addressing and bidirectional links

*From Akien, 2026-08-23 — napkin sketch promoted to intention. Spanning: touches
db_domain, librarian/trees, and every future consumer of the database.*

## The address

A database leaf's address is `<database(per owner)>.<table>.<leaf>` — short,
typically shorter than file paths. Ownership lives in the first segment, not in a
registry lookup.

## The link tuple

Every link — database↔database and database↔file — is a **tuple of two**: the local
address and the remote address. File-side addresses use paths (which may include env
vars). The tuple is always bidirectional by construction: when something changes
address or gets voided, you traverse the reverse to update everything pointing at it.

## Two species

The database holds two species, and nothing else:

| Species | Shape | Addressing | Navigation | Mutability |
|---|---|---|---|---|
| **Trees** | one tree per table | by leaf (derived from embedding) | vector proximity | dynamic |
| **Lists** | one table per kind | by row number (positional) | link tuple reverse | static: void-and-reuse, never delete |

**Nodes** are one table. **Trees** are always one tree per table (already true — each
consumer owns its leaf table). Everything else — **embeddings**, **blobs**, **records**
(anything held for external use, like scanned receipts) — are lists. Only trees are
really dynamic.

## Embeddings are a list

Embeddings are derived and static. With the embedding and its metadata you have fast
search, but any other search by a generated ID is slow. So: use row number as the ID
(positional, O(1)). The traditional flaw — orphaned references when a row is voided —
is solved by the link tuple's reverse traversal.

## Non-binary blob format

`{LINKS: {l1 tuple, l2 tuple, ...}, <whatever else>}` — links are first-class in the
record, not metadata bolted on.

## Why the link tuple is load-bearing

The bidirectional link is not a convenience for provenance — it is what makes
positional addressing safe for the fixed lists. When you void a row, the tuple's
reverse tells you who is pointing here. **Provenance is a free side effect of solving
the orphan problem.** This fortifies provenance for free.

## What already exists

Most of this is already built. The schema has nodes/embeddings/leaves/links, the
ownership registry exists, leaf tables are one-per-tree. This codifies what is there
and makes it universal.

## Traces to

- Law 6 — ownership in the address, not a lookup
- Law 4 — bidirectional links are physics; orphan safety is structural, not policy
- Law 1 — provenance derived from the link structure, never re-derived
