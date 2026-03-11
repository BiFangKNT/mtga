---
name: ast-grep
description: Write and debug ast-grep rules for structural code search and rewrite. Use when tasks require AST-aware matching (not plain text), such as finding specific syntax shapes, relational patterns (inside/has), composite logic (all/any/not), or precise code refactors across a codebase.
---

# ast-grep Code Search

## Overview

Translate user intent into `sg` patterns/rules, validate quickly, then run against target scope.

## General Workflow

### Step 1: Understand the Query

Pin down:
- target syntax shape
- language
- file scope
- include/exclude constraints

### Step 2: Start with the Smallest Pattern

Use `sg run --pattern` first.

```bash
sg run --pattern 'console.log($ARG)' --lang javascript src
```

### Step 3: Escalate to YAML Rule for Structure Logic

For relational/composite logic (`inside` / `has` / `precedes` / `follows` / `all` / `any` / `not` / `matches`), use `sg scan --rule`.

```yaml
# rule.yml
id: async-with-await
language: javascript
rule:
  kind: function_declaration
  has:
    pattern: await $EXPR
    stopBy: end
```

```bash
sg scan --rule rule.yml src
```

### Step 4: Validate and Search

Test on a tiny sample first, then search the project.

```bash
echo "async function f(){ await g() }" | sg scan --rule rule.yml --stdin
sg scan --rule rule.yml src --json=compact
```

## CLI Quick Reference

### Inspect Code Structure (--debug-query)

Use when kind/pattern mismatch is unclear.

```bash
sg run --pattern 'class $NAME { $$$BODY }' \
  --lang javascript \
  --debug-query=pattern
```

### Test Rules (scan with --stdin)

```bash
echo "const x = await fetch();" | sg scan --inline-rules "id: test
language: javascript
rule:
  pattern: await \$EXPR" --stdin --json=compact
```

### Search with Patterns (run)

```bash
sg run --pattern 'function $NAME($$$)' --lang javascript src --json=compact
```

### Search with Rules (scan)

```bash
sg scan --rule rule.yml src
sg scan --inline-rules "id: find-async
language: javascript
rule:
  kind: function_declaration
  has:
    pattern: await \$EXPR
    stopBy: end" src
```

## Tips for Writing Effective Rules

### Default to stopBy: end for Deep Searches

For relational rules (`inside`, `has`), default to:

```yaml
has:
  pattern: await $EXPR
  stopBy: end
```

This ensures the search traverses the entire subtree rather than stopping at the first non-matching node.

### Start Simple, Then Add Complexity

1. `pattern`
2. `kind`
3. add `inside`/`has`
4. add `all`/`any`/`not`

### Metavariable Rules

1. Use exact metavariable forms only: `$A`, `$$OP`, `$$$ARGS`.
2. Keep metavariable text as the only content in its AST node.
3. If a rule depends on previously captured metavariables, combine sub-rules in `all` to guarantee match order.

### No-Match Triage

1. Run with `--json=compact`.
2. If output is `[]`, treat as no match and refine pattern/scope.
3. If stderr has parser/arg errors, fix language, pattern, or flags first.

## Resources

### references/

- `rule_reference.md`: Full rule syntax (atomic, relational, composite, metavariables)
- `windows.md`: PowerShell quoting/escaping tips and Vue SFC script-block workflow

Load only the reference needed for the current task.
