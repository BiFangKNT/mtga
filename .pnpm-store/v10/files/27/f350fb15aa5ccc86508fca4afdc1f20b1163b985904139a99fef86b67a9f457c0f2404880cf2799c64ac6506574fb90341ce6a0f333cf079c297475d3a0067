![tab CLI autocompletions demo](assets/preview.gif)

# tab

Shell autocompletions are largely missing in the JavaScript CLI ecosystem. tab provides a simple API for adding autocompletions to any JavaScript CLI tool.

Additionally, tab supports autocompletions for `pnpm`, `npm`, `yarn`, and `bun`.

Modern CLI libraries like [Gunshi](https://github.com/kazupon/gunshi) include tab completion natively in their core.

As CLI tooling authors, if we can spare our users a second or two by not checking documentation or writing the `-h` flag, we're doing them a huge favor. The unconscious mind loves hitting the [TAB] key and always expects feedback. When nothing happens, it breaks the user's flow - a frustration apparent across the whole JavaScript CLI tooling ecosystem.

tab solves this complexity by providing autocompletions that work consistently across `zsh`, `bash`, `fish`, and `powershell`.

## Installation

### For Package Manager Completions

> **Note:** Global install is recommended

```bash
npm install -g @bomb.sh/tab
```

Then enable completions permanently:

```bash
# For zsh
echo 'source <(tab pnpm zsh)' >> ~/.zshrc
source ~/.zshrc

# For bash
echo 'source <(tab pnpm bash)' >> ~/.bashrc
source ~/.bashrc

# The same can be done for other shells!
```

### For CLI Library (Adding Completions to Your CLI)

```bash
npm install @bomb.sh/tab
# or
pnpm add @bomb.sh/tab
# or
yarn add @bomb.sh/tab
# or
bun add @bomb.sh/tab
```

## Quick Start

Add autocompletions to your CLI tool:

```typescript
import t from '@bomb.sh/tab';

// Define your CLI structure
const devCmd = t.command('dev', 'Start development server');
devCmd.option('port', 'Specify port', (complete) => {
  complete('3000', 'Development port');
  complete('8080', 'Production port');
});

// Handle completion requests
if (process.argv[2] === 'complete') {
  const shell = process.argv[3];
  if (shell === '--') {
    const args = process.argv.slice(4);
    t.parse(args);
  } else {
    t.setup('my-cli', 'node my-cli.js', shell);
  }
}
```

Test your completions:

```bash
node my-cli.js complete -- dev --port=<TAB>
# Output: --port=3000  Development port
#         --port=8080  Production port
```

Install for users:

```bash
# One-time setup
source <(my-cli complete zsh)

# Permanent setup
my-cli complete zsh > ~/.my-cli-completion.zsh
echo 'source ~/.my-cli-completion.zsh' >> ~/.zshrc
```

## Package Manager Completions

As mentioned earlier, tab provides completions for package managers as well:

```bash
# Generate and install completion scripts
tab pnpm zsh > ~/.pnpm-completion.zsh && echo 'source ~/.pnpm-completion.zsh' >> ~/.zshrc
tab npm bash > ~/.npm-completion.bash && echo 'source ~/.npm-completion.bash' >> ~/.bashrc
tab yarn fish > ~/.config/fish/completions/yarn.fish
tab bun powershell > ~/.bun-completion.ps1 && echo '. ~/.bun-completion.ps1' >> $PROFILE
```

Example in action:

```bash
pnpm install --reporter=<TAB>
# Shows: append-only, default, ndjson, silent

yarn add --emoji=<TAB>
# Shows: true, false
```

## Framework Adapters

tab provides adapters for popular JavaScript CLI frameworks.

### CAC Integration

```typescript
import cac from 'cac';
import tab from '@bomb.sh/tab/cac';

const cli = cac('my-cli');

// Define your CLI
cli
  .command('dev', 'Start dev server')
  .option('--port <port>', 'Specify port')
  .option('--host <host>', 'Specify host');

// Initialize tab completions
const completion = await tab(cli);

// Add custom completions for option values
const devCommand = completion.commands.get('dev');
const portOption = devCommand?.options.get('port');
if (portOption) {
  portOption.handler = (complete) => {
    complete('3000', 'Development port');
    complete('8080', 'Production port');
  };
}

cli.parse();
```

### Citty Integration

```typescript
import { defineCommand, createMain } from 'citty';
import tab from '@bomb.sh/tab/citty';

const main = defineCommand({
  meta: { name: 'my-cli', description: 'My CLI tool' },
  subCommands: {
    dev: defineCommand({
      meta: { name: 'dev', description: 'Start dev server' },
      args: {
        port: { type: 'string', description: 'Specify port' },
        host: { type: 'string', description: 'Specify host' },
      },
    }),
  },
});

// Initialize tab completions
const completion = await tab(main);

// Add custom completions
const devCommand = completion.commands.get('dev');
const portOption = devCommand?.options.get('port');
if (portOption) {
  portOption.handler = (complete) => {
    complete('3000', 'Development port');
    complete('8080', 'Production port');
  };
}

const cli = createMain(main);
cli();
```

### Commander.js Integration

```typescript
import { Command } from 'commander';
import tab from '@bomb.sh/tab/commander';

const program = new Command('my-cli');
program.version('1.0.0');

// Define commands
program
  .command('serve')
  .description('Start the server')
  .option('-p, --port <number>', 'port to use', '3000')
  .option('-H, --host <host>', 'host to use', 'localhost')
  .action((options) => {
    console.log('Starting server...');
  });

// Initialize tab completions
const completion = tab(program);

// Add custom completions
const serveCommand = completion.commands.get('serve');
const portOption = serveCommand?.options.get('port');
if (portOption) {
  portOption.handler = (complete) => {
    complete('3000', 'Default port');
    complete('8080', 'Alternative port');
  };
}

program.parse();
```

tab uses a standardized completion protocol that any CLI can implement:

```bash
# Generate shell completion script
my-cli complete zsh

# Parse completion request (called by shell)
my-cli complete -- install --port=""
```

**Output Format:**

```
--port=3000    Development port
--port=8080    Production port
:4
```

## Documentation

See [bombshell docs](https://bomb.sh/docs/tab/).

## Contributing

We welcome contributions! tab's architecture makes it easy to add support for new package managers or CLI frameworks.

## Acknowledgments

tab was inspired by the great [Cobra](https://github.com/spf13/cobra/) project, which set the standard for CLI tooling in the Go ecosystem.

## Adoption Support

We want to make it as easy as possible for the JS ecosystem to enjoy great autocompletions.  
We at [thundraa](https://thundraa.com) would be happy to help any open source CLI utility adopt tab.
If you maintain a CLI and would like autocompletions set up for your users, just [drop the details in our _Adopting tab_ discussion](https://github.com/bombshell-dev/tab/discussions/61).  
We’ll gladly help and even open a PR to get you started.
