import mysql from "mysql2/promise";
import type { Connector } from "db0";
type OmitMysqlConfig = Omit<mysql.ConnectionOptions, "user" | "database" | "password" | "password1" | "password2" | "password3" | "port" | "host" | "uri" | "localAddress" | "socketPath" | "insecureAuth" | "passwordSha1" | "disableEval">;
export type ConnectorOptions = {
	bindingName: string;
} & OmitMysqlConfig;
export default function cloudflareHyperdriveMysqlConnector(opts: ConnectorOptions): Connector<mysql.Connection>;
