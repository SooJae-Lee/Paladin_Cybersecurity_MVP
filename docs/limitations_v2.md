# Limitations v2

1. Mock tools only. No live MCP server, no real calendar/code repo.
2. One task family (document summary) drives the main tables. Code-review and booking were infrastructure, not the n=10 tables.
3. Main language table is n=10. Vendor and paraphrase tables are n=5 and n=10. Do not treat those rates as population parameters.
4. Detector similarity is character 3-gram cosine (lexical), not an embedding model.
5. Partial independence: goal terms are banned from the detector, but resisted labels and detector refusal cues still overlap. Call this partial, not full, independence.
6. Automatic labels are brittle to Korean particles. One audited no_effect case was a hijack-like rewrite. Audit coverage is still 1 inspected example plus this note; a 24-case audit remains to be finished.
7. Detector threshold 0.90 over-flags. Predicted no_effect = 1/120.
8. No claim that Paladin detects hijacking in production.
