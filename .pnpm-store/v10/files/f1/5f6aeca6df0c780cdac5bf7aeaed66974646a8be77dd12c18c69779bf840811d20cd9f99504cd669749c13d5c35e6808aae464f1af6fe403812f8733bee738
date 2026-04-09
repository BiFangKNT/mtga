'use strict';

const tarItemTypeMap = {
  // Standard
  "0": "file",
  // Regular file
  "1": "hardLink",
  // Hard link (meta)
  "2": "symbolicLink",
  // Symbolic link (meta)
  "3": "characterDevice",
  // Character device (meta)
  "4": "blockDevice",
  // Block device (meta)
  "5": "directory",
  // Directory (meta)
  "6": "fifo",
  // Named pipe (FIFO) (meta)
  "7": "contiguousFile",
  // Contiguous file (rarely used, mostly for older systems)
  // Extended headers
  "g": "globalExtendedHeader",
  // Global extended header (meta)
  "x": "extendedHeader",
  // Extended header for the next file (meta)
  // GNU tar
  "D": "gnuDirectory",
  // GNU directory metadata (meta)
  "I": "gnuInodeMetadata",
  // GNU inode metadata
  "K": "gnuLongLinkName",
  // GNU long link name
  "L": "gnuLongFileName",
  // GNU long file name
  "N": "gnuOldLongFileName",
  // GNU long file name (old)
  "M": "gnuMultiVolume",
  // Multi-volume archive entry
  "S": "gnuSparseFile",
  // Sparse file (for files with holes)
  "E": "gnuExtendedSparse",
  // Extended sparse file (used in GNU tar for large sparse files)
  // Solaris tar
  "A": "solarisAcl",
  // Solaris access control list
  "V": "solarisVolumeLabel",
  // Solaris volume label (meta)
  "X": "solarisOldExtendedHeader"
  // Deprecated extended header format (meta)
};

function parseTar(data, opts) {
  const buffer = data.buffer || data;
  const files = [];
  let offset = 0;
  let nextExtendedHeader;
  let globalExtendedHeader;
  while (offset < buffer.byteLength - 512) {
    let name = _readString(buffer, offset, 100);
    if (name.length === 0) {
      break;
    }
    if (nextExtendedHeader) {
      const longName = nextExtendedHeader.path || nextExtendedHeader.linkpath;
      if (longName) {
        name = longName;
      }
    }
    const mode = _readString(buffer, offset + 100, 8).trim();
    const uid = Number.parseInt(_readString(buffer, offset + 108, 8));
    const gid = Number.parseInt(_readString(buffer, offset + 116, 8));
    const size = _readNumber(buffer, offset + 124, 12);
    const seek = 512 + 512 * Math.trunc(size / 512) + (size % 512 ? 512 : 0);
    const mtime = _readNumber(buffer, offset + 136, 12);
    const _type = _readString(buffer, offset + 156, 1) || "0";
    const type = tarItemTypeMap[_type] || _type;
    switch (type) {
      // Extended headers for next entry
      case "extendedHeader":
      case "globalExtendedHeader": {
        const headers = _parseExtendedHeaders(
          new Uint8Array(buffer, offset + 512, size)
        );
        if (type === "extendedHeader") {
          nextExtendedHeader = headers;
        } else {
          nextExtendedHeader = void 0;
          globalExtendedHeader = {
            ...globalExtendedHeader,
            ...headers
          };
        }
        offset += seek;
        continue;
      }
      // GNU tar long file names
      case "gnuLongFileName":
      case "gnuOldLongFileName":
      case "gnuLongLinkName": {
        nextExtendedHeader = { path: _readString(buffer, offset + 512, size) };
        offset += seek;
        continue;
      }
    }
    const user = _readString(buffer, offset + 265, 32);
    const group = _readString(buffer, offset + 297, 32);
    name = _sanitizePath(name);
    const meta = {
      name,
      type,
      size,
      attrs: {
        ...globalExtendedHeader,
        ...nextExtendedHeader,
        mode,
        uid,
        gid,
        mtime,
        user,
        group
      }
    };
    nextExtendedHeader = void 0;
    if (opts?.filter && !opts.filter(meta)) {
      offset += seek;
      continue;
    }
    if (opts?.metaOnly) {
      files.push(meta);
      offset += seek;
      continue;
    }
    const data2 = size === 0 ? void 0 : new Uint8Array(buffer, offset + 512, size);
    files.push({
      ...meta,
      data: data2,
      get text() {
        return new TextDecoder().decode(this.data);
      }
    });
    offset += seek;
  }
  return files;
}
async function parseTarGzip(data, opts = {}) {
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(new Uint8Array(data));
      controller.close();
    }
  }).pipeThrough(new DecompressionStream(opts.compression ?? "gzip"));
  const decompressedData = await new Response(stream).arrayBuffer();
  return parseTar(decompressedData, opts);
}
function _sanitizePath(path) {
  let normalized = path.replace(/\\/g, "/");
  normalized = normalized.replace(/^[a-zA-Z]:\//, "");
  normalized = normalized.replace(/^\/+/, "");
  const hasLeadingDotSlash = normalized.startsWith("./");
  const parts = normalized.split("/");
  const resolved = [];
  for (const part of parts) {
    if (part === "..") {
      resolved.pop();
    } else if (part !== "." && part !== "") {
      resolved.push(part);
    }
  }
  let result = resolved.join("/");
  if (hasLeadingDotSlash && !result.startsWith("./")) {
    result = "./" + result;
  }
  if (path.endsWith("/") && !result.endsWith("/")) {
    result += "/";
  }
  return result;
}
function _readString(buffer, offset, size) {
  const view = new Uint8Array(buffer, offset, size);
  const i = view.indexOf(0);
  const td = new TextDecoder();
  return td.decode(i === -1 ? view : view.slice(0, i));
}
function _readNumber(buffer, offset, size) {
  const view = new Uint8Array(buffer, offset, size);
  let str = "";
  for (let i = 0; i < size; i++) {
    str += String.fromCodePoint(view[i]);
  }
  return Number.parseInt(str, 8);
}
function _parseExtendedHeaders(data) {
  const dataStr = new TextDecoder().decode(data);
  const headers = {};
  for (const line of dataStr.split("\n")) {
    const s = line.split(" ")[1]?.split("=");
    if (s) {
      headers[s[0]] = s[1];
    }
  }
  return headers;
}

function createTar(files, opts = {}) {
  const _files = files.map((file) => {
    const data = _normalizeData(file.data);
    return {
      ...file,
      data,
      size: data?.length || 0
    };
  });
  let tarDataSize = 0;
  for (let i = 0; i < files.length; i++) {
    const size = _files[i].data?.length ?? 0;
    tarDataSize += 512 + 512 * Math.trunc(size / 512);
    if (size % 512) {
      tarDataSize += 512;
    }
  }
  let bufSize = 10240 * Math.trunc(tarDataSize / 10240);
  if (tarDataSize % 10240) {
    bufSize += 10240;
  }
  const buffer = new ArrayBuffer(bufSize);
  let offset = 0;
  for (const file of _files) {
    const isDir = !file.data;
    _writeString(buffer, file.name, offset, 100);
    const mode = file.attrs?.mode ?? opts.attrs?.mode ?? (isDir ? "775" : "664");
    _writeString(buffer, _leftPad(mode, 7), offset + 100, 8);
    const uid = file.attrs?.uid ?? opts.attrs?.uid ?? 1e3;
    _writeString(buffer, _leftPad(uid.toString(8), 7), offset + 108, 8);
    const gid = file.attrs?.gid ?? opts.attrs?.gid ?? 1e3;
    _writeString(buffer, _leftPad(gid.toString(8), 7), offset + 116, 8);
    _writeString(buffer, _leftPad(file.size.toString(8), 11), offset + 124, 12);
    const mtime = file.attrs?.mtime ?? opts.attrs?.mtime ?? Date.now();
    _writeString(
      buffer,
      _leftPad(Math.trunc(mtime / 1e3).toString(8), 11),
      offset + 136,
      12
    );
    const type = isDir ? "5" : "0";
    _writeString(buffer, type, offset + 156, 1);
    _writeString(
      buffer,
      "ustar",
      offset + 257,
      6
      /* magic string */
    );
    _writeString(
      buffer,
      "00",
      offset + 263,
      2
      /* magic version */
    );
    const user = file.attrs?.user ?? opts.attrs?.user ?? "";
    _writeString(buffer, user, offset + 265, 32);
    const group = file.attrs?.group ?? opts.attrs?.group ?? "";
    _writeString(buffer, group, offset + 297, 32);
    _writeString(buffer, "        ", offset + 148, 8);
    const header = new Uint8Array(buffer, offset, 512);
    let chksum = 0;
    for (let i = 0; i < 512; i++) {
      chksum += header[i];
    }
    _writeString(buffer, chksum.toString(8), offset + 148, 8);
    if (!isDir) {
      const destArray = new Uint8Array(buffer, offset + 512, file.size);
      for (let byteIdx = 0; byteIdx < file.size; byteIdx++) {
        destArray[byteIdx] = file.data[byteIdx];
      }
      offset += 512 * Math.trunc(file.size / 512);
      if (file.size % 512) {
        offset += 512;
      }
    }
    offset += 512;
  }
  return new Uint8Array(buffer);
}
function createTarGzipStream(files, opts = {}) {
  const buffer = createTar(files, opts);
  return new ReadableStream({
    start(controller) {
      controller.enqueue(buffer);
      controller.close();
    }
  }).pipeThrough(new CompressionStream(opts.compression ?? "gzip"));
}
async function createTarGzip(files, opts = {}) {
  const data = await new Response(createTarGzipStream(files, opts)).arrayBuffer().then((buffer) => new Uint8Array(buffer));
  return data;
}
function _writeString(buffer, str, offset, size) {
  const strView = new Uint8Array(buffer, offset, size);
  const te = new TextEncoder();
  const written = te.encodeInto(str, strView).written;
  for (let i = written; i < size; i++) {
    strView[i] = 0;
  }
}
function _leftPad(input, targetLength) {
  return String(input).padStart(targetLength, "0");
}
function _normalizeData(data) {
  if (data === null || data === void 0) {
    return void 0;
  }
  if (typeof data === "string") {
    return new TextEncoder().encode(data);
  }
  if (data instanceof ArrayBuffer) {
    return new Uint8Array(data);
  }
  return data;
}

exports.createTar = createTar;
exports.createTarGzip = createTarGzip;
exports.createTarGzipStream = createTarGzipStream;
exports.parseTar = parseTar;
exports.parseTarGzip = parseTarGzip;
