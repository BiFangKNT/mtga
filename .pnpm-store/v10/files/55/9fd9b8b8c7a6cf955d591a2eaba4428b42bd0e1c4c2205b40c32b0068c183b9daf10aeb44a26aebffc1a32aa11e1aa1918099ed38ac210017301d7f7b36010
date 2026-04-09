import process from "node:process";
import net from "node:net";
import { Buffer } from "node:buffer";
import { isTest } from "std-env";
//#region src/vite-node.ts
function getViteNodeOptionsEnvVar() {
	const envVar = process.env.NUXT_VITE_NODE_OPTIONS;
	try {
		return JSON.parse(envVar || "{}");
	} catch (e) {
		console.error("vite-node-shared: Failed to parse NUXT_VITE_NODE_OPTIONS environment variable.", e);
		return {};
	}
}
const viteNodeOptions = getViteNodeOptionsEnvVar();
const pendingRequests = /* @__PURE__ */ new Map();
let requestIdCounter = 0;
let clientSocket;
let currentConnectPromise;
const MAX_RETRY_ATTEMPTS = viteNodeOptions.maxRetryAttempts ?? 5;
const BASE_RETRY_DELAY_MS = viteNodeOptions.baseRetryDelay ?? 100;
const MAX_RETRY_DELAY_MS = viteNodeOptions.maxRetryDelay ?? 2e3;
const REQUEST_TIMEOUT_MS = viteNodeOptions.requestTimeout ?? 6e4;
/**
* Calculates exponential backoff delay with jitter.
* @param attempt - The current attempt number (0-based).
* @returns Delay in milliseconds.
*/
function calculateRetryDelay(attempt) {
	const exponentialDelay = BASE_RETRY_DELAY_MS * Math.pow(2, attempt);
	const jitter = Math.random() * .1 * exponentialDelay;
	return Math.min(exponentialDelay + jitter, MAX_RETRY_DELAY_MS);
}
/**
* Establishes or returns an existing IPC socket connection with retry logic.
* @returns A promise that resolves with the connected socket.
*/
function connectSocket() {
	if (clientSocket && !clientSocket.destroyed) return Promise.resolve(clientSocket);
	if (currentConnectPromise) return currentConnectPromise;
	const thisPromise = new Promise((resolve, reject) => {
		if (!viteNodeOptions.socketPath) {
			console.error("vite-node-shared: NUXT_VITE_NODE_OPTIONS.socketPath is not defined.");
			return reject(/* @__PURE__ */ new Error("Vite Node IPC socket path not configured."));
		}
		const attemptConnection = (attempt = 0) => {
			const socket = net.createConnection(viteNodeOptions.socketPath);
			const INITIAL_BUFFER_SIZE = 64 * 1024;
			const MAX_BUFFER_SIZE = 1024 * 1024 * 1024;
			let buffer = Buffer.alloc(INITIAL_BUFFER_SIZE);
			let writeOffset = 0;
			let readOffset = 0;
			socket.setNoDelay(true);
			socket.setKeepAlive(true, 3e4);
			const cleanup = () => {
				socket.off("connect", onConnect);
				socket.off("data", onData);
				socket.off("error", onError);
				socket.off("close", onClose);
			};
			const resetBuffer = () => {
				writeOffset = 0;
				readOffset = 0;
			};
			const compactBuffer = () => {
				if (readOffset > 0) {
					const remainingData = writeOffset - readOffset;
					if (remainingData > 0) buffer.copy(buffer, 0, readOffset, writeOffset);
					writeOffset = remainingData;
					readOffset = 0;
				}
			};
			const ensureBufferCapacity = (additionalBytes) => {
				const requiredSize = writeOffset + additionalBytes;
				if (requiredSize > MAX_BUFFER_SIZE) throw new Error(`Buffer size limit exceeded: ${requiredSize} > ${MAX_BUFFER_SIZE}`);
				if (requiredSize > buffer.length) {
					compactBuffer();
					if (writeOffset + additionalBytes > buffer.length) {
						const newSize = Math.min(Math.max(buffer.length * 2, requiredSize), MAX_BUFFER_SIZE);
						const newBuffer = Buffer.alloc(newSize);
						buffer.copy(newBuffer, 0, 0, writeOffset);
						buffer = newBuffer;
					}
				}
			};
			const onConnect = () => {
				clientSocket = socket;
				resolve(socket);
			};
			const onData = (data) => {
				try {
					ensureBufferCapacity(data.length);
					data.copy(buffer, writeOffset);
					writeOffset += data.length;
					while (writeOffset - readOffset >= 4) {
						const messageLength = buffer.readUInt32BE(readOffset);
						if (writeOffset - readOffset < 4 + messageLength) return;
						const message = buffer.subarray(readOffset + 4, readOffset + 4 + messageLength).toString("utf-8");
						readOffset += 4 + messageLength;
						try {
							const response = JSON.parse(message);
							const requestHandlers = pendingRequests.get(response.id);
							if (requestHandlers) {
								const { resolve: resolveRequest, reject: rejectRequest } = requestHandlers;
								if (response.type === "error") {
									const err = new Error(response.error.message);
									err.stack = response.error.stack;
									err.data = response.error.data;
									err.statusCode = err.status = response.error.status || response.error.statusCode;
									rejectRequest(err);
								} else resolveRequest(response.data);
								pendingRequests.delete(response.id);
							}
						} catch (parseError) {
							console.warn("vite-node-shared: Failed to parse IPC response:", parseError);
						}
					}
					if (readOffset > buffer.length / 2) compactBuffer();
				} catch (error) {
					socket.destroy(error instanceof Error ? error : /* @__PURE__ */ new Error("Buffer management error"));
				}
			};
			const onError = (err) => {
				cleanup();
				resetBuffer();
				if (attempt < MAX_RETRY_ATTEMPTS) {
					const delay = calculateRetryDelay(attempt);
					setTimeout(() => attemptConnection(attempt + 1), delay);
				} else {
					if (currentConnectPromise === thisPromise) reject(err);
					for (const { reject: rejectRequest } of pendingRequests.values()) rejectRequest(err);
					pendingRequests.clear();
					if (clientSocket === socket) clientSocket = void 0;
					if (currentConnectPromise === thisPromise) currentConnectPromise = void 0;
				}
			};
			const onClose = () => {
				cleanup();
				resetBuffer();
				for (const { reject: rejectRequest } of pendingRequests.values()) rejectRequest(/* @__PURE__ */ new Error("IPC connection closed"));
				pendingRequests.clear();
				if (clientSocket === socket) clientSocket = void 0;
				if (currentConnectPromise === thisPromise) currentConnectPromise = void 0;
			};
			socket.on("connect", onConnect);
			socket.on("data", onData);
			socket.on("error", onError);
			socket.on("close", onClose);
		};
		attemptConnection();
	});
	currentConnectPromise = thisPromise;
	return currentConnectPromise;
}
/**
* Sends a request over the IPC socket with automatic reconnection.
*/
async function sendRequest(type, payload) {
	const requestId = requestIdCounter++;
	let lastError;
	for (let requestAttempt = 0; requestAttempt <= MAX_RETRY_ATTEMPTS; requestAttempt++) try {
		const socket = await connectSocket();
		return await new Promise((resolve, reject) => {
			const timeoutId = setTimeout(() => {
				pendingRequests.delete(requestId);
				reject(/* @__PURE__ */ new Error(`Request timeout after ${REQUEST_TIMEOUT_MS}ms for type: ${type}`));
			}, REQUEST_TIMEOUT_MS);
			pendingRequests.set(requestId, {
				resolve: (value) => {
					clearTimeout(timeoutId);
					resolve(value);
				},
				reject: (reason) => {
					clearTimeout(timeoutId);
					reject(reason);
				}
			});
			const message = JSON.stringify({
				id: requestId,
				type,
				payload
			});
			const messageBuffer = Buffer.from(message, "utf-8");
			const messageLength = messageBuffer.length;
			const fullMessage = Buffer.alloc(4 + messageLength);
			fullMessage.writeUInt32BE(messageLength, 0);
			messageBuffer.copy(fullMessage, 4);
			try {
				socket.write(fullMessage);
			} catch (error) {
				clearTimeout(timeoutId);
				pendingRequests.delete(requestId);
				reject(error);
			}
		});
	} catch (error) {
		lastError = error;
		if (requestAttempt < MAX_RETRY_ATTEMPTS) {
			const delay = calculateRetryDelay(requestAttempt);
			await new Promise((resolve) => setTimeout(resolve, delay));
			if (clientSocket) {
				clientSocket.destroy();
				clientSocket = void 0;
			}
			currentConnectPromise = void 0;
		}
	}
	throw lastError || /* @__PURE__ */ new Error("Request failed after all retry attempts");
}
const viteNodeFetch = {
	getManifest() {
		return sendRequest("manifest", void 0);
	},
	getInvalidates() {
		return sendRequest("invalidates", void 0);
	},
	resolveId(id, importer) {
		return sendRequest("resolve", {
			id,
			importer
		});
	},
	fetchModule(moduleId) {
		return sendRequest("module", { moduleId });
	},
	ensureConnected() {
		return connectSocket();
	}
};
let preConnectAttempted = false;
function preConnect() {
	if (preConnectAttempted || !viteNodeOptions.socketPath) return;
	preConnectAttempted = true;
	return connectSocket().catch(() => {});
}
if (typeof process !== "undefined" && !isTest) setTimeout(preConnect, 100);
//#endregion
export { viteNodeFetch, viteNodeOptions };
