# Windows Notes (PowerShell + Vue SFC)

Load this file only when:
- `sg` commands in PowerShell hit quoting/escaping issues
- Structural search is needed inside `.vue` single-file components

## PowerShell Quoting and Escaping

Prefer single-quoted patterns to avoid shell expansion of `$VAR`:

```powershell
sg run --pattern 'const $A = $B' --lang typescript src
```

In `--inline-rules`, escape metavariables in YAML using `\$`:

```powershell
sg scan --inline-rules "id: t
language: javascript
rule:
  pattern: await \$EXPR" src
```

When inline YAML becomes long, prefer `--rule rule.yml` to avoid deep escaping.

## Vue SFC (`.vue`) Script-Block Search

For JS/TS structural search in Vue SFC files, extract `<script>` first, then use `--stdin`:

```powershell
$src = Get-Content -Path 'app/components/dialogs/SystemPromptEditorDialog.vue' -Raw
if ($src -match '<script(?:\s+setup)?[^>]*>([\s\S]*?)</script>') {
  $matches[1] | sg run --pattern 'const $A = $B' --lang typescript --stdin
}
```

If the script tag is `lang="js"`, switch `--lang typescript` to `--lang javascript`.
