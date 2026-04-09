import path from 'node:path';
import fs from 'node:fs';
import {locatePath, locatePathSync} from 'locate-path';
import {toPath} from 'unicorn-magic';

export const findUpStop = Symbol('findUpStop');

export async function findUpMultiple(name, options = {}) {
	let directory = path.resolve(toPath(options.cwd) ?? '');
	const {root} = path.parse(directory);
	const stopAt = path.resolve(directory, toPath(options.stopAt) ?? root);
	const limit = options.limit ?? Number.POSITIVE_INFINITY;
	const paths = [name].flat();

	const runMatcher = async locateOptions => {
		if (typeof name !== 'function') {
			return locatePath(paths, locateOptions);
		}

		const foundPath = await name(locateOptions.cwd);
		if (typeof foundPath === 'string') {
			return locatePath([foundPath], locateOptions);
		}

		return foundPath;
	};

	const matches = [];
	while (true) {
		// eslint-disable-next-line no-await-in-loop
		const foundPath = await runMatcher({...options, cwd: directory});

		if (foundPath === findUpStop) {
			break;
		}

		if (foundPath) {
			matches.push(path.resolve(directory, foundPath));
		}

		if (directory === stopAt || matches.length >= limit) {
			break;
		}

		directory = path.dirname(directory);
	}

	return matches;
}

export function findUpMultipleSync(name, options = {}) {
	let directory = path.resolve(toPath(options.cwd) ?? '');
	const {root} = path.parse(directory);
	const stopAt = path.resolve(directory, toPath(options.stopAt) ?? root);
	const limit = options.limit ?? Number.POSITIVE_INFINITY;
	const paths = [name].flat();

	const runMatcher = locateOptions => {
		if (typeof name !== 'function') {
			return locatePathSync(paths, locateOptions);
		}

		const foundPath = name(locateOptions.cwd);
		if (typeof foundPath === 'string') {
			return locatePathSync([foundPath], locateOptions);
		}

		return foundPath;
	};

	const matches = [];
	while (true) {
		const foundPath = runMatcher({...options, cwd: directory});

		if (foundPath === findUpStop) {
			break;
		}

		if (foundPath) {
			matches.push(path.resolve(directory, foundPath));
		}

		if (directory === stopAt || matches.length >= limit) {
			break;
		}

		directory = path.dirname(directory);
	}

	return matches;
}

export async function findUp(name, options = {}) {
	const matches = await findUpMultiple(name, {...options, limit: 1});
	return matches[0];
}

export function findUpSync(name, options = {}) {
	const matches = findUpMultipleSync(name, {...options, limit: 1});
	return matches[0];
}

async function findDownDepthFirst(directory, paths, maxDepth, locateOptions, currentDepth = 0) {
	const found = await locatePath(paths, {cwd: directory, ...locateOptions});
	if (found) {
		return path.resolve(directory, found);
	}

	if (currentDepth >= maxDepth) {
		return undefined;
	}

	try {
		const entries = await fs.promises.readdir(directory, {withFileTypes: true});
		for (const entry of entries) {
			if (entry.isDirectory()) {
				// eslint-disable-next-line no-await-in-loop
				const result = await findDownDepthFirst(
					path.join(directory, entry.name),
					paths,
					maxDepth,
					locateOptions,
					currentDepth + 1,
				);
				if (result) {
					return result;
				}
			}
		}
	} catch {}

	return undefined;
}

function findDownDepthFirstSync(directory, paths, maxDepth, locateOptions, currentDepth = 0) {
	const found = locatePathSync(paths, {cwd: directory, ...locateOptions});
	if (found) {
		return path.resolve(directory, found);
	}

	if (currentDepth >= maxDepth) {
		return undefined;
	}

	try {
		const entries = fs.readdirSync(directory, {withFileTypes: true});
		for (const entry of entries) {
			if (entry.isDirectory()) {
				const result = findDownDepthFirstSync(
					path.join(directory, entry.name),
					paths,
					maxDepth,
					locateOptions,
					currentDepth + 1,
				);
				if (result) {
					return result;
				}
			}
		}
	} catch {}

	return undefined;
}

function prepareFindDownOptions(name, options) {
	const startDirectory = path.resolve(toPath(options.cwd) ?? '');
	const maxDepth = Math.max(0, options.depth ?? 1);
	const paths = [name].flat();
	const {type = 'file', allowSymlinks = true, strategy = 'breadth'} = options;
	const locateOptions = {type, allowSymlinks};
	return {
		startDirectory,
		maxDepth,
		paths,
		locateOptions,
		strategy,
	};
}

async function findDownBreadthFirst(startDirectory, paths, maxDepth, locateOptions) {
	const queue = [{directory: startDirectory, depth: 0}];

	while (queue.length > 0) {
		const {directory, depth} = queue.shift();

		// eslint-disable-next-line no-await-in-loop
		const found = await locatePath(paths, {cwd: directory, ...locateOptions});
		if (found) {
			return path.resolve(directory, found);
		}

		if (depth >= maxDepth) {
			continue;
		}

		try {
			// eslint-disable-next-line no-await-in-loop
			const entries = await fs.promises.readdir(directory, {withFileTypes: true});
			for (const entry of entries) {
				if (entry.isDirectory()) {
					queue.push({directory: path.join(directory, entry.name), depth: depth + 1});
				}
			}
		} catch {}
	}

	return undefined;
}

function findDownBreadthFirstSync(startDirectory, paths, maxDepth, locateOptions) {
	const queue = [{directory: startDirectory, depth: 0}];

	while (queue.length > 0) {
		const {directory, depth} = queue.shift();

		const found = locatePathSync(paths, {cwd: directory, ...locateOptions});
		if (found) {
			return path.resolve(directory, found);
		}

		if (depth >= maxDepth) {
			continue;
		}

		try {
			const entries = fs.readdirSync(directory, {withFileTypes: true});
			for (const entry of entries) {
				if (entry.isDirectory()) {
					queue.push({directory: path.join(directory, entry.name), depth: depth + 1});
				}
			}
		} catch {}
	}

	return undefined;
}

export async function findDown(name, options = {}) {
	const {startDirectory, maxDepth, paths, locateOptions, strategy} = prepareFindDownOptions(name, options);

	return strategy === 'depth'
		? findDownDepthFirst(startDirectory, paths, maxDepth, locateOptions)
		: findDownBreadthFirst(startDirectory, paths, maxDepth, locateOptions);
}

export function findDownSync(name, options = {}) {
	const {startDirectory, maxDepth, paths, locateOptions, strategy} = prepareFindDownOptions(name, options);

	return strategy === 'depth'
		? findDownDepthFirstSync(startDirectory, paths, maxDepth, locateOptions)
		: findDownBreadthFirstSync(startDirectory, paths, maxDepth, locateOptions);
}

