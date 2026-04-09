type ImageMeta = {
    images?: Omit<ImageMeta, "images">[];
    width: number | undefined;
    height: number | undefined;
    orientation?: number;
    type?: string;
};

/**
 * @param {Uint8Array|string} input - Uint8Array or relative/absolute path of the image file
 * @param {Function=} [callback] - optional function for async detection
 */
declare function imageMeta(input: Uint8Array): ImageMeta;

export { imageMeta };
export type { ImageMeta };
