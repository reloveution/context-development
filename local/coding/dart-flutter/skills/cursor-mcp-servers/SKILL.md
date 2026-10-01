---
name: cursor-mcp-servers
description: MCP server usage for Dart MCP, Hugging Face. Tool priorities, commands, workflows.
---

# MCP Servers

## Tool Priority

| Task | Tool | Fallback |
|---|---|---|
| Dart/Flutter packages | `pub_dev_search` | fetch the pub.dev page |
| Code analysis/format/tests | Dart MCP | — |
| Web content | search the web, fetch the page | — |
| ML models/datasets/papers | Hugging Face MCP | search the web |

## Dart MCP

**Setup:** `add_roots` required before workspace commands. Format: `[{uri: "file:///path", name: "optional"}]`.

**Commands:**
- **Project:** create_project, add_roots, remove_roots, pub (add/get/remove/upgrade), pub_dev_search
- **Analysis:** analyze_files, dart_fix, dart_format
- **Symbols:** resolve_workspace_symbol, hover, signature_help
- **Tests:** run_tests (testRunnerArgs: name, tags, platform, timeout, fail-fast, coverage)
- **DTD (running app):** connect_dart_tooling_daemon (needs URI from user), hot_reload, get_runtime_errors, get_widget_tree, get_selected_widget

**Errors:** Verify SDK; DTD needs fresh URI after reconnect; dart_fix before manual fixes; check network for pub.

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
Web docs:         search the web for URLs → fetch the page
ML models:        model_search with filters → hub_repo_details
DTD:              connect_dart_tooling_daemon(uri) → get_widget_tree / hot_reload
```
