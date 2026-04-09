import * as birpc from 'birpc';
import { EventOptions, BirpcOptions } from 'birpc';
import { WebSocketServer } from 'vite';
import { ViteHotContext } from 'vite-hot-client';

declare function createRPCServer<ClientFunction extends object, ServerFunctions extends object>(name: string, ws: WebSocketServer, functions: ServerFunctions, options?: EventOptions<ClientFunction>): birpc.BirpcGroupReturn<ClientFunction>;
declare function createRPCClient<ServerFunctions extends object, ClientFunctions extends object>(name: string, hot: ViteHotContext | undefined | Promise<ViteHotContext | undefined>, functions?: ClientFunctions, options?: Omit<BirpcOptions<ServerFunctions>, 'on' | 'post'>): birpc.BirpcReturn<ServerFunctions, ClientFunctions>;

export { createRPCClient, createRPCServer };
