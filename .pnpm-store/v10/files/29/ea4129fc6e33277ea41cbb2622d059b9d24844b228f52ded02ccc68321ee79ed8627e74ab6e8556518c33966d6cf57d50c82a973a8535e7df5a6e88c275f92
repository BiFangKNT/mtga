type TarFileItemType = "file" | "hardLink" | "symbolicLink" | "characterDevice" | "blockDevice" | "directory" | "fifo" | "contiguousFile" | "globalExtendedHeader" | "extendedHeader" | "solarisAcl" | "gnuDirectory" | "gnuInodeMetadata" | "gnuLongLinkName" | "gnuLongFileName" | "gnuMultiVolume" | "gnuOldLongFileName" | "gnuSparseFile" | "solarisVolumeLabel" | "solarisOldExtendedHeader" | "gnuExtendedSparse";
type TarFileItemTypeValue = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "g" | "x" | "A" | "D" | "I" | "K" | "L" | "M" | "N" | "S" | "V" | "X" | "E";

type TarFileItem<DataT = Uint8Array> = {
    /**
     * File name
     */
    name: string;
    /**
     * The data associated with the file. This field is usually omitted for directories.
     * @optional
     */
    data?: DataT;
    /**
     * The attributes of the file. See {@link TarFileAttrs}.
     * @optional
     */
    attrs?: TarFileAttrs;
};
interface ParsedTarFileItem extends TarFileItem {
    /**
     * The type of file system element. It is usually `"file"` or `"directory"`.
     */
    type: TarFileItemType | undefined;
    /**
     * The size of the file in bytes.
     */
    size: number;
    /**
     * The textual representation of the file data. This property is read-only.
     */
    readonly text: string;
}
type ParsedTarFileItemMeta = Omit<ParsedTarFileItem, "data" | "text">;
interface TarFileAttrs {
    /**
     * File mode in octal (e.g., `664`) represents read, write, and execute permissions for the owner, group, and others.
     */
    mode?: string;
    /**
     * The user ID associated with the file.
     * @default 1000
     */
    uid?: number;
    /**
     * The group ID associated with the file.
     * @default 1000
     */
    gid?: number;
    /**
     * The modification time of the file, expressed as the number of milliseconds since the UNIX epoch.
     * @default Date.now()
     */
    mtime?: number;
    /**
     * The name of the user who owns the file.
     * @default ""
     */
    user?: string;
    /**
     * The name of the group that owns the file.
     * @default ""
     */
    group?: string;
}

interface ParseTarOptions {
    /**
     * A filter function that determines whether a file entry should be skipped or not.
     */
    filter?: (file: ParsedTarFileItemMeta) => boolean;
    /**
     * If `true`, only the metadata of the files will be parsed, and the file data will be omitted for listing purposes.
     */
    metaOnly?: boolean;
}
/**
 * Parses a TAR file from a binary buffer and returns an array of {@link TarFileItem} objects.
 *
 * @param {ArrayBuffer | Uint8Array} data - The binary data of the TAR file.
 * @returns {ParsedTarFileItem[]} An array of file items contained in the TAR file.
 */
declare function parseTar<_ = never, _Opts extends ParseTarOptions = ParseTarOptions, _ItemType extends ParsedTarFileItem | ParsedTarFileItemMeta = _Opts["metaOnly"] extends true ? ParsedTarFileItemMeta : ParsedTarFileItem>(data: ArrayBuffer | Uint8Array, opts?: _Opts): _ItemType[];
/**
 * Decompresses a gzipped TAR file and parses it to produce an array of file elements.
 * This function handles the decompression of the gzip format before parsing the contents of the TAR.
 *
 * @param {ArrayBuffer | Uint8Array} data - The binary data of the gzipped TAR file.
 * @param {object} opts - Decompression options.
 * @param {CompressionFormat} [opts.compression="gzip"] - Specifies the compression format to use, defaults to `"gzip"`.
 * @returns {Promise<TarFileItem[]>} A promise that resolves to an array of file items as described by {@link TarFileItem}.
 */
declare function parseTarGzip(data: ArrayBuffer | Uint8Array, opts?: ParseTarOptions & {
    compression?: CompressionFormat;
}): Promise<ParsedTarFileItem[]>;

interface CreateTarOptions {
    /**
     * Default attributes applied to all file unless overridden. See {@link TarFileAttrs}.
     * @optional
     */
    attrs?: TarFileAttrs;
}
type TarFileInput = TarFileItem<string | Uint8Array | ArrayBuffer>;
/**
 * Creates a TAR file from a list of file inputs and options, returning the TAR file as an `Uint8Array`.
 * This function takes care of normalising the file data, setting default attributes and calculating the TAR structure.
 *
 * @param {TarFileInput[]} files - An array of files to include in the TAR archive. Each file can contain different data types. See {@link TarFileInput}.
 * @param {CreateTarOptions} opts - File creation configuration options, including default file attributes. See {@link CreateTarOptions}.
 * @returns {Uint8Array} The TAR file encoded as an `Uint8Array`.
 */
declare function createTar(files: TarFileInput[], opts?: CreateTarOptions): Uint8Array;
/**
 * Creates a gzipped TAR file stream from an array of file inputs, using optional compression settings.
 *
 * @param {TarFileInput[]} files - The files to include in the gzipped TAR archive. See {@link TarFileInput}.
 * @param {CreateTarOptions & { Compression? CompressionFormat }} opts - Options for TAR creation and gzip compression. See {@link CreateTarOptions}.
 * @returns {ReadableStream} A stream of the gzipped TAR file data.
 */
declare function createTarGzipStream(files: TarFileInput[], opts?: CreateTarOptions & {
    compression?: CompressionFormat;
}): ReadableStream;
/**
 * Asynchronously creates a gzipped TAR file from an array of file inputs.
 * This function is suitable for scenarios where a complete gzipped TAR file is required as a single `Uint8` array.
 *
 * @param {TarFileInput[]} files - The files to include in the gzipped TAR archive.
 * @param {CreateTarOptions & { Compression? CompressionFormat }} opts - Options for TAR creation and gzip compression.
 * @returns {Promise<Uint8Array>} A promise that resolves to the gzipped TAR file as an Uint8Array.
 */
declare function createTarGzip(files: TarFileInput[], opts?: CreateTarOptions & {
    compression?: CompressionFormat;
}): Promise<Uint8Array>;

export { createTar, createTarGzip, createTarGzipStream, parseTar, parseTarGzip };
export type { CreateTarOptions, ParseTarOptions, ParsedTarFileItem, ParsedTarFileItemMeta, TarFileAttrs, TarFileInput, TarFileItem, TarFileItemType, TarFileItemTypeValue };
