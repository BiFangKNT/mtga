import "../_chunks/_utils.mjs";
import { r as wrapFetch, t as errorPlugin } from "../_chunks/_plugins.mjs";
//#region src/adapters/_aws/utils.ts
function awsRequest(event, context) {
	const req = new Request(awsEventURL(event), {
		method: awsEventMethod(event),
		headers: awsEventHeaders(event),
		body: awsEventBody(event)
	});
	req.runtime = {
		name: "aws-lambda",
		awsLambda: {
			event,
			context
		}
	};
	req.ip = awsEventIP(event);
	return req;
}
function awsEventMethod(event) {
	return event.httpMethod || event.requestContext?.http?.method || "GET";
}
function awsEventIP(event) {
	return event.requestContext?.http?.sourceIp || event.requestContext?.identity?.sourceIp;
}
function awsEventURL(event) {
	const hostname = event.headers.host || event.headers.Host || event.requestContext?.domainName || ".";
	const path = event.path || event.rawPath;
	const query = awsEventQuery(event);
	const protocol = (event.headers["X-Forwarded-Proto"] || event.headers["x-forwarded-proto"]) === "http" ? "http" : "https";
	return new URL(`${path}${query ? `?${query}` : ""}`, `${protocol}://${hostname}`);
}
function awsEventQuery(event) {
	if (typeof event.rawQueryString === "string") return event.rawQueryString;
	return stringifyQuery({
		...event.queryStringParameters,
		...event.multiValueQueryStringParameters
	});
}
function awsEventHeaders(event) {
	const headers = new Headers();
	for (const [key, value] of Object.entries(event.headers)) if (value) headers.set(key, value);
	if ("cookies" in event && event.cookies) for (const cookie of event.cookies) headers.append("cookie", cookie);
	return headers;
}
function awsEventBody(event) {
	if (!event.body) return;
	if (event.isBase64Encoded) return Buffer.from(event.body || "", "base64");
	return event.body;
}
function awsResponseHeaders(response, event) {
	const headers = Object.create(null);
	for (const [key, value] of response.headers) if (value) headers[key] = Array.isArray(value) ? value.join(",") : String(value);
	const cookies = response.headers.getSetCookie();
	if (cookies.length === 0) return { headers };
	return event?.version === "2.0" || !!event?.requestContext?.http ? {
		headers,
		cookies
	} : {
		headers,
		cookies,
		multiValueHeaders: { "set-cookie": cookies }
	};
}
async function awsResponseBody(response) {
	if (!response.body) return { body: "" };
	const buffer = await toBuffer(response.body);
	return isTextType(response.headers.get("content-type") || "") ? { body: buffer.toString("utf8") } : {
		body: buffer.toString("base64"),
		isBase64Encoded: true
	};
}
async function awsStreamResponse(response, responseStream, event) {
	const metadata = {
		statusCode: response.status,
		...awsResponseHeaders(response, event)
	};
	if (!metadata.headers["transfer-encoding"]) metadata.headers["transfer-encoding"] = "chunked";
	const writer = globalThis.awslambda.HttpResponseStream.from(responseStream, metadata);
	if (!response.body) {
		writer.end();
		return;
	}
	try {
		await streamToNodeStream(response.body, writer);
	} finally {
		writer.end();
	}
}
async function streamToNodeStream(body, writer) {
	const reader = body.getReader();
	try {
		let result = await reader.read();
		while (!result.done) {
			if (!writer.write(result.value)) await new Promise((resolve) => writer.once("drain", resolve));
			result = await reader.read();
		}
	} finally {
		reader.releaseLock();
	}
}
function isTextType(contentType = "") {
	return /^text\/|\/(javascript|json|xml)|utf-?8/i.test(contentType);
}
function toBuffer(data) {
	return new Promise((resolve, reject) => {
		const chunks = [];
		data.pipeTo(new WritableStream({
			write(chunk) {
				chunks.push(chunk);
			},
			close() {
				resolve(Buffer.concat(chunks));
			},
			abort(reason) {
				reject(reason);
			}
		})).catch(reject);
	});
}
function stringifyQuery(obj) {
	const params = new URLSearchParams();
	for (const [key, value] of Object.entries(obj)) {
		if (value == null) continue;
		if (Array.isArray(value)) for (const v of value) params.append(key, String(v));
		else params.append(key, String(value));
	}
	return params.toString();
}
async function requestToAwsEvent(request) {
	const url = new URL(request.url);
	const headers = {};
	const cookies = [];
	for (const [key, value] of request.headers) {
		if (key.toLowerCase() === "cookie") cookies.push(value);
		headers[key] = value;
	}
	let body;
	let isBase64Encoded = false;
	if (request.body) {
		const buffer = await toBuffer(request.body);
		if (isTextType(request.headers.get("content-type") || "")) body = buffer.toString("utf8");
		else {
			body = buffer.toString("base64");
			isBase64Encoded = true;
		}
	}
	const now = Date.now();
	return {
		httpMethod: request.method,
		path: url.pathname,
		resource: url.pathname,
		queryStringParameters: Object.fromEntries(url.searchParams),
		multiValueQueryStringParameters: parseMultiValueQuery(url.searchParams),
		pathParameters: void 0,
		stageVariables: void 0,
		multiValueHeaders: Object.fromEntries([...request.headers].map(([k, v]) => [k, [v]])),
		version: "2.0",
		rawPath: url.pathname,
		rawQueryString: url.search.slice(1),
		cookies: cookies.length > 0 ? cookies : void 0,
		routeKey: `${request.method} ${url.pathname}`,
		headers,
		body: body ?? null,
		isBase64Encoded,
		requestContext: {
			accountId: "000000000000",
			apiId: "local",
			resourceId: "local",
			stage: "$default",
			requestId: crypto.randomUUID(),
			identity: {
				sourceIp: "127.0.0.1",
				userAgent: request.headers.get("user-agent") || "",
				accessKey: null,
				accountId: null,
				apiKey: null,
				apiKeyId: null,
				caller: null,
				clientCert: null,
				cognitoAuthenticationProvider: null,
				cognitoAuthenticationType: null,
				cognitoIdentityId: null,
				cognitoIdentityPoolId: null,
				principalOrgId: null,
				user: null,
				userArn: null
			},
			resourcePath: url.pathname,
			httpMethod: request.method,
			path: url.pathname,
			protocol: "HTTP/1.1",
			requestTimeEpoch: now,
			authorizer: void 0,
			domainName: url.hostname,
			http: {
				method: request.method,
				path: url.pathname,
				protocol: "HTTP/1.1",
				sourceIp: "127.0.0.1",
				userAgent: request.headers.get("user-agent") || ""
			},
			routeKey: `${request.method} ${url.pathname}`,
			time: new Date(now).toISOString(),
			timeEpoch: now,
			domainPrefix: url.hostname.split(".")[0]
		}
	};
}
function parseMultiValueQuery(params) {
	const result = {};
	for (const [key, value] of params) {
		if (!result[key]) result[key] = [];
		result[key].push(value);
	}
	return result;
}
function awsResultToResponse(result) {
	if (typeof result === "string") return new Response(result, { status: 200 });
	const headers = new Headers();
	if (result.headers) {
		for (const [key, value] of Object.entries(result.headers)) if (value !== void 0) headers.set(key, String(value));
	}
	if ("multiValueHeaders" in result && result.multiValueHeaders) {
		for (const [key, values] of Object.entries(result.multiValueHeaders)) if (values) for (const value of values) headers.append(key, String(value));
	}
	if ("cookies" in result && result.cookies) for (const cookie of result.cookies) headers.append("set-cookie", cookie);
	let body;
	if (typeof result.body === "string") if (result.isBase64Encoded) body = Buffer.from(result.body, "base64");
	else body = result.body;
	const statusCode = typeof result.statusCode === "number" ? result.statusCode : 200;
	return new Response(body, {
		status: statusCode,
		headers
	});
}
function createMockContext() {
	const id = crypto.randomUUID();
	return {
		callbackWaitsForEmptyEventLoop: true,
		functionName: "local",
		functionVersion: "$LATEST",
		invokedFunctionArn: `arn:aws:lambda:us-east-1:000000000000:function:local`,
		memoryLimitInMB: "128",
		awsRequestId: id,
		logGroupName: "/aws/lambda/local",
		logStreamName: `${(/* @__PURE__ */ new Date()).toISOString().split("T")[0]}/[$LATEST]${id}`,
		getRemainingTimeInMillis: () => 3e4,
		done: () => {},
		fail: () => {},
		succeed: () => {}
	};
}
//#endregion
//#region src/adapters/aws-lambda.ts
function toLambdaHandler(options) {
	const server = new AWSLambdaServer(options);
	return (event, context) => server.fetch(event, context);
}
async function handleLambdaEvent(fetchHandler, event, context) {
	const response = await fetchHandler(awsRequest(event, context));
	return {
		statusCode: response.status,
		...awsResponseHeaders(response, event),
		...await awsResponseBody(response)
	};
}
async function handleLambdaEventWithStream(fetchHandler, event, responseStream, context) {
	await awsStreamResponse(await fetchHandler(awsRequest(event, context)), responseStream, event);
}
async function invokeLambdaHandler(handler, request) {
	return awsResultToResponse(await handler(await requestToAwsEvent(request), createMockContext()));
}
var AWSLambdaServer = class {
	runtime = "aws-lambda";
	options;
	fetch;
	constructor(options) {
		this.options = {
			...options,
			middleware: [...options.middleware || []]
		};
		for (const plugin of options.plugins || []) plugin(this);
		errorPlugin(this);
		const fetchHandler = wrapFetch(this);
		this.fetch = (event, context) => handleLambdaEvent(fetchHandler, event, context);
	}
	serve() {}
	ready() {
		return Promise.resolve().then(() => this);
	}
	close() {
		return Promise.resolve();
	}
};
//#endregion
export { handleLambdaEvent, handleLambdaEventWithStream, invokeLambdaHandler, toLambdaHandler };
