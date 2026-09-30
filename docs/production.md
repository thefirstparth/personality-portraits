# Daily portrait production — v1.0

The current workflow is [grow-portraits](../plugins/personality-portraits/skills/grow-portraits/SKILL.md). Its linked artist and state references define production. This supersedes the earlier 21/day and independent emerging-watchlist plan.

Discover people on either Andaaza or The House of 1400; prioritise overlap. Preserve exact source evidence, canonical aliases and edition dates. Expand each specific category once per IST day with up to two sourced prominent missing people. An existing portrait can seed expansion; related nominations never recursively expand. Use a seven-day seed cooldown.

Publish at most six accepted portraits per IST day, normally four direct and two related, borrowing unused slots from qualified backlog. Reserve every image request durably before generation: twelve requests maximum per day and two per person. Persist claims, selected IDs, counters and publication outcomes in queue/runs/YYYY-MM-DD.json; repeated invocations share the ledger. Respect other active runs.

The owner has substantially settled the general design language. The updated standard is [artist.md](../prompts/artist.md). Individual trial images are still review drafts. Keep publication_enabled=false until explicit approval to publish the reviewed first batch. Never fabricate approved_by or approval_reference. Store unapproved images privately. Do not publish reference photographs.

The PNG master and metadata schema remain compatible with scripts/build_catalog.py. Rebuild catalog.json and categories.json atomically with approved assets, validate and run --check, preserve old images during replacement, and verify published bytes. WebP derivatives require an explicit extension of the catalog contract. Refreshing is manual in v1; a 90-day metadata date does not automatically launch replacement work.

This plugin is a manual host-assisted workflow using connected GitHub and image generation. It is not an independent image server. A separate scheduler can invoke it only after an end-to-end production test; no scheduler is created or activated by plugin installation. Keep the existing House of 1400/Bunty job separate. Report every run including zero additions and partial failures.
