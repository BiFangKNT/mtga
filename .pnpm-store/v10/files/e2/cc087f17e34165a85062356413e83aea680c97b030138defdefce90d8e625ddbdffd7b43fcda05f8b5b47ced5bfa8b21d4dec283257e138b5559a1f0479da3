import mysql from "mysql2/promise";
import { BoundableStatement } from "./_internal/statement.mjs";
import { getHyperdrive } from "./_internal/cloudflare.mjs";
export default function cloudflareHyperdriveMysqlConnector(opts) {
	let _connection;
	const getConnection = async () => {
		if (_connection) {
			return _connection;
		}
		const hyperdrive = await getHyperdrive(opts.bindingName);
		_connection = await mysql.createConnection({
			...opts,
			host: hyperdrive.host,
			user: hyperdrive.user,
			password: hyperdrive.password,
			database: hyperdrive.database,
			port: hyperdrive.port,
			disableEval: true
		});
		return _connection;
	};
	const query = (sql, params) => getConnection().then((c) => c.query(sql, params)).then((res) => res[0]);
	return {
		name: "cloudflare-hyperdrive-mysql",
		dialect: "mysql",
		getInstance: () => getConnection(),
		exec: (sql) => query(sql),
		prepare: (sql) => new StatementWrapper(sql, query),
		dispose: async () => {
			await _connection?.end?.();
			_connection = undefined;
		}
	};
}
class StatementWrapper extends BoundableStatement {
	#query;
	#sql;
	constructor(sql, query) {
		super();
		this.#sql = sql;
		this.#query = query;
	}
	async all(...params) {
		const res = await this.#query(this.#sql, params);
		return res;
	}
	async run(...params) {
		const res = await this.#query(this.#sql, params);
		return {
			success: true,
			...res
		};
	}
	async get(...params) {
		const res = await this.#query(this.#sql, params);
		return res[0];
	}
}
