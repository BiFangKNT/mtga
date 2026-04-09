import "#nitro-internal-pollyfills";
import { lambda } from "./netlify-lambda.mjs";
export const handler = wrapHandler(lambda);
const BUILDER_FUNCTIONS_FLAG = true;
const HTTP_STATUS_METHOD_NOT_ALLOWED = 405;
const METADATA_VERSION = 1;
const augmentResponse = (response) => {
  if (!response) {
    return response;
  }
  const metadata = {
    version: METADATA_VERSION,
    builder_function: BUILDER_FUNCTIONS_FLAG,
    ttl: response.ttl || 0
  };
  return {
    ...response,
    metadata
  };
};
function wrapHandler(handler2) {
  return (event, context, callback) => {
    if (event.httpMethod !== "GET" && event.httpMethod !== "HEAD") {
      return Promise.resolve({
        body: "Method Not Allowed",
        statusCode: HTTP_STATUS_METHOD_NOT_ALLOWED
      });
    }
    const modifiedEvent = {
      ...event,
      multiValueQueryStringParameters: {},
      queryStringParameters: {}
    };
    const wrappedCallback = (error, response) => callback ? callback(error, augmentResponse(response)) : null;
    const execution = handler2(modifiedEvent, context, wrappedCallback);
    if (typeof execution === "object" && typeof execution.then === "function") {
      return execution.then(augmentResponse);
    }
    return execution;
  };
}
