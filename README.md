# Personality Portraits

A growing editorial caricature PNG library, designed for straightforward use by any website.

**Status:** Personality Portraits v1.0 plugin created; general design language settled. Individual portrait publication remains gated pending review. Candidate names are not available assets.

## Find an image

Fetch [catalog.json](catalog.json). It contains only approved, published portraits. Look up a stable ID in `people`, or a normalized name in `aliases`. Use the returned `image` path relative to the catalog URL.

```js
const base = "https://raw.githubusercontent.com/thefirstparth/personality-portraits/main/";
const catalog = await fetch(base + "catalog.json").then(r => {
  if (!r.ok) throw new Error("Portrait catalog unavailable");
  return r.json();
});
const normalize = name => name.normalize("NFKD").replace(/\p{M}/gu, "")
  .toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
const id = catalog.aliases[normalize("Andrea Kimi Antonelli")];
const person = id ? catalog.people[id] : undefined;
if (person) {
  const img = document.createElement("img");
  img.src = new URL(person.image, base).href;
  img.alt = person.alt;
  img.width = 128;
  img.height = 128;
  document.body.append(img);
} // Otherwise use your website's normal fallback.
```

For reproducible builds, replace `main` in the base URL with a verified commit SHA. The catalog and images must use the same revision. Refreshes retain the same image path; clients should periodically revalidate the catalog and cache, or pin a new commit. Public URLs need no token. No server or framework is required.

## Stable layout

```text
catalog.json                         # published portraits only
categories.json                      # category -> published person IDs
people/<permanent-person-id>/
  portrait.png                       # current approved transparent square PNG
  metadata.json                      # identity, aliases, provenance and dates
config/production.json               # daily quotas and approval gate
queue/2026-09-28.json                 # candidates; never an image availability index
prompts/artist.md                    # versioned draft artist direction
docs/production.md                   # discovery, review and refresh rules
scripts/build_catalog.py             # validate published files and rebuild indexes
review/                             # LOCAL ONLY; ignored by Git
```

IDs are lowercase ASCII kebab-case and never change with a team, category, hairstyle or display name. Resolve name collisions with a meaningful permanent suffix before first publication. One person may have many category tags; never duplicate their portrait into category folders. Explicit aliases handle transliterations. Ambiguous aliases must be omitted or disambiguated, never silently assigned to the wrong person.

## Publishing

Only publish an approved image together with its metadata and rebuilt indexes in one commit. Run `python3 scripts/build_catalog.py` then `python3 scripts/build_catalog.py --check`. The validator requires a square RGBA PNG and verified human review fields. Actual transparent background, likeness, small-size legibility, framing and style are inspected visually before approval.

Production ceiling: six distinct portraits approved or published per IST day, normally four direct discoveries and two related candidates. Maximum twelve image-provider requests per day, including edits, failures and retries; two per person. Unused slots may use qualified backlog. Refreshes are manual in v1. The plugin is a manual host-assisted workflow; scheduling is separate. See [the plugin skill](plugins/personality-portraits/skills/grow-portraits/SKILL.md).

Reference photographs and unapproved images are never committed. The public catalog stays empty until style approval. Licensing for artwork remains to be selected before distributing the first approved release; public visibility alone is not a reuse license.
