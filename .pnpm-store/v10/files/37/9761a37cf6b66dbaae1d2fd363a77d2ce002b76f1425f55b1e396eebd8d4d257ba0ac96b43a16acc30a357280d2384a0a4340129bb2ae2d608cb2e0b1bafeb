//#region src/template.ts
function sqlTemplate(strings, ...values) {
	if (!isTemplateStringsArray(strings) || !Array.isArray(values)) throw new Error("[db0] invalid template invocation");
	const staticIndexes = [];
	let result = strings[0] || "";
	for (let i = 1; i < strings.length; i++) {
		if (result.endsWith("{") && strings[i].startsWith("}")) {
			result = result.slice(0, -1) + values[i - 1] + strings[i].slice(1);
			staticIndexes.push(i - 1);
			continue;
		}
		result += `?${strings[i] ?? ""}`;
	}
	const dynamicValues = values.filter((_, i) => !staticIndexes.includes(i));
	return [result.trim(), dynamicValues];
}
function isTemplateStringsArray(strings) {
	return Array.isArray(strings) && "raw" in strings && Array.isArray(strings.raw);
}

//#endregion
//#region src/database.ts
const SQL_SELECT_RE = /^select/i;
const SQL_RETURNING_RE = /[\s]returning[\s]/i;
const DIALECTS_WITH_RET = new Set(["postgresql", "sqlite"]);
const DISPOSED_ERR = "This database instance has been disposed and cannot be used.";
/**
* Creates and returns a database interface using the specified connector.
* This interface allows you to execute raw SQL queries, prepare SQL statements,
* and execute SQL queries with parameters using tagged template literals.
*
* @param {Connector} connector - The database connector used to execute and prepare SQL statements. See {@link Connector}.
* @returns {Database} The database interface that allows SQL operations. See {@link Database}.
*/
function createDatabase(connector) {
	let _disposed = false;
	const checkDisposed = () => {
		if (_disposed) {
			const err = new Error(DISPOSED_ERR);
			Error.captureStackTrace?.(err, checkDisposed);
			throw err;
		}
	};
	return {
		get dialect() {
			return connector.dialect;
		},
		get disposed() {
			return _disposed;
		},
		getInstance() {
			checkDisposed();
			return connector.getInstance();
		},
		exec: (sql) => {
			checkDisposed();
			return Promise.resolve(connector.exec(sql));
		},
		prepare: (sql) => {
			checkDisposed();
			return connector.prepare(sql);
		},
		sql: async (strings, ...values) => {
			checkDisposed();
			const [sql, params] = sqlTemplate(strings, ...values);
			if (SQL_SELECT_RE.test(sql) || DIALECTS_WITH_RET.has(connector.dialect) && SQL_RETURNING_RE.test(sql)) {
				const rows = await connector.prepare(sql).all(...params);
				return {
					rows,
					success: true
				};
			} else {
				const res = await connector.prepare(sql).run(...params);
				return res;
			}
		},
		dispose: () => {
			if (_disposed) return Promise.resolve();
			_disposed = true;
			try {
				return Promise.resolve(connector.dispose?.());
			} catch (error) {
				return Promise.reject(error);
			}
		},
		[Symbol.asyncDispose]() {
			return this.dispose();
		}
	};
}

//#endregion
//#region src/_connectors.ts
const connectors = Object.freeze({
	"better-sqlite3": "db0/connectors/better-sqlite3",
	"bun-sqlite": "db0/connectors/bun-sqlite",
	"bun": "db0/connectors/bun-sqlite",
	"cloudflare-d1": "db0/connectors/cloudflare-d1",
	"cloudflare-hyperdrive-mysql": "db0/connectors/cloudflare-hyperdrive-mysql",
	"cloudflare-hyperdrive-postgresql": "db0/connectors/cloudflare-hyperdrive-postgresql",
	"libsql-core": "db0/connectors/libsql/core",
	"libsql-http": "db0/connectors/libsql/http",
	"libsql-node": "db0/connectors/libsql/node",
	"libsql": "db0/connectors/libsql/node",
	"libsql-web": "db0/connectors/libsql/web",
	"mysql2": "db0/connectors/mysql2",
	"node-sqlite": "db0/connectors/node-sqlite",
	"sqlite": "db0/connectors/node-sqlite",
	"pglite": "db0/connectors/pglite",
	"planetscale": "db0/connectors/planetscale",
	"postgresql": "db0/connectors/postgresql",
	"sqlite3": "db0/connectors/sqlite3"
});

//#endregion
export { connectors, createDatabase };