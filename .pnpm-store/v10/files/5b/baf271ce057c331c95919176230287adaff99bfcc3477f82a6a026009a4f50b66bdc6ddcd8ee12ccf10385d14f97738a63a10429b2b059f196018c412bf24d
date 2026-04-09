# is-in-ssh

> Check if the process is running in an SSH session

Useful for determining if your Node.js process is being executed over SSH, which can affect how you handle operations like opening files, browsers, or using system-specific commands.

## Install

```sh
npm install is-in-ssh
```

## Usage

```js
import isInSsh from 'is-in-ssh';

if (isInSsh) {
	console.log('Running in an SSH session');
}
```

## How it works

The package detects SSH sessions by checking for the presence of standard SSH environment variables:

- `SSH_CONNECTION`
- `SSH_CLIENT`
- `SSH_TTY`

These variables are automatically set by SSH servers when establishing a connection.

## Limitations

- The detection relies on environment variables, which could theoretically be spoofed or cleared
- May return `true` for `ssh localhost` connections (which are technically SSH sessions)
- Environment variables might not be inherited by all child processes or after privilege escalation (e.g., `sudo`)

## Related

- [is-wsl](https://github.com/sindresorhus/is-wsl) - Check if the process is running inside Windows Subsystem for Linux
- [is-docker](https://github.com/sindresorhus/is-docker) - Check if the process is running inside a Docker container
- [is-inside-container](https://github.com/sindresorhus/is-inside-container) - Check if the process is running inside a container
