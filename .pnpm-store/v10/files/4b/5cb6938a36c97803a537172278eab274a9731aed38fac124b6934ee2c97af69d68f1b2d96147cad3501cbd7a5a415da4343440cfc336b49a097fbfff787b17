import "better-sqlite3";
import "bun:sqlite";
import mysql from "mysql2/promise";
import pg from "pg";
import { Client, Config } from "@libsql/client";
import "node:sqlite";
import { PGliteOptions } from "@electric-sql/pglite";
import { Config as Config$1 } from "@planetscale/database";
import "sqlite3";

//#region src/types.d.ts
/**
* Represents primitive types that can be used in SQL operations.
*/
type Primitive = string | number | boolean | undefined | null;
type SQLDialect = "mysql" | "postgresql" | "sqlite" | "libsql";
type Statement = {
  /**
  * Binds parameters to the statement.
  * @param {...Primitive[]} params - Parameters to bind to the SQL statement.
  * @returns {PreparedStatement} The instance of the statement with bound parameters.
  */
  bind(...params: Primitive[]): PreparedStatement;
  /**
  * Executes the statement and returns all resulting rows as an array.
  * @param {...Primitive[]} params - Parameters to bind to the SQL statement.
  * @returns {Promise<unknown[]>} A promise that resolves to an array of rows.
  */
  all(...params: Primitive[]): Promise<unknown[]>;
  /**
  * Executes the statement as an action (e.g. insert, update, delete).
  * @param {...Primitive[]} params - Parameters to bind to the SQL statement.
  * @returns {Promise<{ success: boolean }>} A promise that resolves to the success state of the action.
  */
  run(...params: Primitive[]): Promise<{
    success: boolean;
  }>;
  /**
  * Executes the statement and returns a single row.
  * @param {...Primitive[]} params - Parameters to bind to the SQL statement.
  * @returns {Promise<unknown>} A promise that resolves to the first row in the result set.
  */
  get(...params: Primitive[]): Promise<unknown>;
};
type PreparedStatement = {
  /**
  * Binds parameters to the statement.
  * @param {...Primitive[]} params - Parameters to bind to the SQL statement.
  * @returns {PreparedStatement} The instance of the statement with bound parameters.
  */
  bind(...params: Primitive[]): PreparedStatement;
  /**
  * Executes the statement and returns all resulting rows as an array.
  * @returns {Promise<unknown[]>} A promise that resolves to an array of rows.
  */
  all(): Promise<unknown[]>;
  /**
  * Executes the statement as an action (e.g. insert, update, delete).
  * @returns {Promise<{ success: boolean }>} A promise that resolves to the success state of the action.
  */
  run(): Promise<{
    success: boolean;
  }>;
  /**
  * Executes the statement and returns a single row.
  * @returns {Promise<unknown>} A promise that resolves to the first row in the result set.
  */
  get(): Promise<unknown>;
};
/**
* Represents the result of a database execution.
*/
type ExecResult = unknown;
/**
* Defines a database connector for executing SQL queries and preparing statements.
*/
type Connector<TInstance = unknown> = {
  /**
  * The name of the connector.
  */
  name: string;
  /**
  * The SQL dialect used by the connector.
  */
  dialect: SQLDialect;
  /**
  * The client instance used internally.
  */
  getInstance: () => TInstance | Promise<TInstance>;
  /**
  * Executes an SQL query directly and returns the result.
  * @param {string} sql - The SQL string to execute.
  * @returns {ExecResult | Promise<ExecResult>} The result of the execution.
  */
  exec: (sql: string) => ExecResult | Promise<ExecResult>;
  /**
  * Prepares an SQL statement for execution.
  * @param {string} sql - The SQL string to prepare.
  * @returns {statement} The prepared SQL statement.
  */
  prepare: (sql: string) => Statement;
  /**
  * Closes the database connection and cleans up resources.
  * @returns {void | Promise<void>} A promise that resolves when the connection is closed.
  */
  dispose?: () => void | Promise<void>;
};
/**
* Represents default SQL results, including any error messages, row changes and rows returned.
*/
type DefaultSQLResult = {
  lastInsertRowid?: number;
  changes?: number;
  error?: string;
  rows?: {
    id?: string | number;
    [key: string]: unknown;
  }[];
  success?: boolean;
};
interface Database<TConnector extends Connector = Connector> extends AsyncDisposable {
  readonly dialect: SQLDialect;
  /**
  * Indicates whether the database instance has been disposed/closed.
  * @returns {boolean} True if the database has been disposed, false otherwise.
  */
  readonly disposed: boolean;
  /**
  * The client instance used internally.
  * @returns {Promise<TInstance>} A promise that resolves with the client instance.
  */
  getInstance: () => Promise<Awaited<ReturnType<TConnector["getInstance"]>>>;
  /**
  * Executes a raw SQL string.
  * @param {string} sql - The SQL string to execute.
  * @returns {Promise<ExecResult>} A promise that resolves with the execution result.
  */
  exec: (sql: string) => Promise<ExecResult>;
  /**
  * Prepares an SQL statement from a raw SQL string.
  * @param {string} sql - The SQL string to prepare.
  * @returns {statement} The prepared SQL statement.
  */
  prepare: (sql: string) => Statement;
  /**
  * Executes SQL queries using tagged template literals.
  * @template T The expected type of query result.
  * @param {TemplateStringsArray} strings - The segments of the SQL string.
  * @param {...Primitive[]} values - The values to interpolate into the SQL string.
  * @returns {Promise<T>} A promise that resolves with the typed result of the query.
  */
  sql: <T = DefaultSQLResult>(strings: TemplateStringsArray, ...values: Primitive[]) => Promise<T>;
  /**
  * Closes the database connection and cleans up resources.
  * @returns {Promise<void>} A promise that resolves when the connection is closed.
  */
  dispose: () => Promise<void>;
  /**
  * AsyncDisposable implementation for using syntax support.
  * @returns {Promise<void>} A promise that resolves when the connection is disposed.
  */
  [Symbol.asyncDispose]: () => Promise<void>;
}
//#endregion
//#region src/database.d.ts
/**
* Creates and returns a database interface using the specified connector.
* This interface allows you to execute raw SQL queries, prepare SQL statements,
* and execute SQL queries with parameters using tagged template literals.
*
* @param {Connector} connector - The database connector used to execute and prepare SQL statements. See {@link Connector}.
* @returns {Database} The database interface that allows SQL operations. See {@link Database}.
*/
declare function createDatabase<TConnector extends Connector = Connector>(connector: TConnector): Database<TConnector>;
//#endregion
//#region src/connectors/better-sqlite3.d.ts
interface ConnectorOptions$15 {
  cwd?: string;
  path?: string;
  name?: string;
}
//#endregion
//#region src/connectors/bun-sqlite.d.ts
interface ConnectorOptions$14 {
  cwd?: string;
  path?: string;
  name?: string;
}
//#endregion
//#region src/connectors/cloudflare-d1.d.ts
interface ConnectorOptions$13 {
  bindingName?: string;
}
//#endregion
//#region src/connectors/cloudflare-hyperdrive-mysql.d.ts
type OmitMysqlConfig = Omit<mysql.ConnectionOptions, "user" | "database" | "password" | "password1" | "password2" | "password3" | "port" | "host" | "uri" | "localAddress" | "socketPath" | "insecureAuth" | "passwordSha1" | "disableEval">;
type ConnectorOptions$12 = {
  bindingName: string;
} & OmitMysqlConfig;
//#endregion
//#region src/connectors/cloudflare-hyperdrive-postgresql.d.ts
type OmitPgConfig = Omit<pg.ClientConfig, "user" | "database" | "password" | "port" | "host" | "connectionString">;
type ConnectorOptions$11 = {
  bindingName: string;
} & OmitPgConfig;
//#endregion
//#region src/connectors/libsql/core.d.ts
type ConnectorOptions$10 = {
  getClient: () => Client;
  name?: string;
};
//#endregion
//#region src/connectors/libsql/http.d.ts
type ConnectorOptions$9 = Config;
//#endregion
//#region src/connectors/libsql/node.d.ts
type ConnectorOptions$8 = Config;
//#endregion
//#region src/connectors/libsql/web.d.ts
type ConnectorOptions$7 = Config;
//#endregion
//#region src/connectors/mysql2.d.ts
type ConnectorOptions$6 = mysql.ConnectionOptions;
//#endregion
//#region src/connectors/node-sqlite.d.ts
interface ConnectorOptions$5 {
  cwd?: string;
  path?: string;
  name?: string;
}
//#endregion
//#region src/connectors/pglite.d.ts
type ConnectorOptions$4 = PGliteOptions;
//#endregion
//#region src/connectors/planetscale.d.ts
type ConnectorOptions$3 = Config$1;
//#endregion
//#region src/connectors/postgresql.d.ts
type ConnectorOptions$2 = {
  url: string;
} | pg.ClientConfig;
//#endregion
//#region src/connectors/sqlite3.d.ts
interface ConnectorOptions$1 {
  cwd?: string;
  path?: string;
  name?: string;
}
//#endregion
//#region src/_connectors.d.ts
type ConnectorName = "better-sqlite3" | "bun-sqlite" | "bun" | "cloudflare-d1" | "cloudflare-hyperdrive-mysql" | "cloudflare-hyperdrive-postgresql" | "libsql-core" | "libsql-http" | "libsql-node" | "libsql" | "libsql-web" | "mysql2" | "node-sqlite" | "sqlite" | "pglite" | "planetscale" | "postgresql" | "sqlite3";
type ConnectorOptions = {
  "better-sqlite3": ConnectorOptions$15;
  "bun-sqlite": ConnectorOptions$14;
  /** alias of bun-sqlite */
  "bun": ConnectorOptions$14;
  "cloudflare-d1": ConnectorOptions$13;
  "cloudflare-hyperdrive-mysql": ConnectorOptions$12;
  "cloudflare-hyperdrive-postgresql": ConnectorOptions$11;
  "libsql-core": ConnectorOptions$10;
  "libsql-http": ConnectorOptions$9;
  "libsql-node": ConnectorOptions$8;
  /** alias of libsql-node */
  "libsql": ConnectorOptions$8;
  "libsql-web": ConnectorOptions$7;
  "mysql2": ConnectorOptions$6;
  "node-sqlite": ConnectorOptions$5;
  /** alias of node-sqlite */
  "sqlite": ConnectorOptions$5;
  "pglite": ConnectorOptions$4;
  "planetscale": ConnectorOptions$3;
  "postgresql": ConnectorOptions$2;
  "sqlite3": ConnectorOptions$1;
};
declare const connectors: Record<ConnectorName, string>;
//#endregion
export { type Connector, type ConnectorName, type ConnectorOptions, type Database, type ExecResult, type PreparedStatement, type Primitive, type SQLDialect, type Statement, connectors, createDatabase };