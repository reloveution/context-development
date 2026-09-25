---
name: cursor-mcp-servers
description: MCP server usage for Dart MCP, Firecrawl, Hugging Face. Tool priorities, commands, workflows.
---

# MCP Servers

## Tool Priority

| Task | Tool | Fallback |
|---|---|---|
| Dart/Flutter packages | `pub_dev_search` | Firecrawl scrape pub.dev |
| Code analysis/format/tests | Dart MCP | — |
| Web content | Firecrawl `scrape`/`map` | `web_search` |
| ML models/datasets/papers | Hugging Face MCP | Firecrawl |

**firecrawl_search: UNAVAILABLE (503)** — use `web_search` or `map` + `scrape`.

## Dart MCP

**Setup:** `add_roots` required before workspace commands. Format: `[{uri: "file:///path", name: "optional"}]`.

**Commands:**
- **Project:** create_project, add_roots, remove_roots, pub (add/get/remove/upgrade), pub_dev_search
- **Analysis:** analyze_files, dart_fix, dart_format
- **Symbols:** resolve_workspace_symbol, hover, signature_help
- **Tests:** run_tests (testRunnerArgs: name, tags, platform, timeout, fail-fast, coverage)
- **DTD (running app):** connect_dart_tooling_daemon (needs URI from user), hot_reload, get_runtime_errors, get_widget_tree, get_selected_widget

**Errors:** Verify SDK; DTD needs fresh URI after reconnect; dart_fix before manual fixes; check network for pub.

## Firecrawl

- `scrape` — single page (formats: markdown/html; maxAge for caching)
- `batch_scrape` → `check_batch_status` — multiple URLs
- `map` — discover URLs on site, then scrape
- `crawl` → `check_crawl_status` — full site (caution: token overflow; limit depth/pages)
- `extract` — structured data with schema/prompt

**Config:** FIRECRAWL_API_KEY required. maxAge for caching (172800000 = 2 days).

**Errors:** `onlyMainContent: true` for cleaner scrape; JS-heavy sites may fail.

## Hugging Face

- `model_search` (query, sort, limit, author, library, task) — max 100/query
- `dataset_search` (query, sort, tags)
- `paper_search` (query, results_limit, concise_only) — concise_only for broad search
- `space_search`, `hub_repo_details` (repo_ids `author/name`, repo_type) — max 10/call
- `hf_doc_search` → `hf_doc_fetch` (offset for large docs)
- `gr1_flux1_schnell_infer` (prompt, width, height, num_inference_steps) — defaults: 4 steps, 1024x1024

**Errors:** `hf_whoami` for auth; specify repo_type if auto-detect fails; filter early.

## Key Workflows

```
Package info:     pub_dev_search(query: "package_name")
Add dependency:   pub(command: "add", packageName: "x", roots: [{root: "file:///path"}])
Analyze project:  add_roots → analyze_files → dart_fix → dart_format
Web docs:         web_search for URLs → scrape(url, formats: ["markdown"], onlyMainContent: true)
Batch scrape:     batch_scrape(urls) → check_batch_status(id)
ML models:        model_search with filters → hub_repo_details
DTD:              connect_dart_tooling_daemon(uri) → get_widget_tree / hot_reload
```
