/**
Check if the current environment is Windows Subsystem for Linux (WSL).
*/
export const isWsl: boolean;

/**
Get the PowerShell executable path in WSL environment.
*/
export function powerShellPathFromWsl(): Promise<string>;

/**
Get the PowerShell executable path for the current environment.

Returns WSL path if in WSL, otherwise returns Windows path.
*/
export function powerShellPath(): Promise<string>;

/**
Check if PowerShell is accessible in the current environment.

This is useful to determine whether Windows integration features can be used. In sandboxed WSL environments or systems where PowerShell is not accessible, this will return `false`.

@returns A promise that resolves to `true` if PowerShell is accessible, `false` otherwise.

@example
```
import {canAccessPowerShell} from 'wsl-utils';

if (await canAccessPowerShell()) {
	// Use Windows integration features
	console.log('PowerShell is accessible');
} else {
	// Fall back to Linux-native behavior
	console.log('PowerShell is not accessible');
}
```
*/
export function canAccessPowerShell(): Promise<boolean>;

/**
Get the default browser in WSL.

@returns A promise that resolves to the [ProgID](https://setuserfta.com/guide-to-understanding-progids-and-file-type-associations/) of the default browser (e.g., `'ChromeHTML'`, `'FirefoxURL'`).

@example
```
import {wslDefaultBrowser} from 'wsl-utils';

const progId = await wslDefaultBrowser();
//=> 'ChromeHTML'
```
*/
export function wslDefaultBrowser(): Promise<string>;

/**
Get the mount point for fixed drives in WSL.
*/
export function wslDrivesMountPoint(): Promise<string>;

/**
Convert a WSL Linux path to a Windows-accessible path.

URLs (strings starting with a protocol like `https://`) are returned unchanged.

@param path - The WSL path to convert (e.g., `/home/user/file.html`).
@returns The Windows-accessible path (e.g., `\\wsl.localhost\Ubuntu\home\user\file.html`) or the original path if conversion fails.

@example
```
import {convertWslPathToWindows} from 'wsl-utils';

// Convert a Linux path
const windowsPath = await convertWslPathToWindows('/home/user/file.html');
//=> '\\wsl.localhost\Ubuntu\home\user\file.html'

// URLs are not converted
const url = await convertWslPathToWindows('https://example.com');
//=> 'https://example.com'
```
*/
export function convertWslPathToWindows(path: string): Promise<string>;
