import { FetchHandler, ServerOptions } from "../types.mjs";
import * as AWS from "aws-lambda";

//#region src/adapters/_aws/utils.d.ts
type AWSLambdaResponseStream = NodeJS.WritableStream & {
  setContentType(contentType: string): void;
};
//#endregion
//#region src/adapters/aws-lambda.d.ts
type MaybePromise<T> = T | Promise<T>;
type AwsLambdaEvent = AWS.APIGatewayProxyEvent | AWS.APIGatewayProxyEventV2;
type AWSLambdaHandler = (event: AwsLambdaEvent, context: AWS.Context) => MaybePromise<AWS.APIGatewayProxyResult | AWS.APIGatewayProxyResultV2>;
type AWSLambdaStreamingHandler = (event: AwsLambdaEvent, responseStream: AWSLambdaResponseStream, context: AWS.Context) => MaybePromise<void>;
declare function toLambdaHandler(options: ServerOptions): AWSLambdaHandler;
declare function handleLambdaEvent(fetchHandler: FetchHandler, event: AwsLambdaEvent, context: AWS.Context): Promise<AWS.APIGatewayProxyResult | AWS.APIGatewayProxyResultV2>;
declare function handleLambdaEventWithStream(fetchHandler: FetchHandler, event: AwsLambdaEvent, responseStream: AWSLambdaResponseStream, context: AWS.Context): Promise<void>;
declare function invokeLambdaHandler(handler: AWSLambdaHandler, request: Request): Promise<Response>;
//#endregion
export { AWSLambdaHandler, type AWSLambdaResponseStream, AWSLambdaStreamingHandler, AwsLambdaEvent, handleLambdaEvent, handleLambdaEventWithStream, invokeLambdaHandler, toLambdaHandler };