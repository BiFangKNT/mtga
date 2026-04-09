import * as _codemirror_state from '@codemirror/state';
import { Text, ChangeDesc, EditorState, StateCommand, EditorStateConfig, StateField, ChangeSet, StateEffect } from '@codemirror/state';
import { EditorView, DecorationSet } from '@codemirror/view';

/**
A changed range.
*/
declare class Change {
    /**
    The start of the change in document A.
    */
    readonly fromA: number;
    /**
    The end of the change in document A. This is equal to `fromA`
    in case of insertions.
    */
    readonly toA: number;
    /**
    The start of the change in document B.
    */
    readonly fromB: number;
    /**
    The end of the change in document B. This is equal to `fromB`
    for deletions.
    */
    readonly toB: number;
    constructor(
    /**
    The start of the change in document A.
    */
    fromA: number, 
    /**
    The end of the change in document A. This is equal to `fromA`
    in case of insertions.
    */
    toA: number, 
    /**
    The start of the change in document B.
    */
    fromB: number, 
    /**
    The end of the change in document B. This is equal to `fromB`
    for deletions.
    */
    toB: number);
}
/**
Options passed to diffing functions.
*/
interface DiffConfig {
    /**
    When given, this limits the depth of full (expensive) diff
    computations, causing them to give up and fall back to a faster
    but less precise approach when there is more than this many
    changed characters in a scanned range. This should help avoid
    quadratic running time on large, very different inputs.
    */
    scanLimit?: number;
    /**
    When set, this makes the algorithm periodically check how long
    it has been running, and if it has taken more than the given
    number of milliseconds, it aborts detailed diffing in falls back
    to the imprecise algorithm.
    */
    timeout?: number;
    /**
    Provide your own diff algorithm, replacing this package's `diff`
    function.
    */
    override?: (a: string, b: string) => readonly Change[];
}
/**
Compute the difference between two strings.
*/
declare function diff(a: string, b: string, config?: DiffConfig): readonly Change[];
/**
Compute the difference between the given strings, and clean up the
resulting diff for presentation to users by dropping short
unchanged ranges, and aligning changes to word boundaries when
appropriate.
*/
declare function presentableDiff(a: string, b: string, config?: DiffConfig): readonly Change[];

/**
A chunk describes a range of lines which have changed content in
them. Either side (a/b) may either be empty (when its `to` is
equal to its `from`), or points at a range starting at the start
of the first changed line, to 1 past the end of the last changed
line. Note that `to` positions may point past the end of the
document. Use `endA`/`endB` if you need an end position that is
certain to be a valid document position.
*/
declare class Chunk {
    /**
    The individual changes inside this chunk. These are stored
    relative to the start of the chunk, so you have to add
    `chunk.fromA`/`fromB` to get document positions.
    */
    readonly changes: readonly Change[];
    /**
    The start of the chunk in document A.
    */
    readonly fromA: number;
    /**
    The end of the chunk in document A. This is equal to `fromA`
    when the chunk covers no lines in document A, or is one unit
    past the end of the last line in the chunk if it does.
    */
    readonly toA: number;
    /**
    The start of the chunk in document B.
    */
    readonly fromB: number;
    /**
    The end of the chunk in document A.
    */
    readonly toB: number;
    /**
    This is set to false when the diff used to compute this chunk
    fell back to fast, imprecise diffing.
    */
    readonly precise: boolean;
    constructor(
    /**
    The individual changes inside this chunk. These are stored
    relative to the start of the chunk, so you have to add
    `chunk.fromA`/`fromB` to get document positions.
    */
    changes: readonly Change[], 
    /**
    The start of the chunk in document A.
    */
    fromA: number, 
    /**
    The end of the chunk in document A. This is equal to `fromA`
    when the chunk covers no lines in document A, or is one unit
    past the end of the last line in the chunk if it does.
    */
    toA: number, 
    /**
    The start of the chunk in document B.
    */
    fromB: number, 
    /**
    The end of the chunk in document A.
    */
    toB: number, 
    /**
    This is set to false when the diff used to compute this chunk
    fell back to fast, imprecise diffing.
    */
    precise?: boolean);
    /**
    Returns `fromA` if the chunk is empty in A, or the end of the
    last line in the chunk otherwise.
    */
    get endA(): number;
    /**
    Returns `fromB` if the chunk is empty in B, or the end of the
    last line in the chunk otherwise.
    */
    get endB(): number;
    /**
    Build a set of changed chunks for the given documents.
    */
    static build(a: Text, b: Text, conf?: DiffConfig): readonly Chunk[];
    /**
    Update a set of chunks for changes in document A. `a` should
    hold the updated document A.
    */
    static updateA(chunks: readonly Chunk[], a: Text, b: Text, changes: ChangeDesc, conf?: DiffConfig): readonly Chunk[];
    /**
    Update a set of chunks for changes in document B.
    */
    static updateB(chunks: readonly Chunk[], a: Text, b: Text, changes: ChangeDesc, conf?: DiffConfig): readonly Chunk[];
}

/**
Get the changed chunks for the merge view that this editor is part
of, plus the side it is on if it is part of a `MergeView`. Returns
null if the editor doesn't have a merge extension active or the
merge view hasn't finished initializing yet.
*/
declare function getChunks(state: EditorState): {
    chunks: readonly Chunk[];
    side: "a" | "b" | null;
} | null;
/**
Move the selection to the next changed chunk.
*/
declare const goToNextChunk: StateCommand;
/**
Move the selection to the previous changed chunk.
*/
declare const goToPreviousChunk: StateCommand;

/**
Configuration options to `MergeView` that can be provided both
initially and to [`reconfigure`](https://codemirror.net/6/docs/ref/#merge.MergeView.reconfigure).
*/
interface MergeConfig {
    /**
    Controls whether editor A or editor B is shown first. Defaults
    to `"a-b"`.
    */
    orientation?: "a-b" | "b-a";
    /**
    Controls whether revert controls are shown between changed
    chunks.
    */
    revertControls?: "a-to-b" | "b-to-a";
    /**
    When given, this function is called to render the button to
    revert a chunk.
    */
    renderRevertControl?: () => HTMLElement;
    /**
    By default, the merge view will mark inserted and deleted text
    in changed chunks. Set this to false to turn that off.
    */
    highlightChanges?: boolean;
    /**
    Controls whether a gutter marker is shown next to changed lines.
    */
    gutter?: boolean;
    /**
    When given, long stretches of unchanged text are collapsed.
    `margin` gives the number of lines to leave visible after/before
    a change (default is 3), and `minSize` gives the minimum amount
    of collapsible lines that need to be present (defaults to 4).
    */
    collapseUnchanged?: {
        margin?: number;
        minSize?: number;
    };
    /**
    Pass options to the diff algorithm. By default, the merge view
    sets [`scanLimit`](https://codemirror.net/6/docs/ref/#merge.DiffConfig.scanLimit) to 500.
    */
    diffConfig?: DiffConfig;
}
/**
Configuration options given to the [`MergeView`](https://codemirror.net/6/docs/ref/#merge.MergeView)
constructor.
*/
interface DirectMergeConfig extends MergeConfig {
    /**
    Configuration for the first editor (the left one in a
    left-to-right context).
    */
    a: EditorStateConfig;
    /**
    Configuration for the second editor.
    */
    b: EditorStateConfig;
    /**
    Parent element to append the view to.
    */
    parent?: Element | DocumentFragment;
    /**
    An optional root. Only necessary if the view is mounted in a
    shadow root or a document other than the global `document`
    object.
    */
    root?: Document | ShadowRoot;
}
/**
A merge view manages two editors side-by-side, highlighting the
difference between them and vertically aligning unchanged lines.
If you want one of the editors to be read-only, you have to
configure that in its extensions.

By default, views are not scrollable. Style them (`.cm-mergeView`)
with a height and `overflow: auto` to make them scrollable.
*/
declare class MergeView {
    /**
    The first editor.
    */
    a: EditorView;
    /**
    The second editor.
    */
    b: EditorView;
    /**
    The outer DOM element holding the view.
    */
    dom: HTMLElement;
    private editorDOM;
    private revertDOM;
    private revertToA;
    private revertToLeft;
    private renderRevert;
    private diffConf;
    /**
    The current set of changed chunks.
    */
    chunks: readonly Chunk[];
    private measuring;
    /**
    Create a new merge view.
    */
    constructor(config: DirectMergeConfig);
    private dispatch;
    /**
    Reconfigure an existing merge view.
    */
    reconfigure(config: MergeConfig): void;
    private setupRevertControls;
    private scheduleMeasure;
    private measure;
    private updateRevertButtons;
    private renderRevertButton;
    private revertClicked;
    /**
    Destroy this merge view.
    */
    destroy(): void;
}

interface UnifiedMergeConfig {
    /**
    The other document to compare the editor content with.
    */
    original: Text | string;
    /**
    By default, the merge view will mark inserted and deleted text
    in changed chunks. Set this to false to turn that off.
    */
    highlightChanges?: boolean;
    /**
    Controls whether a gutter marker is shown next to changed lines.
    */
    gutter?: boolean;
    /**
    By default, deleted chunks are highlighted using the main
    editor's language. Since these are just fragments, not full
    documents, this doesn't always work well. Set this option to
    false to disable syntax highlighting for deleted lines.
    */
    syntaxHighlightDeletions?: boolean;
    /**
    When enabled (off by default), chunks that look like they
    contain only inline changes will have the changes displayed
    inline, rather than as separate deleted/inserted lines.
    */
    allowInlineDiffs?: boolean;
    /**
    Deleted blocks larger than this size do not get
    syntax-highlighted. Defaults to 3000.
    */
    syntaxHighlightDeletionsMaxLength?: number;
    /**
    Controls whether accept/reject buttons are displayed for each
    changed chunk. Defaults to true. When set to a function, that
    function is used to render the buttons.
    */
    mergeControls?: boolean | ((type: "reject" | "accept", action: (e: MouseEvent) => void) => HTMLElement);
    /**
    Pass options to the diff algorithm. By default, the merge view
    sets [`scanLimit`](https://codemirror.net/6/docs/ref/#merge.DiffConfig.scanLimit) to 500.
    */
    diffConfig?: DiffConfig;
    /**
    When given, long stretches of unchanged text are collapsed.
    `margin` gives the number of lines to leave visible after/before
    a change (default is 3), and `minSize` gives the minimum amount
    of collapsible lines that need to be present (defaults to 4).
    */
    collapseUnchanged?: {
        margin?: number;
        minSize?: number;
    };
}
/**
Create an extension that causes the editor to display changes
between its content and the given original document. Changed
chunks will be highlighted, with uneditable widgets displaying the
original text displayed above the new text.
*/
declare function unifiedMergeView(config: UnifiedMergeConfig): (_codemirror_state.Extension | StateField<DecorationSet>)[];
/**
The state effect used to signal changes in the original doc in a
unified merge view.
*/
declare const updateOriginalDoc: _codemirror_state.StateEffectType<{
    doc: Text;
    changes: ChangeSet;
}>;
/**
Create an effect that, when added to a transaction on a unified
merge view, will update the original document that's being compared against.
*/
declare function originalDocChangeEffect(state: EditorState, changes: ChangeSet): StateEffect<{
    doc: Text;
    changes: ChangeSet;
}>;
/**
Get the original document from a unified merge editor's state.
*/
declare function getOriginalDoc(state: EditorState): Text;
/**
In a [unified](https://codemirror.net/6/docs/ref/#merge.unifiedMergeView) merge view, accept the
chunk under the given position or the cursor. This chunk will no
longer be highlighted unless it is edited again.
*/
declare function acceptChunk(view: EditorView, pos?: number): boolean;
/**
In a [unified](https://codemirror.net/6/docs/ref/#merge.unifiedMergeView) merge view, reject the
chunk under the given position or the cursor. Reverts that range
to the content it has in the original document.
*/
declare function rejectChunk(view: EditorView, pos?: number): boolean;

/**
A state effect that expands the section of collapsed unchanged
code starting at the given position.
*/
declare const uncollapseUnchanged: _codemirror_state.StateEffectType<number>;
/**
Query whether the given view is displayed next to another editor
in a merge view. Returns `null` if it isn't, and a pair of editors
(one of which will be the view itself) otherwise.
*/
declare function mergeViewSiblings(view: EditorView): {
    a: EditorView;
    b: EditorView;
} | null;

export { Change, Chunk, type DiffConfig, type DirectMergeConfig, type MergeConfig, MergeView, acceptChunk, diff, getChunks, getOriginalDoc, goToNextChunk, goToPreviousChunk, mergeViewSiblings, originalDocChangeEffect, presentableDiff, rejectChunk, uncollapseUnchanged, unifiedMergeView, updateOriginalDoc };
