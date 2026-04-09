import process from 'node:process';

const isInSsh = Boolean(process.env.SSH_CONNECTION
	|| process.env.SSH_CLIENT
	|| process.env.SSH_TTY);

export default isInSsh;
