import { NoopLogger } from "drizzle-orm";
import { SQLiteSession, SQLitePreparedQuery } from "drizzle-orm/sqlite-core";
export class DB0Session extends SQLiteSession {
	dialect;
	logger;
	constructor(db, dialect, schema, options = {}) {
		super(dialect);
		this.db = db;
		this.schema = schema;
		this.options = options;
		this.logger = options.logger ?? new NoopLogger();
	}
	// @ts-expect-error TODO
	prepareQuery(query, fields, executeMethod, customResultMapper) {
		const stmt = this.db.prepare(query.sql);
		return new DB0PreparedQuery(stmt, query, this.logger, fields, executeMethod, customResultMapper);
	}
	// TODO: Implement batch
	// TODO: Implement transaction
	transaction(transaction, config) {
		throw new Error("transaction is not implemented!");
		//   const tx = new D1Transaction('async', this.dialect, this, this.schema);
		//   await this.run(sql.raw(`begin${config?.behavior ? ' ' + config.behavior : ''}`));
		//   try {
		//     const result = await transaction(tx);
		//     await this.run(sql`commit`);
		//     return result;
		//   } catch (err) {
		//     await this.run(sql`rollback`);
		//     throw err;
		//   }
	}
}
export class DB0PreparedQuery extends SQLitePreparedQuery {
	constructor(stmt, query, logger, fields, executeMethod, customResultMapper) {
		super("async", executeMethod, query);
		this.stmt = stmt;
		this.logger = logger;
	}
	run() {
		return this.stmt.run(...this.query.params);
	}
	all() {
		return this.stmt.all(...this.query.params);
	}
	get() {
		return this.stmt.get(...this.query.params);
	}
	values() {
		return Promise.reject(new Error("values is not implemented!"));
	}
}
// Object.defineProperty(DB0PreparedQuery, entityKind, {
//   value: "DB0PreparedQuery",
//   enumerable: true,
//   configurable: true,
// });
