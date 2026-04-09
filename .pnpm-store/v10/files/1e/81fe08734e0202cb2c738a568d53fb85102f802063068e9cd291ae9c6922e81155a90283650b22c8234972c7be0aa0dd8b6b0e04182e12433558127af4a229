'use strict';

var view = require('@codemirror/view');
var state = require('@codemirror/state');
var styleMod = require('style-mod');
var language = require('@codemirror/language');
var highlight = require('@lezer/highlight');

// This algorithm was heavily inspired by Neil Fraser's
// diff-match-patch library. See https://github.com/google/diff-match-patch/
/**
A changed range.
*/
class Change {
    constructor(
    /**
    The start of the change in document A.
    */
    fromA, 
    /**
    The end of the change in document A. This is equal to `fromA`
    in case of insertions.
    */
    toA, 
    /**
    The start of the change in document B.
    */
    fromB, 
    /**
    The end of the change in document B. This is equal to `fromB`
    for deletions.
    */
    toB) {
        this.fromA = fromA;
        this.toA = toA;
        this.fromB = fromB;
        this.toB = toB;
    }
    /**
    @internal
    */
    offset(offA, offB = offA) {
        return new Change(this.fromA + offA, this.toA + offA, this.fromB + offB, this.toB + offB);
    }
}
function findDiff(a, fromA, toA, b, fromB, toB) {
    if (a == b)
        return [];
    // Remove identical prefix and suffix
    let prefix = commonPrefix(a, fromA, toA, b, fromB, toB);
    let suffix = commonSuffix(a, fromA + prefix, toA, b, fromB + prefix, toB);
    fromA += prefix;
    toA -= suffix;
    fromB += prefix;
    toB -= suffix;
    let lenA = toA - fromA, lenB = toB - fromB;
    // Nothing left in one of them
    if (!lenA || !lenB)
        return [new Change(fromA, toA, fromB, toB)];
    // Try to find one string in the other to cover cases with just 2
    // deletions/insertions.
    if (lenA > lenB) {
        let found = a.slice(fromA, toA).indexOf(b.slice(fromB, toB));
        if (found > -1)
            return [
                new Change(fromA, fromA + found, fromB, fromB),
                new Change(fromA + found + lenB, toA, toB, toB)
            ];
    }
    else if (lenB > lenA) {
        let found = b.slice(fromB, toB).indexOf(a.slice(fromA, toA));
        if (found > -1)
            return [
                new Change(fromA, fromA, fromB, fromB + found),
                new Change(toA, toA, fromB + found + lenA, toB)
            ];
    }
    // Only one character left on one side, does not occur in other
    // string.
    if (lenA == 1 || lenB == 1)
        return [new Change(fromA, toA, fromB, toB)];
    // Try to split the problem in two by finding a substring of one of
    // the strings in the other.
    let half = halfMatch(a, fromA, toA, b, fromB, toB);
    if (half) {
        let [sharedA, sharedB, sharedLen] = half;
        return findDiff(a, fromA, sharedA, b, fromB, sharedB)
            .concat(findDiff(a, sharedA + sharedLen, toA, b, sharedB + sharedLen, toB));
    }
    // Fall back to more expensive general search for a shared
    // subsequence.
    return findSnake(a, fromA, toA, b, fromB, toB);
}
let scanLimit = 1e9;
let timeout = 0;
let crude = false;
// Implementation of Myers 1986 "An O(ND) Difference Algorithm and Its Variations"
function findSnake(a, fromA, toA, b, fromB, toB) {
    let lenA = toA - fromA, lenB = toB - fromB;
    if (scanLimit < 1e9 && Math.min(lenA, lenB) > scanLimit * 16 ||
        timeout > 0 && Date.now() > timeout) {
        if (Math.min(lenA, lenB) > scanLimit * 64)
            return [new Change(fromA, toA, fromB, toB)];
        return crudeMatch(a, fromA, toA, b, fromB, toB);
    }
    let off = Math.ceil((lenA + lenB) / 2);
    frontier1.reset(off);
    frontier2.reset(off);
    let match1 = (x, y) => a.charCodeAt(fromA + x) == b.charCodeAt(fromB + y);
    let match2 = (x, y) => a.charCodeAt(toA - x - 1) == b.charCodeAt(toB - y - 1);
    let test1 = (lenA - lenB) % 2 != 0 ? frontier2 : null, test2 = test1 ? null : frontier1;
    for (let depth = 0; depth < off; depth++) {
        if (depth > scanLimit || timeout > 0 && !(depth & 63) && Date.now() > timeout)
            return crudeMatch(a, fromA, toA, b, fromB, toB);
        let done = frontier1.advance(depth, lenA, lenB, off, test1, false, match1) ||
            frontier2.advance(depth, lenA, lenB, off, test2, true, match2);
        if (done)
            return bisect(a, fromA, toA, fromA + done[0], b, fromB, toB, fromB + done[1]);
    }
    // No commonality at all.
    return [new Change(fromA, toA, fromB, toB)];
}
class Frontier {
    constructor() {
        this.vec = [];
    }
    reset(off) {
        this.len = off << 1;
        for (let i = 0; i < this.len; i++)
            this.vec[i] = -1;
        this.vec[off + 1] = 0;
        this.start = this.end = 0;
    }
    advance(depth, lenX, lenY, vOff, other, fromBack, match) {
        for (let k = -depth + this.start; k <= depth - this.end; k += 2) {
            let off = vOff + k;
            let x = k == -depth || (k != depth && this.vec[off - 1] < this.vec[off + 1])
                ? this.vec[off + 1] : this.vec[off - 1] + 1;
            let y = x - k;
            while (x < lenX && y < lenY && match(x, y)) {
                x++;
                y++;
            }
            this.vec[off] = x;
            if (x > lenX) {
                this.end += 2;
            }
            else if (y > lenY) {
                this.start += 2;
            }
            else if (other) {
                let offOther = vOff + (lenX - lenY) - k;
                if (offOther >= 0 && offOther < this.len && other.vec[offOther] != -1) {
                    if (!fromBack) {
                        let xOther = lenX - other.vec[offOther];
                        if (x >= xOther)
                            return [x, y];
                    }
                    else {
                        let xOther = other.vec[offOther];
                        if (xOther >= lenX - x)
                            return [xOther, vOff + xOther - offOther];
                    }
                }
            }
        }
        return null;
    }
}
// Reused across calls to avoid growing the vectors again and again
const frontier1 = new Frontier, frontier2 = new Frontier;
// Given a position in both strings, recursively call `findDiff` with
// the sub-problems before and after that position. Make sure cut
// points lie on character boundaries.
function bisect(a, fromA, toA, splitA, b, fromB, toB, splitB) {
    let stop = false;
    if (!validIndex(a, splitA) && ++splitA == toA)
        stop = true;
    if (!validIndex(b, splitB) && ++splitB == toB)
        stop = true;
    if (stop)
        return [new Change(fromA, toA, fromB, toB)];
    return findDiff(a, fromA, splitA, b, fromB, splitB).concat(findDiff(a, splitA, toA, b, splitB, toB));
}
function chunkSize(lenA, lenB) {
    let size = 1, max = Math.min(lenA, lenB);
    while (size < max)
        size = size << 1;
    return size;
}
// Common prefix length of the given ranges. Because string comparison
// is so much faster than a JavaScript by-character loop, this
// compares whole chunks at a time.
function commonPrefix(a, fromA, toA, b, fromB, toB) {
    if (fromA == toA || fromA == toB || a.charCodeAt(fromA) != b.charCodeAt(fromB))
        return 0;
    let chunk = chunkSize(toA - fromA, toB - fromB);
    for (let pA = fromA, pB = fromB;;) {
        let endA = pA + chunk, endB = pB + chunk;
        if (endA > toA || endB > toB || a.slice(pA, endA) != b.slice(pB, endB)) {
            if (chunk == 1)
                return pA - fromA - (validIndex(a, pA) ? 0 : 1);
            chunk = chunk >> 1;
        }
        else if (endA == toA || endB == toB) {
            return endA - fromA;
        }
        else {
            pA = endA;
            pB = endB;
        }
    }
}
// Common suffix length
function commonSuffix(a, fromA, toA, b, fromB, toB) {
    if (fromA == toA || fromB == toB || a.charCodeAt(toA - 1) != b.charCodeAt(toB - 1))
        return 0;
    let chunk = chunkSize(toA - fromA, toB - fromB);
    for (let pA = toA, pB = toB;;) {
        let sA = pA - chunk, sB = pB - chunk;
        if (sA < fromA || sB < fromB || a.slice(sA, pA) != b.slice(sB, pB)) {
            if (chunk == 1)
                return toA - pA - (validIndex(a, pA) ? 0 : 1);
            chunk = chunk >> 1;
        }
        else if (sA == fromA || sB == fromB) {
            return toA - sA;
        }
        else {
            pA = sA;
            pB = sB;
        }
    }
}
// a assumed to be be longer than b
function findMatch(a, fromA, toA, b, fromB, toB, size, divideTo) {
    let rangeB = b.slice(fromB, toB);
    // Try some substrings of A of length `size` and see if they exist
    // in B.
    let best = null;
    for (;;) {
        if (best || size < divideTo)
            return best;
        for (let start = fromA + size;;) {
            if (!validIndex(a, start))
                start++;
            let end = start + size;
            if (!validIndex(a, end))
                end += end == start + 1 ? 1 : -1;
            if (end >= toA)
                break;
            let seed = a.slice(start, end);
            let found = -1;
            while ((found = rangeB.indexOf(seed, found + 1)) != -1) {
                let prefixAfter = commonPrefix(a, end, toA, b, fromB + found + seed.length, toB);
                let suffixBefore = commonSuffix(a, fromA, start, b, fromB, fromB + found);
                let length = seed.length + prefixAfter + suffixBefore;
                if (!best || best[2] < length)
                    best = [start - suffixBefore, fromB + found - suffixBefore, length];
            }
            start = end;
        }
        if (divideTo < 0)
            return best;
        size = size >> 1;
    }
}
// Find a shared substring that is at least half the length of the
// longer range. Returns an array describing the substring [startA,
// startB, len], or null.
function halfMatch(a, fromA, toA, b, fromB, toB) {
    let lenA = toA - fromA, lenB = toB - fromB;
    if (lenA < lenB) {
        let result = halfMatch(b, fromB, toB, a, fromA, toA);
        return result && [result[1], result[0], result[2]];
    }
    // From here a is known to be at least as long as b
    if (lenA < 4 || lenB * 2 < lenA)
        return null;
    return findMatch(a, fromA, toA, b, fromB, toB, Math.floor(lenA / 4), -1);
}
function crudeMatch(a, fromA, toA, b, fromB, toB) {
    crude = true;
    let lenA = toA - fromA, lenB = toB - fromB;
    let result;
    if (lenA < lenB) {
        let inv = findMatch(b, fromB, toB, a, fromA, toA, Math.floor(lenA / 6), 50);
        result = inv && [inv[1], inv[0], inv[2]];
    }
    else {
        result = findMatch(a, fromA, toA, b, fromB, toB, Math.floor(lenB / 6), 50);
    }
    if (!result)
        return [new Change(fromA, toA, fromB, toB)];
    let [sharedA, sharedB, sharedLen] = result;
    return findDiff(a, fromA, sharedA, b, fromB, sharedB)
        .concat(findDiff(a, sharedA + sharedLen, toA, b, sharedB + sharedLen, toB));
}
function mergeAdjacent(changes, minGap) {
    for (let i = 1; i < changes.length; i++) {
        let prev = changes[i - 1], cur = changes[i];
        if (prev.toA > cur.fromA - minGap && prev.toB > cur.fromB - minGap) {
            changes[i - 1] = new Change(prev.fromA, cur.toA, prev.fromB, cur.toB);
            changes.splice(i--, 1);
        }
    }
}
// Reorder and merge changes
function normalize(a, b, changes) {
    for (;;) {
        mergeAdjacent(changes, 1);
        let moved = false;
        // Move unchanged ranges that can be fully moved across an
        // adjacent insertion/deletion, to simplify the diff.
        for (let i = 0; i < changes.length; i++) {
            let ch = changes[i], pre, post;
            // The half-match heuristic sometimes produces non-minimal
            // diffs. Strip matching pre- and post-fixes again here.
            if (pre = commonPrefix(a, ch.fromA, ch.toA, b, ch.fromB, ch.toB))
                ch = changes[i] = new Change(ch.fromA + pre, ch.toA, ch.fromB + pre, ch.toB);
            if (post = commonSuffix(a, ch.fromA, ch.toA, b, ch.fromB, ch.toB))
                ch = changes[i] = new Change(ch.fromA, ch.toA - post, ch.fromB, ch.toB - post);
            let lenA = ch.toA - ch.fromA, lenB = ch.toB - ch.fromB;
            // Only look at plain insertions/deletions
            if (lenA && lenB)
                continue;
            let beforeLen = ch.fromA - (i ? changes[i - 1].toA : 0);
            let afterLen = (i < changes.length - 1 ? changes[i + 1].fromA : a.length) - ch.toA;
            if (!beforeLen || !afterLen)
                continue;
            let text = lenA ? a.slice(ch.fromA, ch.toA) : b.slice(ch.fromB, ch.toB);
            if (beforeLen <= text.length &&
                a.slice(ch.fromA - beforeLen, ch.fromA) == text.slice(text.length - beforeLen)) {
                // Text before matches the end of the change
                changes[i] = new Change(ch.fromA - beforeLen, ch.toA - beforeLen, ch.fromB - beforeLen, ch.toB - beforeLen);
                moved = true;
            }
            else if (afterLen <= text.length &&
                a.slice(ch.toA, ch.toA + afterLen) == text.slice(0, afterLen)) {
                // Text after matches the start of the change
                changes[i] = new Change(ch.fromA + afterLen, ch.toA + afterLen, ch.fromB + afterLen, ch.toB + afterLen);
                moved = true;
            }
        }
        if (!moved)
            break;
    }
    return changes;
}
// Process a change set to make it suitable for presenting to users.
function makePresentable(changes, a, b) {
    for (let posA = 0, i = 0; i < changes.length; i++) {
        let change = changes[i];
        let lenA = change.toA - change.fromA, lenB = change.toB - change.fromB;
        // Don't touch short insertions or deletions.
        if (lenA && lenB || lenA > 3 || lenB > 3) {
            let nextChangeA = i == changes.length - 1 ? a.length : changes[i + 1].fromA;
            let maxScanBefore = change.fromA - posA, maxScanAfter = nextChangeA - change.toA;
            let boundBefore = findWordBoundaryBefore(a, change.fromA, maxScanBefore);
            let boundAfter = findWordBoundaryAfter(a, change.toA, maxScanAfter);
            let lenBefore = change.fromA - boundBefore, lenAfter = boundAfter - change.toA;
            // An insertion or deletion that falls inside words on both
            // sides can maybe be moved to align with word boundaries.
            if ((!lenA || !lenB) && lenBefore && lenAfter) {
                let changeLen = Math.max(lenA, lenB);
                let [changeText, changeFrom, changeTo] = lenA ? [a, change.fromA, change.toA] : [b, change.fromB, change.toB];
                if (changeLen > lenBefore &&
                    a.slice(boundBefore, change.fromA) == changeText.slice(changeTo - lenBefore, changeTo)) {
                    change = changes[i] = new Change(boundBefore, boundBefore + lenA, change.fromB - lenBefore, change.toB - lenBefore);
                    boundBefore = change.fromA;
                    boundAfter = findWordBoundaryAfter(a, change.toA, nextChangeA - change.toA);
                }
                else if (changeLen > lenAfter &&
                    a.slice(change.toA, boundAfter) == changeText.slice(changeFrom, changeFrom + lenAfter)) {
                    change = changes[i] = new Change(boundAfter - lenA, boundAfter, change.fromB + lenAfter, change.toB + lenAfter);
                    boundAfter = change.toA;
                    boundBefore = findWordBoundaryBefore(a, change.fromA, change.fromA - posA);
                }
                lenBefore = change.fromA - boundBefore;
                lenAfter = boundAfter - change.toA;
            }
            if (lenBefore || lenAfter) {
                // Expand the change to cover the entire word
                change = changes[i] = new Change(change.fromA - lenBefore, change.toA + lenAfter, change.fromB - lenBefore, change.toB + lenAfter);
            }
            else if (!lenA) {
                // Align insertion to line boundary, when possible
                let first = findLineBreakAfter(b, change.fromB, change.toB), len;
                let last = first < 0 ? -1 : findLineBreakBefore(b, change.toB, change.fromB);
                if (first > -1 && (len = first - change.fromB) <= maxScanAfter &&
                    b.slice(change.fromB, first) == b.slice(change.toB, change.toB + len))
                    change = changes[i] = change.offset(len);
                else if (last > -1 && (len = change.toB - last) <= maxScanBefore &&
                    b.slice(change.fromB - len, change.fromB) == b.slice(last, change.toB))
                    change = changes[i] = change.offset(-len);
            }
            else if (!lenB) {
                // Align deletion to line boundary
                let first = findLineBreakAfter(a, change.fromA, change.toA), len;
                let last = first < 0 ? -1 : findLineBreakBefore(a, change.toA, change.fromA);
                if (first > -1 && (len = first - change.fromA) <= maxScanAfter &&
                    a.slice(change.fromA, first) == a.slice(change.toA, change.toA + len))
                    change = changes[i] = change.offset(len);
                else if (last > -1 && (len = change.toA - last) <= maxScanBefore &&
                    a.slice(change.fromA - len, change.fromA) == a.slice(last, change.toA))
                    change = changes[i] = change.offset(-len);
            }
        }
        posA = change.toA;
    }
    mergeAdjacent(changes, 3);
    return changes;
}
let wordChar;
try {
    wordChar = new RegExp("[\\p{Alphabetic}\\p{Number}]", "u");
}
catch (_) { }
function asciiWordChar(code) {
    return code > 48 && code < 58 || code > 64 && code < 91 || code > 96 && code < 123;
}
function wordCharAfter(s, pos) {
    if (pos == s.length)
        return 0;
    let next = s.charCodeAt(pos);
    if (next < 192)
        return asciiWordChar(next) ? 1 : 0;
    if (!wordChar)
        return 0;
    if (!isSurrogate1(next) || pos == s.length - 1)
        return wordChar.test(String.fromCharCode(next)) ? 1 : 0;
    return wordChar.test(s.slice(pos, pos + 2)) ? 2 : 0;
}
function wordCharBefore(s, pos) {
    if (!pos)
        return 0;
    let prev = s.charCodeAt(pos - 1);
    if (prev < 192)
        return asciiWordChar(prev) ? 1 : 0;
    if (!wordChar)
        return 0;
    if (!isSurrogate2(prev) || pos == 1)
        return wordChar.test(String.fromCharCode(prev)) ? 1 : 0;
    return wordChar.test(s.slice(pos - 2, pos)) ? 2 : 0;
}
const MAX_SCAN = 8;
function findWordBoundaryAfter(s, pos, max) {
    if (pos == s.length || !wordCharBefore(s, pos))
        return pos;
    for (let cur = pos, end = pos + max, i = 0; i < MAX_SCAN; i++) {
        let size = wordCharAfter(s, cur);
        if (!size || cur + size > end)
            return cur;
        cur += size;
    }
    return pos;
}
function findWordBoundaryBefore(s, pos, max) {
    if (!pos || !wordCharAfter(s, pos))
        return pos;
    for (let cur = pos, end = pos - max, i = 0; i < MAX_SCAN; i++) {
        let size = wordCharBefore(s, cur);
        if (!size || cur - size < end)
            return cur;
        cur -= size;
    }
    return pos;
}
function findLineBreakBefore(s, pos, stop) {
    for (; pos != stop; pos--)
        if (s.charCodeAt(pos - 1) == 10)
            return pos;
    return -1;
}
function findLineBreakAfter(s, pos, stop) {
    for (; pos != stop; pos++)
        if (s.charCodeAt(pos) == 10)
            return pos;
    return -1;
}
const isSurrogate1 = (code) => code >= 0xD800 && code <= 0xDBFF;
const isSurrogate2 = (code) => code >= 0xDC00 && code <= 0xDFFF;
// Returns false if index looks like it is in the middle of a
// surrogate pair.
function validIndex(s, index) {
    return !index || index == s.length || !isSurrogate1(s.charCodeAt(index - 1)) || !isSurrogate2(s.charCodeAt(index));
}
/**
Compute the difference between two strings.
*/
function diff(a, b, config) {
    var _a;
    let override = config === null || config === void 0 ? void 0 : config.override;
    if (override)
        return override(a, b);
    scanLimit = ((_a = config === null || config === void 0 ? void 0 : config.scanLimit) !== null && _a !== void 0 ? _a : 1e9) >> 1;
    timeout = (config === null || config === void 0 ? void 0 : config.timeout) ? Date.now() + config.timeout : 0;
    crude = false;
    return normalize(a, b, findDiff(a, 0, a.length, b, 0, b.length));
}
// Return whether the last diff fell back to the imprecise algorithm.
function diffIsPrecise() { return !crude; }
/**
Compute the difference between the given strings, and clean up the
resulting diff for presentation to users by dropping short
unchanged ranges, and aligning changes to word boundaries when
appropriate.
*/
function presentableDiff(a, b, config) {
    return makePresentable(diff(a, b, config), a, b);
}

const mergeConfig = state.Facet.define({
    combine: values => values[0]
});
const setChunks = state.StateEffect.define();
const computeChunks = state.Facet.define();
const ChunkField = state.StateField.define({
    create(state) {
        return null;
    },
    update(current, tr) {
        for (let e of tr.effects)
            if (e.is(setChunks))
                current = e.value;
        for (let comp of tr.state.facet(computeChunks))
            current = comp(current, tr);
        return current;
    }
});
/**
Get the changed chunks for the merge view that this editor is part
of, plus the side it is on if it is part of a `MergeView`. Returns
null if the editor doesn't have a merge extension active or the
merge view hasn't finished initializing yet.
*/
function getChunks(state) {
    let field = state.field(ChunkField, false);
    if (!field)
        return null;
    let conf = state.facet(mergeConfig);
    return { chunks: field, side: conf ? conf.side : null };
}
let moveByChunk = (dir) => ({ state: state$1, dispatch }) => {
    let chunks = state$1.field(ChunkField, false), conf = state$1.facet(mergeConfig);
    if (!chunks || !chunks.length || !conf)
        return false;
    let { head } = state$1.selection.main, pos = 0;
    for (let i = chunks.length - 1; i >= 0; i--) {
        let chunk = chunks[i];
        let [from, to] = conf.side == "b" ? [chunk.fromB, chunk.toB] : [chunk.fromA, chunk.toA];
        if (to < head) {
            pos = i + 1;
            break;
        }
        if (from <= head) {
            if (chunks.length == 1)
                return false;
            pos = i + (dir < 0 ? 0 : 1);
            break;
        }
    }
    let next = chunks[(pos + (dir < 0 ? chunks.length - 1 : 0)) % chunks.length];
    let [from, to] = conf.side == "b" ? [next.fromB, next.toB] : [next.fromA, next.toA];
    dispatch(state$1.update({
        selection: { anchor: from },
        userEvent: "select.byChunk",
        effects: view.EditorView.scrollIntoView(state.EditorSelection.range(to, from))
    }));
    return true;
};
/**
Move the selection to the next changed chunk.
*/
const goToNextChunk = moveByChunk(1);
/**
Move the selection to the previous changed chunk.
*/
const goToPreviousChunk = moveByChunk(-1);

/**
A chunk describes a range of lines which have changed content in
them. Either side (a/b) may either be empty (when its `to` is
equal to its `from`), or points at a range starting at the start
of the first changed line, to 1 past the end of the last changed
line. Note that `to` positions may point past the end of the
document. Use `endA`/`endB` if you need an end position that is
certain to be a valid document position.
*/
class Chunk {
    constructor(
    /**
    The individual changes inside this chunk. These are stored
    relative to the start of the chunk, so you have to add
    `chunk.fromA`/`fromB` to get document positions.
    */
    changes, 
    /**
    The start of the chunk in document A.
    */
    fromA, 
    /**
    The end of the chunk in document A. This is equal to `fromA`
    when the chunk covers no lines in document A, or is one unit
    past the end of the last line in the chunk if it does.
    */
    toA, 
    /**
    The start of the chunk in document B.
    */
    fromB, 
    /**
    The end of the chunk in document A.
    */
    toB, 
    /**
    This is set to false when the diff used to compute this chunk
    fell back to fast, imprecise diffing.
    */
    precise = true) {
        this.changes = changes;
        this.fromA = fromA;
        this.toA = toA;
        this.fromB = fromB;
        this.toB = toB;
        this.precise = precise;
    }
    /**
    @internal
    */
    offset(offA, offB) {
        return offA || offB
            ? new Chunk(this.changes, this.fromA + offA, this.toA + offA, this.fromB + offB, this.toB + offB, this.precise)
            : this;
    }
    /**
    Returns `fromA` if the chunk is empty in A, or the end of the
    last line in the chunk otherwise.
    */
    get endA() { return Math.max(this.fromA, this.toA - 1); }
    /**
    Returns `fromB` if the chunk is empty in B, or the end of the
    last line in the chunk otherwise.
    */
    get endB() { return Math.max(this.fromB, this.toB - 1); }
    /**
    Build a set of changed chunks for the given documents.
    */
    static build(a, b, conf) {
        let diff = presentableDiff(a.toString(), b.toString(), conf);
        return toChunks(diff, a, b, 0, 0, diffIsPrecise());
    }
    /**
    Update a set of chunks for changes in document A. `a` should
    hold the updated document A.
    */
    static updateA(chunks, a, b, changes, conf) {
        return updateChunks(findRangesForChange(chunks, changes, true, b.length), chunks, a, b, conf);
    }
    /**
    Update a set of chunks for changes in document B.
    */
    static updateB(chunks, a, b, changes, conf) {
        return updateChunks(findRangesForChange(chunks, changes, false, a.length), chunks, a, b, conf);
    }
}
function fromLine(fromA, fromB, a, b) {
    let lineA = a.lineAt(fromA), lineB = b.lineAt(fromB);
    return lineA.to == fromA && lineB.to == fromB && fromA < a.length && fromB < b.length
        ? [fromA + 1, fromB + 1] : [lineA.from, lineB.from];
}
function toLine(toA, toB, a, b) {
    let lineA = a.lineAt(toA), lineB = b.lineAt(toB);
    return lineA.from == toA && lineB.from == toB ? [toA, toB] : [lineA.to + 1, lineB.to + 1];
}
function toChunks(changes, a, b, offA, offB, precise) {
    let chunks = [];
    for (let i = 0; i < changes.length; i++) {
        let change = changes[i];
        let [fromA, fromB] = fromLine(change.fromA + offA, change.fromB + offB, a, b);
        let [toA, toB] = toLine(change.toA + offA, change.toB + offB, a, b);
        let chunk = [change.offset(-fromA + offA, -fromB + offB)];
        while (i < changes.length - 1) {
            let next = changes[i + 1];
            let [nextA, nextB] = fromLine(next.fromA + offA, next.fromB + offB, a, b);
            if (nextA > toA + 1 && nextB > toB + 1)
                break;
            chunk.push(next.offset(-fromA + offA, -fromB + offB));
            [toA, toB] = toLine(next.toA + offA, next.toB + offB, a, b);
            i++;
        }
        chunks.push(new Chunk(chunk, fromA, Math.max(fromA, toA), fromB, Math.max(fromB, toB), precise));
    }
    return chunks;
}
const updateMargin = 1000;
// Finds the given position in the chunks. Returns the extent of the
// chunk it overlaps with if it overlaps, or a position corresponding
// to that position on both sides otherwise.
function findPos(chunks, pos, isA, start) {
    let lo = 0, hi = chunks.length;
    for (;;) {
        if (lo == hi) {
            let refA = 0, refB = 0;
            if (lo)
                ({ toA: refA, toB: refB } = chunks[lo - 1]);
            let off = pos - (isA ? refA : refB);
            return [refA + off, refB + off];
        }
        let mid = (lo + hi) >> 1, chunk = chunks[mid];
        let [from, to] = isA ? [chunk.fromA, chunk.toA] : [chunk.fromB, chunk.toB];
        if (from > pos)
            hi = mid;
        else if (to <= pos)
            lo = mid + 1;
        else
            return start ? [chunk.fromA, chunk.fromB] : [chunk.toA, chunk.toB];
    }
}
function findRangesForChange(chunks, changes, isA, otherLen) {
    let ranges = [];
    changes.iterChangedRanges((cFromA, cToA, cFromB, cToB) => {
        let fromA = 0, toA = isA ? changes.length : otherLen;
        let fromB = 0, toB = isA ? otherLen : changes.length;
        if (cFromA > updateMargin)
            [fromA, fromB] = findPos(chunks, cFromA - updateMargin, isA, true);
        if (cToA < changes.length - updateMargin)
            [toA, toB] = findPos(chunks, cToA + updateMargin, isA, false);
        let lenDiff = (cToB - cFromB) - (cToA - cFromA), last;
        let [diffA, diffB] = isA ? [lenDiff, 0] : [0, lenDiff];
        if (ranges.length && (last = ranges[ranges.length - 1]).toA >= fromA)
            ranges[ranges.length - 1] = { fromA: last.fromA, fromB: last.fromB, toA, toB,
                diffA: last.diffA + diffA, diffB: last.diffB + diffB };
        else
            ranges.push({ fromA, toA, fromB, toB, diffA, diffB });
    });
    return ranges;
}
function updateChunks(ranges, chunks, a, b, conf) {
    if (!ranges.length)
        return chunks;
    let result = [];
    for (let i = 0, offA = 0, offB = 0, chunkI = 0;; i++) {
        let range = i == ranges.length ? null : ranges[i];
        let fromA = range ? range.fromA + offA : a.length, fromB = range ? range.fromB + offB : b.length;
        while (chunkI < chunks.length) {
            let next = chunks[chunkI];
            if (next.endA + offA > fromA || next.endB + offB > fromB)
                break;
            result.push(next.offset(offA, offB));
            chunkI++;
        }
        if (!range)
            break;
        let toA = range.toA + offA + range.diffA, toB = range.toB + offB + range.diffB;
        let diff = presentableDiff(a.sliceString(fromA, toA), b.sliceString(fromB, toB), conf);
        for (let chunk of toChunks(diff, a, b, fromA, fromB, diffIsPrecise()))
            result.push(chunk);
        offA += range.diffA;
        offB += range.diffB;
        while (chunkI < chunks.length) {
            let next = chunks[chunkI];
            if (next.fromA + offA > toA && next.fromB + offB > toB)
                break;
            chunkI++;
        }
    }
    return result;
}
const defaultDiffConfig = { scanLimit: 500 };

const decorateChunks = view.ViewPlugin.fromClass(class {
    constructor(view) {
        ({ deco: this.deco, gutter: this.gutter } = getChunkDeco(view));
    }
    update(update) {
        if (update.docChanged || update.viewportChanged || chunksChanged(update.startState, update.state) ||
            configChanged(update.startState, update.state))
            ({ deco: this.deco, gutter: this.gutter } = getChunkDeco(update.view));
    }
}, {
    decorations: d => d.deco
});
const changeGutter = state.Prec.low(view.gutter({
    class: "cm-changeGutter",
    markers: view => { var _a; return ((_a = view.plugin(decorateChunks)) === null || _a === void 0 ? void 0 : _a.gutter) || state.RangeSet.empty; }
}));
function chunksChanged(s1, s2) {
    return s1.field(ChunkField, false) != s2.field(ChunkField, false);
}
function configChanged(s1, s2) {
    return s1.facet(mergeConfig) != s2.facet(mergeConfig);
}
const changedLine = view.Decoration.line({ class: "cm-changedLine" });
const changedText = view.Decoration.mark({ class: "cm-changedText" });
const inserted = view.Decoration.mark({ tagName: "ins", class: "cm-insertedLine" });
const deleted = view.Decoration.mark({ tagName: "del", class: "cm-deletedLine" });
const changedLineGutterMarker = new class extends view.GutterMarker {
    constructor() {
        super(...arguments);
        this.elementClass = "cm-changedLineGutter";
    }
};
function buildChunkDeco(chunk, doc, isA, highlight, builder, gutterBuilder) {
    let from = isA ? chunk.fromA : chunk.fromB, to = isA ? chunk.toA : chunk.toB;
    let changeI = 0;
    if (from != to) {
        builder.add(from, from, changedLine);
        builder.add(from, to, isA ? deleted : inserted);
        if (gutterBuilder)
            gutterBuilder.add(from, from, changedLineGutterMarker);
        for (let iter = doc.iterRange(from, to - 1), pos = from; !iter.next().done;) {
            if (iter.lineBreak) {
                pos++;
                builder.add(pos, pos, changedLine);
                if (gutterBuilder)
                    gutterBuilder.add(pos, pos, changedLineGutterMarker);
                continue;
            }
            let lineEnd = pos + iter.value.length;
            if (highlight)
                while (changeI < chunk.changes.length) {
                    let nextChange = chunk.changes[changeI];
                    let nextFrom = from + (isA ? nextChange.fromA : nextChange.fromB);
                    let nextTo = from + (isA ? nextChange.toA : nextChange.toB);
                    let chFrom = Math.max(pos, nextFrom), chTo = Math.min(lineEnd, nextTo);
                    if (chFrom < chTo)
                        builder.add(chFrom, chTo, changedText);
                    if (nextTo < lineEnd)
                        changeI++;
                    else
                        break;
                }
            pos = lineEnd;
        }
    }
}
function getChunkDeco(view) {
    let chunks = view.state.field(ChunkField);
    let { side, highlightChanges, markGutter, overrideChunk } = view.state.facet(mergeConfig), isA = side == "a";
    let builder = new state.RangeSetBuilder();
    let gutterBuilder = markGutter ? new state.RangeSetBuilder() : null;
    let { from, to } = view.viewport;
    for (let chunk of chunks) {
        if ((isA ? chunk.fromA : chunk.fromB) >= to)
            break;
        if ((isA ? chunk.toA : chunk.toB) > from) {
            if (!overrideChunk || !overrideChunk(view.state, chunk, builder, gutterBuilder))
                buildChunkDeco(chunk, view.state.doc, isA, highlightChanges, builder, gutterBuilder);
        }
    }
    return { deco: builder.finish(), gutter: gutterBuilder && gutterBuilder.finish() };
}
class Spacer extends view.WidgetType {
    constructor(height) {
        super();
        this.height = height;
    }
    eq(other) { return this.height == other.height; }
    toDOM() {
        let elt = document.createElement("div");
        elt.className = "cm-mergeSpacer";
        elt.style.height = this.height + "px";
        return elt;
    }
    updateDOM(dom) {
        dom.style.height = this.height + "px";
        return true;
    }
    get estimatedHeight() { return this.height; }
    ignoreEvent() { return false; }
}
const adjustSpacers = state.StateEffect.define({
    map: (value, mapping) => value.map(mapping)
});
const Spacers = state.StateField.define({
    create: () => view.Decoration.none,
    update: (spacers, tr) => {
        for (let e of tr.effects)
            if (e.is(adjustSpacers))
                return e.value;
        return spacers.map(tr.changes);
    },
    provide: f => view.EditorView.decorations.from(f)
});
const epsilon = .01;
function compareSpacers(a, b) {
    if (a.size != b.size)
        return false;
    let iA = a.iter(), iB = b.iter();
    while (iA.value) {
        if (iA.from != iB.from ||
            Math.abs(iA.value.spec.widget.height - iB.value.spec.widget.height) > 1)
            return false;
        iA.next();
        iB.next();
    }
    return true;
}
function updateSpacers(a, b, chunks) {
    let buildA = new state.RangeSetBuilder(), buildB = new state.RangeSetBuilder();
    let spacersA = a.state.field(Spacers).iter(), spacersB = b.state.field(Spacers).iter();
    let posA = 0, posB = 0, offA = 0, offB = 0, vpA = a.viewport, vpB = b.viewport;
    for (let chunkI = 0;; chunkI++) {
        let chunk = chunkI < chunks.length ? chunks[chunkI] : null;
        let endA = chunk ? chunk.fromA : a.state.doc.length, endB = chunk ? chunk.fromB : b.state.doc.length;
        // A range at posA/posB is unchanged, must be aligned.
        if (posA < endA) {
            let heightA = a.lineBlockAt(posA).top + offA;
            let heightB = b.lineBlockAt(posB).top + offB;
            let diff = heightA - heightB;
            if (diff < -epsilon) {
                offA -= diff;
                buildA.add(posA, posA, view.Decoration.widget({
                    widget: new Spacer(-diff),
                    block: true,
                    side: -1
                }));
            }
            else if (diff > epsilon) {
                offB += diff;
                buildB.add(posB, posB, view.Decoration.widget({
                    widget: new Spacer(diff),
                    block: true,
                    side: -1
                }));
            }
        }
        // If the viewport starts inside the unchanged range (on both
        // sides), add another sync at the top of the viewport. That way,
        // big unchanged chunks with possibly inaccurate estimated heights
        // won't cause the content to misalign (#1408)
        if (endA > posA + 1000 && posA < vpA.from && endA > vpA.from && posB < vpB.from && endB > vpB.from) {
            let off = Math.min(vpA.from - posA, vpB.from - posB);
            posA += off;
            posB += off;
            chunkI--;
        }
        else if (!chunk) {
            break;
        }
        else {
            posA = chunk.toA;
            posB = chunk.toB;
        }
        while (spacersA.value && spacersA.from < posA) {
            offA -= spacersA.value.spec.widget.height;
            spacersA.next();
        }
        while (spacersB.value && spacersB.from < posB) {
            offB -= spacersB.value.spec.widget.height;
            spacersB.next();
        }
    }
    while (spacersA.value) {
        offA -= spacersA.value.spec.widget.height;
        spacersA.next();
    }
    while (spacersB.value) {
        offB -= spacersB.value.spec.widget.height;
        spacersB.next();
    }
    let docDiff = (a.contentHeight + offA) - (b.contentHeight + offB);
    if (docDiff < epsilon) {
        buildA.add(a.state.doc.length, a.state.doc.length, view.Decoration.widget({
            widget: new Spacer(-docDiff),
            block: true,
            side: 1
        }));
    }
    else if (docDiff > epsilon) {
        buildB.add(b.state.doc.length, b.state.doc.length, view.Decoration.widget({
            widget: new Spacer(docDiff),
            block: true,
            side: 1
        }));
    }
    let decoA = buildA.finish(), decoB = buildB.finish();
    if (!compareSpacers(decoA, a.state.field(Spacers)))
        a.dispatch({ effects: adjustSpacers.of(decoA) });
    if (!compareSpacers(decoB, b.state.field(Spacers)))
        b.dispatch({ effects: adjustSpacers.of(decoB) });
}
/**
A state effect that expands the section of collapsed unchanged
code starting at the given position.
*/
const uncollapseUnchanged = state.StateEffect.define({
    map: (value, change) => change.mapPos(value)
});
/**
Query whether the given view is displayed next to another editor
in a merge view. Returns `null` if it isn't, and a pair of editors
(one of which will be the view itself) otherwise.
*/
function mergeViewSiblings(view) {
    let conf = view.state.facet(mergeConfig);
    return !conf || !conf.sibling ? null : conf.side == "a" ? { a: view, b: conf.sibling() } : { a: conf.sibling(), b: view };
}
class CollapseWidget extends view.WidgetType {
    constructor(lines) {
        super();
        this.lines = lines;
    }
    eq(other) { return this.lines == other.lines; }
    toDOM(view) {
        let outer = document.createElement("div");
        outer.className = "cm-collapsedLines";
        outer.textContent = view.state.phrase("$ unchanged lines", this.lines);
        outer.addEventListener("click", e => {
            let pos = view.posAtDOM(e.target);
            view.dispatch({ effects: uncollapseUnchanged.of(pos) });
            let { side, sibling } = view.state.facet(mergeConfig);
            if (sibling)
                sibling().dispatch({ effects: uncollapseUnchanged.of(mapPos(pos, view.state.field(ChunkField), side == "a")) });
        });
        return outer;
    }
    ignoreEvent(e) { return e instanceof MouseEvent; }
    get estimatedHeight() { return 27; }
    get type() { return "collapsed-unchanged-code"; }
}
function mapPos(pos, chunks, isA) {
    let startOur = 0, startOther = 0;
    for (let i = 0;; i++) {
        let next = i < chunks.length ? chunks[i] : null;
        if (!next || (isA ? next.fromA : next.fromB) >= pos)
            return startOther + (pos - startOur);
        [startOur, startOther] = isA ? [next.toA, next.toB] : [next.toB, next.toA];
    }
}
const CollapsedRanges = state.StateField.define({
    create(state) { return view.Decoration.none; },
    update(deco, tr) {
        deco = deco.map(tr.changes);
        for (let e of tr.effects)
            if (e.is(uncollapseUnchanged))
                deco = deco.update({ filter: from => from != e.value });
        return deco;
    },
    provide: f => view.EditorView.decorations.from(f)
});
function collapseUnchanged({ margin = 3, minSize = 4 }) {
    return CollapsedRanges.init(state => buildCollapsedRanges(state, margin, minSize));
}
function buildCollapsedRanges(state$1, margin, minLines) {
    let builder = new state.RangeSetBuilder();
    let isA = state$1.facet(mergeConfig).side == "a";
    let chunks = state$1.field(ChunkField);
    let prevLine = 1;
    for (let i = 0;; i++) {
        let chunk = i < chunks.length ? chunks[i] : null;
        let collapseFrom = i ? prevLine + margin : 1;
        let collapseTo = chunk ? state$1.doc.lineAt(isA ? chunk.fromA : chunk.fromB).number - 1 - margin : state$1.doc.lines;
        let lines = collapseTo - collapseFrom + 1;
        if (lines >= minLines) {
            builder.add(state$1.doc.line(collapseFrom).from, state$1.doc.line(collapseTo).to, view.Decoration.replace({
                widget: new CollapseWidget(lines),
                block: true
            }));
        }
        if (!chunk)
            break;
        prevLine = state$1.doc.lineAt(Math.min(state$1.doc.length, isA ? chunk.toA : chunk.toB)).number;
    }
    return builder.finish();
}

const externalTheme = view.EditorView.styleModule.of(new styleMod.StyleModule({
    ".cm-mergeView": {
        overflowY: "auto",
    },
    ".cm-mergeViewEditors": {
        display: "flex",
        alignItems: "stretch",
    },
    ".cm-mergeViewEditor": {
        flexGrow: 1,
        flexBasis: 0,
        overflow: "hidden"
    },
    ".cm-merge-revert": {
        width: "1.6em",
        flexGrow: 0,
        flexShrink: 0,
        position: "relative"
    },
    ".cm-merge-revert button": {
        position: "absolute",
        display: "block",
        width: "100%",
        boxSizing: "border-box",
        textAlign: "center",
        background: "none",
        border: "none",
        font: "inherit",
        cursor: "pointer"
    }
}));
const baseTheme = view.EditorView.baseTheme({
    ".cm-mergeView & .cm-scroller, .cm-mergeView &": {
        height: "auto !important",
        overflowY: "visible !important"
    },
    "&.cm-merge-a .cm-changedLine, .cm-deletedChunk": {
        backgroundColor: "rgba(160, 128, 100, .08)"
    },
    "&.cm-merge-b .cm-changedLine, .cm-inlineChangedLine": {
        backgroundColor: "rgba(100, 160, 128, .08)"
    },
    "&light.cm-merge-a .cm-changedText, &light .cm-deletedChunk .cm-deletedText": {
        background: "linear-gradient(#ee443366, #ee443366) bottom/100% 2px no-repeat",
    },
    "&dark.cm-merge-a .cm-changedText, &dark .cm-deletedChunk .cm-deletedText": {
        background: "linear-gradient(#ffaa9966, #ffaa9966) bottom/100% 2px no-repeat",
    },
    "&light.cm-merge-b .cm-changedText": {
        background: "linear-gradient(#22bb22aa, #22bb22aa) bottom/100% 2px no-repeat",
    },
    "&dark.cm-merge-b .cm-changedText": {
        background: "linear-gradient(#88ff88aa, #88ff88aa) bottom/100% 2px no-repeat",
    },
    "&.cm-merge-b .cm-deletedText": {
        background: "#ff000033"
    },
    ".cm-insertedLine, .cm-deletedLine, .cm-deletedLine del": {
        textDecoration: "none"
    },
    ".cm-deletedChunk": {
        paddingLeft: "6px",
        "& .cm-chunkButtons": {
            position: "absolute",
            insetInlineEnd: "5px"
        },
        "& button": {
            border: "none",
            cursor: "pointer",
            color: "white",
            margin: "0 2px",
            borderRadius: "3px",
            "&[name=accept]": { background: "#2a2" },
            "&[name=reject]": { background: "#d43" }
        },
    },
    ".cm-collapsedLines": {
        padding: "5px 5px 5px 10px",
        cursor: "pointer",
        "&:before": {
            content: '"⦚"',
            marginInlineEnd: "7px"
        },
        "&:after": {
            content: '"⦚"',
            marginInlineStart: "7px"
        },
    },
    "&light .cm-collapsedLines": {
        color: "#444",
        background: "linear-gradient(to bottom, transparent 0, #f3f3f3 30%, #f3f3f3 70%, transparent 100%)"
    },
    "&dark .cm-collapsedLines": {
        color: "#ddd",
        background: "linear-gradient(to bottom, transparent 0, #222 30%, #222 70%, transparent 100%)"
    },
    ".cm-changeGutter": { width: "3px", paddingLeft: "1px" },
    "&light.cm-merge-a .cm-changedLineGutter, &light .cm-deletedLineGutter": { background: "#e43" },
    "&dark.cm-merge-a .cm-changedLineGutter, &dark .cm-deletedLineGutter": { background: "#fa9" },
    "&light.cm-merge-b .cm-changedLineGutter": { background: "#2b2" },
    "&dark.cm-merge-b .cm-changedLineGutter": { background: "#8f8" },
    ".cm-inlineChangedLineGutter": { background: "#75d" }
});

const collapseCompartment = new state.Compartment, configCompartment = new state.Compartment;
/**
A merge view manages two editors side-by-side, highlighting the
difference between them and vertically aligning unchanged lines.
If you want one of the editors to be read-only, you have to
configure that in its extensions.

By default, views are not scrollable. Style them (`.cm-mergeView`)
with a height and `overflow: auto` to make them scrollable.
*/
class MergeView {
    /**
    Create a new merge view.
    */
    constructor(config) {
        this.revertDOM = null;
        this.revertToA = false;
        this.revertToLeft = false;
        this.measuring = -1;
        this.diffConf = config.diffConfig || defaultDiffConfig;
        let sharedExtensions = [
            state.Prec.low(decorateChunks),
            baseTheme,
            externalTheme,
            Spacers,
            view.EditorView.updateListener.of(update => {
                if (this.measuring < 0 && (update.heightChanged || update.viewportChanged) &&
                    !update.transactions.some(tr => tr.effects.some(e => e.is(adjustSpacers))))
                    this.measure();
            }),
        ];
        let configA = [mergeConfig.of({
                side: "a",
                sibling: () => this.b,
                highlightChanges: config.highlightChanges !== false,
                markGutter: config.gutter !== false
            })];
        if (config.gutter !== false)
            configA.push(changeGutter);
        let stateA = state.EditorState.create({
            doc: config.a.doc,
            selection: config.a.selection,
            extensions: [
                config.a.extensions || [],
                view.EditorView.editorAttributes.of({ class: "cm-merge-a" }),
                configCompartment.of(configA),
                sharedExtensions
            ]
        });
        let configB = [mergeConfig.of({
                side: "b",
                sibling: () => this.a,
                highlightChanges: config.highlightChanges !== false,
                markGutter: config.gutter !== false
            })];
        if (config.gutter !== false)
            configB.push(changeGutter);
        let stateB = state.EditorState.create({
            doc: config.b.doc,
            selection: config.b.selection,
            extensions: [
                config.b.extensions || [],
                view.EditorView.editorAttributes.of({ class: "cm-merge-b" }),
                configCompartment.of(configB),
                sharedExtensions
            ]
        });
        this.chunks = Chunk.build(stateA.doc, stateB.doc, this.diffConf);
        let add = [
            ChunkField.init(() => this.chunks),
            collapseCompartment.of(config.collapseUnchanged ? collapseUnchanged(config.collapseUnchanged) : [])
        ];
        stateA = stateA.update({ effects: state.StateEffect.appendConfig.of(add) }).state;
        stateB = stateB.update({ effects: state.StateEffect.appendConfig.of(add) }).state;
        this.dom = document.createElement("div");
        this.dom.className = "cm-mergeView";
        this.editorDOM = this.dom.appendChild(document.createElement("div"));
        this.editorDOM.className = "cm-mergeViewEditors";
        let orientation = config.orientation || "a-b";
        let wrapA = document.createElement("div");
        wrapA.className = "cm-mergeViewEditor";
        let wrapB = document.createElement("div");
        wrapB.className = "cm-mergeViewEditor";
        this.editorDOM.appendChild(orientation == "a-b" ? wrapA : wrapB);
        this.editorDOM.appendChild(orientation == "a-b" ? wrapB : wrapA);
        this.a = new view.EditorView({
            state: stateA,
            parent: wrapA,
            root: config.root,
            dispatchTransactions: trs => this.dispatch(trs, this.a)
        });
        this.b = new view.EditorView({
            state: stateB,
            parent: wrapB,
            root: config.root,
            dispatchTransactions: trs => this.dispatch(trs, this.b)
        });
        this.setupRevertControls(!!config.revertControls, config.revertControls == "b-to-a", config.renderRevertControl);
        if (config.parent)
            config.parent.appendChild(this.dom);
        this.scheduleMeasure();
    }
    dispatch(trs, target) {
        if (trs.some(tr => tr.docChanged)) {
            let last = trs[trs.length - 1];
            let changes = trs.reduce((chs, tr) => chs.compose(tr.changes), state.ChangeSet.empty(trs[0].startState.doc.length));
            this.chunks = target == this.a ? Chunk.updateA(this.chunks, last.newDoc, this.b.state.doc, changes, this.diffConf)
                : Chunk.updateB(this.chunks, this.a.state.doc, last.newDoc, changes, this.diffConf);
            target.update([...trs, last.state.update({ effects: setChunks.of(this.chunks) })]);
            let other = target == this.a ? this.b : this.a;
            other.update([other.state.update({ effects: setChunks.of(this.chunks) })]);
            this.scheduleMeasure();
        }
        else {
            target.update(trs);
        }
    }
    /**
    Reconfigure an existing merge view.
    */
    reconfigure(config) {
        if ("diffConfig" in config) {
            this.diffConf = config.diffConfig;
        }
        if ("orientation" in config) {
            let aB = config.orientation != "b-a";
            if (aB != (this.editorDOM.firstChild == this.a.dom.parentNode)) {
                let domA = this.a.dom.parentNode, domB = this.b.dom.parentNode;
                domA.remove();
                domB.remove();
                this.editorDOM.insertBefore(aB ? domA : domB, this.editorDOM.firstChild);
                this.editorDOM.appendChild(aB ? domB : domA);
                this.revertToLeft = !this.revertToLeft;
                if (this.revertDOM)
                    this.revertDOM.textContent = "";
            }
        }
        if ("revertControls" in config || "renderRevertControl" in config) {
            let controls = !!this.revertDOM, toA = this.revertToA, render = this.renderRevert;
            if ("revertControls" in config) {
                controls = !!config.revertControls;
                toA = config.revertControls == "b-to-a";
            }
            if ("renderRevertControl" in config)
                render = config.renderRevertControl;
            this.setupRevertControls(controls, toA, render);
        }
        let highlight = "highlightChanges" in config, gutter = "gutter" in config, collapse = "collapseUnchanged" in config;
        if (highlight || gutter || collapse) {
            let effectsA = [], effectsB = [];
            if (highlight || gutter) {
                let currentConfig = this.a.state.facet(mergeConfig);
                let markGutter = gutter ? config.gutter !== false : currentConfig.markGutter;
                let highlightChanges = highlight ? config.highlightChanges !== false : currentConfig.highlightChanges;
                effectsA.push(configCompartment.reconfigure([
                    mergeConfig.of({ side: "a", sibling: () => this.b, highlightChanges, markGutter }),
                    markGutter ? changeGutter : []
                ]));
                effectsB.push(configCompartment.reconfigure([
                    mergeConfig.of({ side: "b", sibling: () => this.a, highlightChanges, markGutter }),
                    markGutter ? changeGutter : []
                ]));
            }
            if (collapse) {
                let effect = collapseCompartment.reconfigure(config.collapseUnchanged ? collapseUnchanged(config.collapseUnchanged) : []);
                effectsA.push(effect);
                effectsB.push(effect);
            }
            this.a.dispatch({ effects: effectsA });
            this.b.dispatch({ effects: effectsB });
        }
        this.scheduleMeasure();
    }
    setupRevertControls(controls, toA, render) {
        this.revertToA = toA;
        this.revertToLeft = this.revertToA == (this.editorDOM.firstChild == this.a.dom.parentNode);
        this.renderRevert = render;
        if (!controls && this.revertDOM) {
            this.revertDOM.remove();
            this.revertDOM = null;
        }
        else if (controls && !this.revertDOM) {
            this.revertDOM = this.editorDOM.insertBefore(document.createElement("div"), this.editorDOM.firstChild.nextSibling);
            this.revertDOM.addEventListener("mousedown", e => this.revertClicked(e));
            this.revertDOM.className = "cm-merge-revert";
        }
        else if (this.revertDOM) {
            this.revertDOM.textContent = "";
        }
    }
    scheduleMeasure() {
        if (this.measuring < 0) {
            let win = (this.dom.ownerDocument.defaultView || window);
            this.measuring = win.requestAnimationFrame(() => {
                this.measuring = -1;
                this.measure();
            });
        }
    }
    measure() {
        updateSpacers(this.a, this.b, this.chunks);
        if (this.revertDOM)
            this.updateRevertButtons();
    }
    updateRevertButtons() {
        let dom = this.revertDOM, next = dom.firstChild;
        let vpA = this.a.viewport, vpB = this.b.viewport;
        for (let i = 0; i < this.chunks.length; i++) {
            let chunk = this.chunks[i];
            if (chunk.fromA > vpA.to || chunk.fromB > vpB.to)
                break;
            if (chunk.fromA < vpA.from || chunk.fromB < vpB.from)
                continue;
            let top = this.a.lineBlockAt(chunk.fromA).top + "px";
            while (next && +(next.dataset.chunk) < i)
                next = rm(next);
            if (next && next.dataset.chunk == String(i)) {
                if (next.style.top != top)
                    next.style.top = top;
                next = next.nextSibling;
            }
            else {
                dom.insertBefore(this.renderRevertButton(top, i), next);
            }
        }
        while (next)
            next = rm(next);
    }
    renderRevertButton(top, chunk) {
        let elt;
        if (this.renderRevert) {
            elt = this.renderRevert();
        }
        else {
            elt = document.createElement("button");
            let text = this.a.state.phrase("Revert this chunk");
            elt.setAttribute("aria-label", text);
            elt.setAttribute("title", text);
            elt.textContent = this.revertToLeft ? "⇜" : "⇝";
        }
        elt.style.top = top;
        elt.setAttribute("data-chunk", String(chunk));
        return elt;
    }
    revertClicked(e) {
        let target = e.target, chunk;
        while (target && target.parentNode != this.revertDOM)
            target = target.parentNode;
        if (target && (chunk = this.chunks[target.dataset.chunk])) {
            let [source, dest, srcFrom, srcTo, destFrom, destTo] = this.revertToA
                ? [this.b, this.a, chunk.fromB, chunk.toB, chunk.fromA, chunk.toA]
                : [this.a, this.b, chunk.fromA, chunk.toA, chunk.fromB, chunk.toB];
            let insert = source.state.sliceDoc(srcFrom, Math.max(srcFrom, srcTo - 1));
            if (srcFrom != srcTo && destTo <= dest.state.doc.length)
                insert += source.state.lineBreak;
            dest.dispatch({
                changes: { from: destFrom, to: Math.min(dest.state.doc.length, destTo), insert },
                userEvent: "revert"
            });
            e.preventDefault();
        }
    }
    /**
    Destroy this merge view.
    */
    destroy() {
        this.a.destroy();
        this.b.destroy();
        if (this.measuring > -1)
            (this.dom.ownerDocument.defaultView || window).cancelAnimationFrame(this.measuring);
        this.dom.remove();
    }
}
function rm(elt) {
    let next = elt.nextSibling;
    elt.remove();
    return next;
}

const deletedChunkGutterMarker = new class extends view.GutterMarker {
    constructor() {
        super(...arguments);
        this.elementClass = "cm-deletedLineGutter";
    }
};
const unifiedChangeGutter = state.Prec.low(view.gutter({
    class: "cm-changeGutter",
    markers: view => { var _a; return ((_a = view.plugin(decorateChunks)) === null || _a === void 0 ? void 0 : _a.gutter) || state.RangeSet.empty; },
    widgetMarker: (view, widget) => widget instanceof DeletionWidget ? deletedChunkGutterMarker : null
}));
/**
Create an extension that causes the editor to display changes
between its content and the given original document. Changed
chunks will be highlighted, with uneditable widgets displaying the
original text displayed above the new text.
*/
function unifiedMergeView(config) {
    var _a;
    let orig = typeof config.original == "string" ? state.Text.of(config.original.split(/\r?\n/)) : config.original;
    let diffConf = config.diffConfig || defaultDiffConfig;
    return [
        state.Prec.low(decorateChunks),
        deletedChunks,
        baseTheme,
        view.EditorView.editorAttributes.of({ class: "cm-merge-b" }),
        computeChunks.of((chunks, tr) => {
            let updateDoc = tr.effects.find(e => e.is(updateOriginalDoc));
            if (updateDoc)
                chunks = Chunk.updateA(chunks, updateDoc.value.doc, tr.startState.doc, updateDoc.value.changes, diffConf);
            if (tr.docChanged)
                chunks = Chunk.updateB(chunks, tr.state.field(originalDoc), tr.newDoc, tr.changes, diffConf);
            return chunks;
        }),
        mergeConfig.of({
            highlightChanges: config.highlightChanges !== false,
            markGutter: config.gutter !== false,
            syntaxHighlightDeletions: config.syntaxHighlightDeletions !== false,
            syntaxHighlightDeletionsMaxLength: 3000,
            mergeControls: (_a = config.mergeControls) !== null && _a !== void 0 ? _a : true,
            overrideChunk: config.allowInlineDiffs ? overrideChunkInline : undefined,
            side: "b"
        }),
        originalDoc.init(() => orig),
        config.gutter !== false ? unifiedChangeGutter : [],
        config.collapseUnchanged ? collapseUnchanged(config.collapseUnchanged) : [],
        ChunkField.init(state => Chunk.build(orig, state.doc, diffConf))
    ];
}
/**
The state effect used to signal changes in the original doc in a
unified merge view.
*/
const updateOriginalDoc = state.StateEffect.define();
/**
Create an effect that, when added to a transaction on a unified
merge view, will update the original document that's being compared against.
*/
function originalDocChangeEffect(state, changes) {
    return updateOriginalDoc.of({ doc: changes.apply(getOriginalDoc(state)), changes });
}
const originalDoc = state.StateField.define({
    create: () => state.Text.empty,
    update(doc, tr) {
        for (let e of tr.effects)
            if (e.is(updateOriginalDoc))
                doc = e.value.doc;
        return doc;
    }
});
/**
Get the original document from a unified merge editor's state.
*/
function getOriginalDoc(state) {
    return state.field(originalDoc);
}
const DeletionWidgets = new WeakMap;
class DeletionWidget extends view.WidgetType {
    constructor(buildDOM) {
        super();
        this.buildDOM = buildDOM;
        this.dom = null;
    }
    eq(other) { return this.dom == other.dom; }
    toDOM(view) { return this.dom || (this.dom = this.buildDOM(view)); }
}
function deletionWidget(state, chunk, hideContent) {
    let known = DeletionWidgets.get(chunk.changes);
    if (known)
        return known;
    let buildDOM = (view) => {
        let { highlightChanges, syntaxHighlightDeletions, syntaxHighlightDeletionsMaxLength, mergeControls } = state.facet(mergeConfig);
        let dom = document.createElement("div");
        dom.className = "cm-deletedChunk";
        if (mergeControls) {
            let buttons = dom.appendChild(document.createElement("div"));
            buttons.className = "cm-chunkButtons";
            let onAccept = (e) => { e.preventDefault(); acceptChunk(view, view.posAtDOM(dom)); };
            let onReject = (e) => { e.preventDefault(); rejectChunk(view, view.posAtDOM(dom)); };
            if (typeof mergeControls == "function") {
                buttons.appendChild(mergeControls("accept", onAccept));
                buttons.appendChild(mergeControls("reject", onReject));
            }
            else {
                let accept = buttons.appendChild(document.createElement("button"));
                accept.name = "accept";
                accept.textContent = state.phrase("Accept");
                accept.onmousedown = onAccept;
                let reject = buttons.appendChild(document.createElement("button"));
                reject.name = "reject";
                reject.textContent = state.phrase("Reject");
                reject.onmousedown = onReject;
            }
        }
        if (hideContent || chunk.fromA >= chunk.toA)
            return dom;
        let text = view.state.field(originalDoc).sliceString(chunk.fromA, chunk.endA);
        let lang = syntaxHighlightDeletions && state.facet(language.language);
        let line = makeLine();
        let changes = chunk.changes, changeI = 0, inside = false;
        function makeLine() {
            let div = dom.appendChild(document.createElement("div"));
            div.className = "cm-deletedLine";
            return div.appendChild(document.createElement("del"));
        }
        function add(from, to, cls) {
            for (let at = from; at < to;) {
                if (text.charAt(at) == "\n") {
                    if (!line.firstChild)
                        line.appendChild(document.createElement("br"));
                    line = makeLine();
                    at++;
                    continue;
                }
                let nextStop = to, nodeCls = cls + (inside ? " cm-deletedText" : ""), flip = false;
                let newline = text.indexOf("\n", at);
                if (newline > -1 && newline < to)
                    nextStop = newline;
                if (highlightChanges && changeI < changes.length) {
                    let nextBound = Math.max(0, inside ? changes[changeI].toA : changes[changeI].fromA);
                    if (nextBound <= nextStop) {
                        nextStop = nextBound;
                        if (inside)
                            changeI++;
                        flip = true;
                    }
                }
                if (nextStop > at) {
                    let node = document.createTextNode(text.slice(at, nextStop));
                    if (nodeCls) {
                        let span = line.appendChild(document.createElement("span"));
                        span.className = nodeCls;
                        span.appendChild(node);
                    }
                    else {
                        line.appendChild(node);
                    }
                    at = nextStop;
                }
                if (flip)
                    inside = !inside;
            }
        }
        if (lang && chunk.toA - chunk.fromA <= syntaxHighlightDeletionsMaxLength) {
            let tree = lang.parser.parse(text), pos = 0;
            highlight.highlightTree(tree, { style: tags => language.highlightingFor(state, tags) }, (from, to, cls) => {
                if (from > pos)
                    add(pos, from, "");
                add(from, to, cls);
                pos = to;
            });
            add(pos, text.length, "");
        }
        else {
            add(0, text.length, "");
        }
        if (!line.firstChild)
            line.appendChild(document.createElement("br"));
        return dom;
    };
    let deco = view.Decoration.widget({
        block: true,
        side: -1,
        widget: new DeletionWidget(buildDOM)
    });
    DeletionWidgets.set(chunk.changes, deco);
    return deco;
}
/**
In a [unified](https://codemirror.net/6/docs/ref/#merge.unifiedMergeView) merge view, accept the
chunk under the given position or the cursor. This chunk will no
longer be highlighted unless it is edited again.
*/
function acceptChunk(view, pos) {
    let { state: state$1 } = view, at = pos !== null && pos !== void 0 ? pos : state$1.selection.main.head;
    let chunk = view.state.field(ChunkField).find(ch => ch.fromB <= at && ch.endB >= at);
    if (!chunk)
        return false;
    let insert = view.state.sliceDoc(chunk.fromB, Math.max(chunk.fromB, chunk.toB - 1));
    let orig = view.state.field(originalDoc);
    if (chunk.fromB != chunk.toB && chunk.toA <= orig.length)
        insert += view.state.lineBreak;
    let changes = state.ChangeSet.of({ from: chunk.fromA, to: Math.min(orig.length, chunk.toA), insert }, orig.length);
    view.dispatch({
        effects: updateOriginalDoc.of({ doc: changes.apply(orig), changes }),
        userEvent: "accept"
    });
    return true;
}
/**
In a [unified](https://codemirror.net/6/docs/ref/#merge.unifiedMergeView) merge view, reject the
chunk under the given position or the cursor. Reverts that range
to the content it has in the original document.
*/
function rejectChunk(view, pos) {
    let { state } = view, at = pos !== null && pos !== void 0 ? pos : state.selection.main.head;
    let chunk = state.field(ChunkField).find(ch => ch.fromB <= at && ch.endB >= at);
    if (!chunk)
        return false;
    let orig = state.field(originalDoc);
    let insert = orig.sliceString(chunk.fromA, Math.max(chunk.fromA, chunk.toA - 1));
    if (chunk.fromA != chunk.toA && chunk.toB <= state.doc.length)
        insert += state.lineBreak;
    view.dispatch({
        changes: { from: chunk.fromB, to: Math.min(state.doc.length, chunk.toB), insert },
        userEvent: "revert"
    });
    return true;
}
function buildDeletedChunks(state$1) {
    let builder = new state.RangeSetBuilder();
    for (let ch of state$1.field(ChunkField)) {
        let hide = state$1.facet(mergeConfig).overrideChunk && chunkCanDisplayInline(state$1, ch);
        builder.add(ch.fromB, ch.fromB, deletionWidget(state$1, ch, !!hide));
    }
    return builder.finish();
}
const deletedChunks = state.StateField.define({
    create: state => buildDeletedChunks(state),
    update(deco, tr) {
        return tr.state.field(ChunkField, false) != tr.startState.field(ChunkField, false) ? buildDeletedChunks(tr.state) : deco;
    },
    provide: f => view.EditorView.decorations.from(f)
});
const InlineChunkCache = new WeakMap();
function chunkCanDisplayInline(state, chunk) {
    let result = InlineChunkCache.get(chunk);
    if (result !== undefined)
        return result;
    result = null;
    let a = state.field(originalDoc), b = state.doc;
    let linesA = a.lineAt(chunk.endA).number - a.lineAt(chunk.fromA).number + 1;
    let linesB = b.lineAt(chunk.endB).number - b.lineAt(chunk.fromB).number + 1;
    abort: if (linesA == linesB && linesA < 10) {
        let deco = [], deleteCount = 0;
        let bA = chunk.fromA, bB = chunk.fromB;
        for (let ch of chunk.changes) {
            if (ch.fromA < ch.toA) {
                deleteCount += ch.toA - ch.fromA;
                let deleted = a.sliceString(bA + ch.fromA, bA + ch.toA);
                if (/\n/.test(deleted))
                    break abort;
                deco.push(view.Decoration.widget({ widget: new InlineDeletion(deleted), side: -1 }).range(bB + ch.fromB));
            }
            if (ch.fromB < ch.toB) {
                deco.push(changedText.range(bB + ch.fromB, bB + ch.toB));
            }
        }
        if (deleteCount < (chunk.endA - chunk.fromA - linesA * 2))
            result = deco;
    }
    InlineChunkCache.set(chunk, result);
    return result;
}
class InlineDeletion extends view.WidgetType {
    constructor(text) {
        super();
        this.text = text;
    }
    eq(other) { return this.text == other.text; }
    toDOM(view) {
        let elt = document.createElement("del");
        elt.className = "cm-deletedText";
        elt.textContent = this.text;
        return elt;
    }
}
const inlineChangedLineGutterMarker = new class extends view.GutterMarker {
    constructor() {
        super(...arguments);
        this.elementClass = "cm-inlineChangedLineGutter";
    }
};
const inlineChangedLine = view.Decoration.line({ class: "cm-inlineChangedLine" });
function overrideChunkInline(state, chunk, builder, gutterBuilder) {
    let inline = chunkCanDisplayInline(state, chunk), i = 0;
    if (!inline)
        return false;
    for (let line = state.doc.lineAt(chunk.fromB);;) {
        if (gutterBuilder)
            gutterBuilder.add(line.from, line.from, inlineChangedLineGutterMarker);
        builder.add(line.from, line.from, inlineChangedLine);
        while (i < inline.length && inline[i].to <= line.to) {
            let r = inline[i++];
            builder.add(r.from, r.to, r.value);
        }
        if (line.to >= chunk.endB)
            break;
        line = state.doc.lineAt(line.to + 1);
    }
    return true;
}

exports.Change = Change;
exports.Chunk = Chunk;
exports.MergeView = MergeView;
exports.acceptChunk = acceptChunk;
exports.diff = diff;
exports.getChunks = getChunks;
exports.getOriginalDoc = getOriginalDoc;
exports.goToNextChunk = goToNextChunk;
exports.goToPreviousChunk = goToPreviousChunk;
exports.mergeViewSiblings = mergeViewSiblings;
exports.originalDocChangeEffect = originalDocChangeEffect;
exports.presentableDiff = presentableDiff;
exports.rejectChunk = rejectChunk;
exports.uncollapseUnchanged = uncollapseUnchanged;
exports.unifiedMergeView = unifiedMergeView;
exports.updateOriginalDoc = updateOriginalDoc;
