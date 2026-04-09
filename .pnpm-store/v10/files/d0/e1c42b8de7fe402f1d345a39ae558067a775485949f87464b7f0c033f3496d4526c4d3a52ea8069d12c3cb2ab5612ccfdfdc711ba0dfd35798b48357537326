import { getTableName, is, Column, SQL } from "drizzle-orm";
// Source: https://github.com/drizzle-team/drizzle-orm/blob/main/drizzle-orm/src/utils.ts#L14
/** @internal */
export function mapResultRow(columns, row, joinsNotNullableMap) {
	// Key -> nested object key, value -> table name if all fields in the nested object are from the same table, false otherwise
	const nullifyMap = {};
	// eslint-disable-next-line unicorn/no-array-reduce
	const result = columns.reduce((result, { path, field }, columnIndex) => {
		let decoder;
		if (is(field, Column)) {
			decoder = field;
		} else if (is(field, SQL)) {
			decoder = "decoder" in field && field.decoder;
		} else {
			decoder = "decoder" in field.sql && field.sql.decoder;
		}
		let node = result;
		for (const [pathChunkIndex, pathChunk] of path.entries()) {
			if (pathChunkIndex < path.length - 1) {
				if (!(pathChunk in node)) {
					node[pathChunk] = {};
				}
				node = node[pathChunk];
			} else {
				const rawValue = row[columnIndex];
				const value = node[pathChunk] = rawValue === null ? null : decoder.mapFromDriverValue(rawValue);
				if (joinsNotNullableMap && is(field, Column) && path.length === 2) {
					const objectName = path[0];
					if (!(objectName in nullifyMap)) {
						nullifyMap[objectName] = value === null ? getTableName(field.table) : false;
					} else if (typeof nullifyMap[objectName] === "string" && nullifyMap[objectName] !== getTableName(field.table)) {
						nullifyMap[objectName] = false;
					}
				}
			}
		}
		return result;
	}, {});
	// Nullify all nested objects from nullifyMap that are nullable
	if (joinsNotNullableMap && Object.keys(nullifyMap).length > 0) {
		for (const [objectName, tableName] of Object.entries(nullifyMap)) {
			if (typeof tableName === "string" && !joinsNotNullableMap[tableName]) {
				result[objectName] = null;
			}
		}
	}
	return result;
}
