import {promisify} from 'node:util';
import childProcess from 'node:child_process';
import fs, {constants as fsConstants} from 'node:fs/promises';
import isWsl from 'is-wsl';
import {powerShellPath as windowsPowerShellPath, executePowerShell} from 'powershell-utils';
import {parseMountPointFromConfig} from './utilities.js';

const execFile = promisify(childProcess.execFile);

export const wslDrivesMountPoint = (() => {
	// Default value for "root" param
	// according to https://docs.microsoft.com/en-us/windows/wsl/wsl-config
	const defaultMountPoint = '/mnt/';

	let mountPoint;

	return async function () {
		if (mountPoint) {
			// Return memoized mount point value
			return mountPoint;
		}

		const configFilePath = '/etc/wsl.conf';

		let isConfigFileExists = false;
		try {
			await fs.access(configFilePath, fsConstants.F_OK);
			isConfigFileExists = true;
		} catch {}

		if (!isConfigFileExists) {
			return defaultMountPoint;
		}

		const configContent = await fs.readFile(configFilePath, {encoding: 'utf8'});
		const parsedMountPoint = parseMountPointFromConfig(configContent);

		if (parsedMountPoint === undefined) {
			return defaultMountPoint;
		}

		mountPoint = parsedMountPoint;
		mountPoint = mountPoint.endsWith('/') ? mountPoint : `${mountPoint}/`;

		return mountPoint;
	};
})();

export const powerShellPathFromWsl = async () => {
	const mountPoint = await wslDrivesMountPoint();
	return `${mountPoint}c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`;
};

export const powerShellPath = isWsl ? powerShellPathFromWsl : windowsPowerShellPath;

// Cache for PowerShell accessibility check
let canAccessPowerShellPromise;

export const canAccessPowerShell = async () => {
	canAccessPowerShellPromise ??= (async () => {
		try {
			const psPath = await powerShellPath();
			await fs.access(psPath, fsConstants.X_OK);
			return true;
		} catch {
			// PowerShell is not accessible (either doesn't exist, no execute permission, or other error)
			return false;
		}
	})();

	return canAccessPowerShellPromise;
};

export const wslDefaultBrowser = async () => {
	const psPath = await powerShellPath();
	const command = String.raw`(Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice").ProgId`;

	const {stdout} = await executePowerShell(command, {powerShellPath: psPath});

	return stdout.trim();
};

export const convertWslPathToWindows = async path => {
	// Don't convert URLs
	if (/^[a-z]+:\/\//i.test(path)) {
		return path;
	}

	try {
		const {stdout} = await execFile('wslpath', ['-aw', path], {encoding: 'utf8'});
		return stdout.trim();
	} catch {
		// If wslpath fails, return the original path
		return path;
	}
};

export {default as isWsl} from 'is-wsl';
