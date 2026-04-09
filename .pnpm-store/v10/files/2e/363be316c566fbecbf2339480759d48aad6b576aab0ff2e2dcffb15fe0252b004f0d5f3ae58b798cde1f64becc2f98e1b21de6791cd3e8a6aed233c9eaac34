import { resolve, dirname } from "node:path";
import { mkdirSync } from "node:fs";
import sqlite3 from "sqlite3";
import { BoundableStatement } from "./_internal/statement.mjs";
export default function nodeSqlite3Connector(opts) {
	let _db;
	const _activeStatements = new Set();
	const getDB = () => {
		if (_db) {
			return _db;
		}
		if (opts.name === ":memory:") {
			_db = new sqlite3.Database(":memory:");
			return _db;
		}
		const filePath = resolve(opts.cwd || ".", opts.path || `.data/${opts.name || "db"}.sqlite3`);
		mkdirSync(dirname(filePath), { recursive: true });
		_db = new sqlite3.Database(filePath);
		return _db;
	};
	const query = (sql) => new Promise((resolve, reject) => {
		getDB().exec(sql, (err) => {
			if (err) {
				return reject(err);
			}
			resolve({ success: true });
		});
	});
	return {
		name: "sqlite3",
		dialect: "sqlite",
		getInstance: () => getDB(),
		exec: (sql) => query(sql),
		prepare: (sql) => {
			const stmt = new StatementWrapper(sql, getDB());
			_activeStatements.add(stmt);
			return stmt;
		},
		dispose: async () => {
			await Promise.all([..._activeStatements].map((s) => s.finalize().catch((error) => {
				console.warn("[db0] [sqlite3] failed to finalize statement", error);
			})));
			_activeStatements.clear();
			await new Promise((resolve, reject) => _db?.close?.((error) => error ? reject(error) : resolve()));
			_db = undefined;
		}
	};
}
class StatementWrapper extends BoundableStatement {
	#onError;
	constructor(sql, db) {
		super(db.prepare(sql, (err) => {
			if (err && this.#onError) {
				return this.#onError(err);
			}
		}));
	}
	async all(...params) {
		const rows = await new Promise((resolve, reject) => {
			this.#onError = reject;
			this._statement.all(...params, (err, rows) => err ? reject(err) : resolve(rows));
		});
		return rows;
	}
	async run(...params) {
		await new Promise((resolve, reject) => {
			this.#onError = reject;
			this._statement.run(...params, (err) => err ? reject(err) : resolve());
		});
		return { success: true };
	}
	async get(...params) {
		const row = await new Promise((resolve, reject) => {
			this.#onError = reject;
			this._statement.get(...params, (err, row) => err ? reject(err) : resolve(row));
		});
		return row;
	}
	finalize() {
		try {
			// TODO: Can we await on finalize cb?
			this._statement.finalize();
			return Promise.resolve();
		} catch (error) {
			return Promise.reject(error);
		}
	}
}
