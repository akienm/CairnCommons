# 6ba77d0e0c32: d12fd9781fb6's proof over the corpus tree (2026-11-12)

Run: python3 cairn/devices/codemother/proofs/test_codemother_holds_the_librarians_questions.py, after the build. _corpus reads every key of librarian_cross_domain_questions (store.read) and each newest leaf (trees.find); tooth 5 asserts trees.find + CROSS_DOMAIN_QUESTIONS and no corpus-module import. Clauses 1-6 keep their claims; only the reading changed.

```
  ok   test_her_file_carries_no_corpus_text
  ok   test_every_held_id_resolves_and_the_five_missing_are_held
  ok   test_a_dry_seed_lands_the_corpus_text
  ok   test_an_unknown_held_id_is_loud
  ok   test_seed_reaches_the_corpus_only_through_the_module
  ok   test_every_held_entry_carries_its_origin
6/6 green
```
