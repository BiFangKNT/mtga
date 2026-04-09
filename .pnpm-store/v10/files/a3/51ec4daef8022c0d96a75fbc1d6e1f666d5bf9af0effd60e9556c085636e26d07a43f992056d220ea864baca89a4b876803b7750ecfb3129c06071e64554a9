import { SourceLocation } from '@babel/code-frame';

/**
 * Create a code frame from source code and location
 * @param source source code
 * @param location babel compatible location to highlight
 */
declare function createFrame(source: string, location: SourceLocation): string;
declare function tsLikeLocToBabelLoc(tsLoc: Record<'start' | 'end', {
    line: number;
    character: number;
} /** 0-based */>): SourceLocation;
declare function lineColLocToBabelLoc(d: {
    line: number;
    column: number;
    endLine?: number;
    endColumn?: number;
}): SourceLocation;
/**
 * Convert a [startOffset, length] range into a Babel-compatible SourceLocation.
 * - Lines/columns are 1-based.
 * - Offsets and length are clamped to source bounds.
 * - Single-pass up to the end offset, minimal allocations.
 */
declare function offsetRangeToBabelLocation(source: string, offset: number, length: number): SourceLocation;

export { createFrame, lineColLocToBabelLoc, offsetRangeToBabelLocation, tsLikeLocToBabelLoc };
