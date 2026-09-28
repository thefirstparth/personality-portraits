# Daily production rules

## Approval gate and limits

The owner explicitly requires reviewing a few portraits before finalizing the master prompt or publishing any portraits. Until config/production.json has style_approved=true and publication_enabled=true following explicit owner approval, do discovery and preparation only. Never publish review samples, references or generated images. The two initial sample outputs await review; remaining daily candidates are queued.

Target 21 accepted portraits per Asia/Kolkata day. Count approved samples toward that day's target if published that day. Count refreshes too. Persist attempted and accepted person IDs in the daily run state so resumed runs and concurrent workers cannot duplicate work. Claim one run at a time and reread remote main before publication. Stop on user quota constraints or provider limits; no paid API fallback without authorization. A 30-attempt ceiling includes failed requests and retries and does not imply 30 attempts fit the account. Report an unfilled target honestly.

## Allocation

- 12 slots: missing directly mentioned people and related established personalities.
- 4 protected slots: emerging, newly eligible or breakthrough personalities.
- Up to 5 slots: regenerate portraits whose last_generated_at is over 90 days old.
- No overdue portraits on day one: 17 established/site-driven plus 4 emerging.
- Unused refresh/emerging slots transfer to eligible new people. Never invent candidates to fill a quota.
- New additions have priority; refreshes never exceed 5. Rank refresh candidates first by mentions on both sites in the trailing 30 days, then either site, then days overdue.
- The 90-day point makes an image eligible, not a guaranteed replacement deadline. A growing library can accumulate a refresh backlog. Report it; never expand the cap silently.
- Refresh from last_generated_at, not metadata edits or a git commit timestamp. Keep the current approved image online until a replacement passes review.

## Discovery and identity

Read both live websites daily, including rendered market outcomes, tables, fixtures and article bodies. Record source page, section, source publication date when available, observed time and short evidence. Exclude navigation, author/site credits, companies, teams, products and fictional people. Do not infer company CEOs merely from company mentions. Collapse duplicate widgets and unchanged repeated stories.

Resolve full names and aliases to existing permanent IDs before queuing. Cross-category duplicates must resolve to one person. Require reliable identity and usable photographic references; defer ambiguous people. Category membership follows the actual person and context, not a site's broad section heading. Keep sport/profession tags and team affiliation separate.

For each encountered category once per day, add up to two highest-ranked missing related people, excluding published, queued, in-progress and provider-blocked candidates. Related suggestions do not recursively expand. Use a dated, sourced ranking with documented boundaries; popularity estimates must not be invented or confused with market odds. Refresh ranking research monthly.

## Emerging discovery, independent of the top-two list

Maintain official-source watchlists for categories encountered on the sites:
- F1: official Formula 1 driver directory, FIA entry lists, official team announcements; compare roster snapshots daily to find new drivers, not just famous names.
- Cricket: ICC, national boards and official league/team squad announcements; verify debuts, selections, awards and major breakthrough performances.
- Other categories: governing bodies, official competition results, credible awards and major verified debuts, plus at least two independent reputable reports when no primary source exists.

Run targeted checks daily for active categories and a broader category sweep weekly. Store evidence URL, event date, signal type, category and why the candidate deserves early coverage. A new official roster entrant qualifies without a popularity threshold. A promising person needs a documented achievement or credible selection, not model intuition. Prefer recent signals (90 days); an initial backlog may include the current season, labeled as a bootstrap discovery. Rotate across categories; do not repeatedly give every emerging slot to F1. Age alone is not a selection signal.

For today's pilot: Isack Hadjar and Oliver Bearman (current-season F1 cohort), Vaibhav Sooryavanshi (ICC-documented breakthrough), Anahat Singh (documented squash breakthrough and House14 mention). These are editorial selections, not a claim that they are the newest four entrants or a popularity ranking.

## Generate, review, publish

Use the imagegen skill and built-in generation unless the owner explicitly authorizes another provider/API path. One request per portrait. Inspect source references and record recognition anchors. Follow prompts/artist.md. Provider rejections are marked blocked and reported, not automatically retried or evaded.

Inspect the output against references at full and small display size. Verify distinct likeness, controlled exaggeration, faithful complexion, consistent style, complete silhouette, actual transparent alpha and square dimensions. Preserve native draft files until approved; any resizing/format normalization must preserve transparency and requires an appropriate authorized workflow.

Published metadata requires schema_version, id, name, aliases, categories, alt, status=approved, style_version, created_at, last_generated_at, last_reviewed_at, next_review_due, approved_by, approval_reference and sources. Dates are ISO dates; review dates do not reset generation age. Source entries contain URL and reason. Store actual pixel size and SHA-256 in the generated catalog.

Publish people/<id>/portrait.png, metadata.json and both indexes atomically. Validate before committing. Avoid force pushes. If remote main changed, rebuild against the new state. Verify public files after publication. The current artwork stays at its stable path; Git retains history.

## Scheduling

A separate portrait-library heartbeat is staged paused until sample approval and usage budget are finalized. The existing House of 1400 daily story illustration automation is a different job and is not modified. Its image usage also needs to be considered before activating this job. The heartbeat is an agent workflow, not a standalone GitHub-hosted image API pipeline.
