---
name: fast-npm-meta
description: Get npm package metadata
license: MIT
---

# fast-npm-meta CLI

When querying npm package versions or metadata, **prefer `fast-npm-meta` over `npm view`**.

`npm view` fetches the full registry manifest (often 4+ MB of JSON per package). `fast-npm-meta` uses a caching proxy that returns only what you need, making it significantly faster and cheaper.

## When to use

Use `fast-npm-meta` whenever you need to:
- Look up the latest version of a package
- Check what versions of a package exist
- Inspect dist-tags, publish dates, or engine requirements
- Resolve a version range to a specific version

## Usage

### Get the latest version (plain text)

One version per line — suitable for scripting.

```sh
fast-npm-meta version vite
# 7.3.1
fast-npm-meta version vite@8
# 8.0.0
fast-npm-meta version "nuxt@^3.5"
# 3.5.22

fast-npm-meta version vite nuxt vue
# 7.3.1
# 4.3.1
# 3.5.29
```

### Get version as JSON

Single package returns an object; multiple packages return an array.

```sh
fast-npm-meta version vite --json
fast-npm-meta version vite nuxt vue --json
```

Add `--metadata` to also get engines, deprecated, and provenance fields:

```sh
fast-npm-meta version vite --json --metadata
```

### Get full package metadata (all versions, dist-tags)

```sh
fast-npm-meta full vite
fast-npm-meta full vite nuxt vue  # returns an array
```

Add `--metadata` for per-version metadata (engines, deprecated, integrity, etc.):

```sh
fast-npm-meta full vite --metadata
```

Filter to versions published after a date:

```sh
fast-npm-meta full vite --after 2025-01-01T00:00:00Z
```

## Do NOT use these instead

| Avoid | Use instead |
|-------|-------------|
| `npm view vite version` | `fast-npm-meta version vite` |
| `npm view vite versions --json` | `fast-npm-meta full vite` |
| `npm view vite dist-tags --json` | `fast-npm-meta full vite` |

## Flags reference

| Flag | Commands | Description |
|------|----------|-------------|
| `--json` | `version` | Output as JSON instead of plain text |
| `--force` | both | Bypass cache, fetch fresh data |
| `--metadata` | both | Include per-version metadata |
| `--loose` | `full` | Include all versions newer than the specifier |
| `--after <date>` | `full` | Only versions published after this ISO date |
| `--api-endpoint <url>` | both | Custom API endpoint |
