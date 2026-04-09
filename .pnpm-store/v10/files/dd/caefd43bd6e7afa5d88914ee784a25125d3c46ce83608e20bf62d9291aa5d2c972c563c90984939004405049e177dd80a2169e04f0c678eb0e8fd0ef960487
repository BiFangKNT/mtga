## 6.12.0 (2026-02-15)

### Bug fixes

Fix an issue where a change that made both documents empty could leave an invalid chunk.

### New features

The diffing routine used can now be replaced with a custom implementation via `DiffConfig.override`.

## 6.11.2 (2025-11-07)

### Bug fixes

Fix a bug in `Chunk.updateA`/`updateB` that would cause it to drop an insertion or deletion chunk at the very end of the document.

## 6.11.1 (2025-10-23)

### Bug fixes

Export a function  that allows you to find the sibling of a given editor in a merge view.

## 6.11.0 (2025-10-02)

### New features

The `mergeControls` option to the unified merge view can now be a function, which will be used to render the buttons.

## 6.10.2 (2025-06-09)

### Bug fixes

Fix an issue where chunks in the unified diff weren't updated properly when a single transaction changed for the original and the edited document.

## 6.10.1 (2025-05-14)

### Bug fixes

Fix an issue in `presentableDiff` where it sometimes doesn't expand changes over words with multiple individual changes in them.

## 6.10.0 (2025-03-06)

### New features

The new `allowInlineDiffs` option to `unifiedMergeView` will display chunks with only limited inline changes inline in the code.

## 6.9.0 (2025-03-03)

### New features

The new diff option `timeout` can be used to make the algorithm bail out after a given amount of milliseconds.

Chunks now have a `precise` property that is false when the diff that the chunk is based on fell back to imprecise diffing (because of a scan depth limit or timeout).

## 6.8.0 (2024-12-30)

### Bug fixes

Limit the size of highlighted chunks in the unified view, to prevent freezing the interface highlighting huge amounts of code.

Fix a regression that caused deleted chunks in the unified view to be rendered with strike-through style by default.

### New features

Export the `uncollapseUnchanged` effect that is used to uncollapse sections of code.

## 6.7.5 (2024-12-17)

### Bug fixes

Fix a bug that hid the accept/reject buttons for insertions in the unified merge view.

The lines shown around collapsed unchanged lines are now css `:before`/`:after` elements, so that they can be customized more easily.

Render deleted lines in the unified merge view as block elements, for easier styling.

## 6.7.4 (2024-11-13)

### Bug fixes

In the unified diff view, fix an issue where empty deleted lines were rendered for chunks that deleted nothing.

Fix a bug that made the diff algorithm miss some obvious opportunities to align changes on line boundaries.

## 6.7.3 (2024-11-05)

### Bug fixes

Fix an issue where the last line of a deleted chunk, if there is no text on it, was collapsed by the browser and not visible.

## 6.7.2 (2024-10-10)

### Bug fixes

Fix a bug in `presentableDiff` that could cause it to produce corrupted diffs.

## 6.7.1 (2024-09-17)

### Bug fixes

Improve the way `presentableDiff` aligns changes to line boundaries when possible.

## 6.7.0 (2024-08-18)

### New features

`unifiedMergeView` now supports the `collapseUnchanged` option the way the split view does.

## 6.6.7 (2024-07-31)

### Bug fixes

Fix a bug in the way spacers were inserted at the top of the viewport.

## 6.6.6 (2024-07-30)

### Bug fixes

Improve vertical alignment of huge unchanged chunks in the side-by-side view.

## 6.6.5 (2024-07-18)

### Bug fixes

Fix an issue that would corrupt the text displayed for some deleted lines in the unified merge view.

## 6.6.4 (2024-07-18)

### Bug fixes

Fix syntax and change highlighting in deleted lines in the unified merge view.

## 6.6.3 (2024-06-07)

### Bug fixes

Fix `originalDocChangeEffect` to apply the changes to the appropriate document.

## 6.6.2 (2024-05-17)

### Bug fixes

Restore the default scan limit when diffing for chunks, which looks like it was accidentally dropped when it was made configurable in 6.3.0.

## 6.6.1 (2024-03-08)

### Bug fixes

Fix a bug that could cause the set of changed chunks to be updated incorrectly on some types of changes.

## 6.6.0 (2024-01-25)

### Bug fixes

Fix a bug where big deletions could corrupt the merge state.

### New features

The state effect used to change the original document in a unified merge view is now available to client code as `updateOriginalDoc`.

## 6.5.0 (2024-01-04)

### New features

The new `changeOriginalDocEffect` function can be used to update the reference document in a unified merge editor.

## 6.4.0 (2023-12-14)

### New features

The `getOriginalDoc` function extracts the original document from a unified merge editor.

## 6.3.1 (2023-12-03)

### Bug fixes

Add a `userEvent` annotation to transactions that accept a change in the unified merge view.

Fix CSS selectors in the merge view base theme to avoid affecting the style of non-merge view editors.

## 6.3.0 (2023-11-16)

### New features

Merge views (and `Chunk` building methods) now take an optional diff config object to allow precision to be configured.

## 6.2.0 (2023-10-06)

### New features

The package now exports `goToNextChunk` and `goToPreviousChunk` commands that allow by-changed-chunk document navigation.

## 6.1.3 (2023-09-28)

### Bug fixes

Create alignment spacers for the whole document, not just the viewport, to avoid scroll position popping and misalignment.

## 6.1.2 (2023-08-18)

### Bug fixes

Fall back to treating entire documents as changed when they are too large to compute a diff in a reasonable timeframe.

## 6.1.1 (2023-06-05)

### Bug fixes

Fix a crash when `unifiedMergeView` is added to an existing state by reconfiguration.

## 6.1.0 (2023-05-06)

### Bug fixes

Add `<ins>`/`<del>` tags around inserted and deleted lines to give screen readers a chance to communicate their role.

### New features

The new `unifiedMergeView` extension can be used to display a diff inside a single editor, by inserting deleted content as widgets in the document.

## 6.0.2 (2023-04-18)

### Bug fixes

Fix a bug that could cause `diff` to loop endlessly when the input contains astral characters in specific positions.

## 6.0.1 (2023-03-28)

### Bug fixes

Fix a bug that would cause diffing to loop infinitely with some inputs.

## 6.0.0 (2023-03-22)

### Bug fixes

Improve performance of the merge view when the inputs are almost entirely different.

### New features

`diff` and `presentableDiff` now take an optional `scanLimit` option that can be used to trade speed for accuracy on very different inputs.

## 0.1.6 (2023-02-28)

### Bug fixes

Fix a bug where changed chunks could be found in equal documents.

## 0.1.5 (2023-02-26)

### New features

`Chunk` now exposes static methods for building an updating sets of chunks directly.

## 0.1.4 (2023-02-17)

### Bug fixes

Fix a bug that caused an extra stray newline to be inserted when pressing the merge button for a change at the end of the document.

Avoid generating incorrect chunks for insertions or deletions at the end of the document.

## 0.1.3 (2022-12-09)

### New features

It is now possible to change the configuration of a merge view with its `reconfigure` method.

## 0.1.2 (2022-12-05)

### New features

The `Chunk` data structure, and the set of chunks kept by the merge view, are now part of the public interface.

The new `orientation` option makes it possible to show editor B first.

## 0.1.1 (2022-11-14)

### Bug fixes

Color changed chunks in editor A red by default.

## 0.1.0 (2022-11-10)

### Breaking changes

First numbered release.
