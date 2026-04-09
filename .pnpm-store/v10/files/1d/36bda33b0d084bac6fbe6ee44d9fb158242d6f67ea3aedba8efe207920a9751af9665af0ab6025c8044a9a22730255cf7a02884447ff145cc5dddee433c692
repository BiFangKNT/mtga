# wsl-utils

> Utilities for working with [Windows Subsystem for Linux (WSL)](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux)

## Install

```sh
npm install wsl-utils
```

## Usage

```js
import {isWsl, powerShellPathFromWsl} from 'wsl-utils';

// Check if running in WSL
console.log('Is WSL:', isWsl);

// Get PowerShell path from WSL
console.log('PowerShell path:', await powerShellPathFromWsl());
//=> '/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'
```

## API

### isWsl

Type: `boolean`

Check if the current environment is Windows Subsystem for Linux (WSL).

### powerShellPathFromWsl()

Returns: `Promise<string>`

Get the PowerShell executable path in WSL environment.

### powerShellPath()

Returns: `Promise<string>`

Get the PowerShell executable path for the current environment.

Returns WSL path if in WSL, otherwise returns Windows path.

### canAccessPowerShell()

Returns: `Promise<boolean>`

Check if PowerShell is accessible in the current environment.

This is useful to determine whether Windows integration features can be used. In sandboxed WSL environments or systems where PowerShell is not accessible, this will return `false`.

```js
import {canAccessPowerShell} from 'wsl-utils';

if (await canAccessPowerShell()) {
	// Use Windows integration features
	console.log('PowerShell is accessible');
} else {
	// Fall back to Linux-native behavior
	console.log('PowerShell is not accessible');
}
```

### wslDefaultBrowser()

Returns: `Promise<string>`

Get the default browser in WSL.

Returns a promise that resolves to the [ProgID](https://setuserfta.com/guide-to-understanding-progids-and-file-type-associations/) of the default browser (e.g., `'ChromeHTML'`, `'FirefoxURL'`).

```js
import {wslDefaultBrowser} from 'wsl-utils';

const progId = await wslDefaultBrowser();
//=> 'ChromeHTML'
```

### wslDrivesMountPoint()

Returns: `Promise<string>`

Get the mount point for fixed drives in WSL.

### convertWslPathToWindows(path)

Returns: `Promise<string>`

Convert a WSL Linux path to a Windows-accessible path.

URLs (strings starting with a protocol like `https://`) are returned unchanged.

```js
import {convertWslPathToWindows} from 'wsl-utils';

// Convert a Linux path
const windowsPath = await convertWslPathToWindows('/home/user/file.html');
//=> '\\wsl.localhost\Ubuntu\home\user\file.html'

// URLs are not converted
const url = await convertWslPathToWindows('https://example.com');
//=> 'https://example.com'
```

#### path

Type: `string`

The WSL path to convert (e.g., `/home/user/file.html`).
