# Website and automatic publishing

The public directory is available at **https://m9rco.github.io/awesome-python-dev/**,
with a [Chinese introduction](https://m9rco.github.io/awesome-python-dev/zh/).

## Content sources

`scripts/build_site.py` is the stable command entry point. Its implementation in
`scripts/sitegen/` separates shared configuration, HTML rendering and Agent
discovery exports. It creates a static website from the repository's catalog and
package metadata. Tool names, descriptions, installation support, provenance,
profile membership and counts come from
`src/awesome_python_dev/data/catalog.json`; the CLI version comes from
`pyproject.toml`. Edit those sources to update the collection. Website presentation
and navigation live in `scripts/sitegen/renderer.py` and `site/assets/`.

Generated HTML, Markdown and JSON in `_site/` are ignored by Git. The site includes a home page,
getting-started guide, category pages, individual tool pages and profile pages.
Each tool page distinguishes an installable recipe from an upstream reference.
Catalog content is present in the HTML, so browsing and crawling do not depend on
JavaScript. Search and command copying add optional browser conveniences.

The website is a `main` source snapshot. Its package version is not proof that
every displayed tool has shipped in that runtime release. Discovery metadata
identifies the catalog snapshot; installed clients should check `apd list --json`
and `apd profiles --json` before using a new ID.

## Agent discovery and GEO

| Entry | Purpose |
| --- | --- |
| [`llms.txt`](https://m9rco.github.io/awesome-python-dev/llms.txt) | Compact project overview and links to Markdown details |
| [`agents/`](https://m9rco.github.io/awesome-python-dev/agents/) | How an agent can identify tools, verify availability and preview installation |
| [`catalog.json`](https://m9rco.github.io/awesome-python-dev/catalog.json) | Catalog records plus discovery metadata and source provenance |
| `index.md` beside a page | Plain-text counterpart for landing, getting-started, category, tool and profile pages |

HTML link metadata advertises the covering `llms.txt` (`rel="describedby"`) and
the page's Markdown counterpart (`rel="alternate" type="text/markdown"`). Links
include the configured base path, including on GitHub project sites. Tool pages
and machine exports distinguish reference-only resources from installable
recipes; reference-only entries must not advertise an installation command.

These files help agents retrieve focused information without parsing the full
visual layout. `llms.txt` is a [community proposal](https://llmstxt.org/), not a
ranking requirement. Google states that [its AI search features use normal SEO
requirements](https://developers.google.com/search/docs/appearance/ai-features)
and do not require special AI files. Crawlability, useful visible text, accurate
structured metadata and source evidence remain the foundation; ranking or
citations are not guaranteed.

`scripts/check_site.py` and the website tests validate discovery files and link
targets along with HTML metadata and the sitemap. Content is generated from the
same catalog rather than maintained as a second tool database.

## Automatic updates

The [GitHub Pages workflow](../.github/workflows/pages.yml) runs on every push to
`main`, on pull requests targeting `main`, and on manual dispatch:

1. Install the locked development dependencies and test website generation.
2. Build the entire site from the current repository contents.
3. Validate the generated pages, SEO metadata and internal links.
4. On `main`, upload the validated Pages artifact and deploy it to the
   `github-pages` environment.

Pull requests only build and validate; they cannot publish the production site.
Only the deployment job receives `pages: write` and `id-token: write`. Action
versions are pinned to full commit hashes. A running production deployment is
allowed to finish before another deployment starts.

This updates the website from the reviewed catalog; it does not automatically
change upstream pins or refresh GitHub star snapshots. Those remain deliberate
catalog maintenance changes.

GitHub Pages must use **Settings → Pages → Build and deployment → GitHub Actions**.
No deployment token or additional secret is needed. The production build takes
its base URL from `actions/configure-pages`, so project subpaths and a configured
custom domain are reflected in links and canonical URLs. Fork maintainers should
also update the fallback URL used for pull-request builds in `pages.yml`.

## Local preview

From the repository root:

```sh
uv sync --locked
uv run python scripts/build_site.py --output _site --base-url http://localhost:8000
uv run python scripts/check_site.py --site _site --base-url http://localhost:8000
uv run python -m http.server 8000 --directory _site
```

Open `http://localhost:8000/`. A production-equivalent build uses:

```sh
uv run python scripts/build_site.py --output _site --base-url https://m9rco.github.io/awesome-python-dev
uv run python scripts/check_site.py --site _site --base-url https://m9rco.github.io/awesome-python-dev
```

Do not publish the localhost build: its canonical URLs and sitemap intentionally
point at the preview origin. CI always rebuilds with the configured Pages URL.

## Search visibility

The site provides descriptive page titles and summaries, canonical URLs,
structured data, a sitemap, and social sharing metadata. English and Chinese
landing pages identify their language alternatives. Links between the directory,
profiles and tool detail pages make the collection discoverable without a search
form.

The sitemap is published at
[`sitemap.xml`](https://m9rco.github.io/awesome-python-dev/sitemap.xml).
If you have verified ownership in Google Search Console, submit this URL there.
Search engines decide when to crawl, index and rank pages; publishing a sitemap
does not guarantee inclusion.

GitHub project sites live below a path such as `/awesome-python-dev/`. A generated
`robots.txt` at that path cannot control the whole host: crawlers look for
`https://m9rco.github.io/robots.txt`. The project does not edit the owner's root
site. If a custom domain is configured at its root, the generated robots file can
be served from the correct location. The sitemap remains independently usable on
the project URL.

References: [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages),
[Google's sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap),
[language alternate guidance](https://developers.google.com/search/docs/specialty/international/localized-versions),
[structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies),
and [robots.txt location requirements](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt).
