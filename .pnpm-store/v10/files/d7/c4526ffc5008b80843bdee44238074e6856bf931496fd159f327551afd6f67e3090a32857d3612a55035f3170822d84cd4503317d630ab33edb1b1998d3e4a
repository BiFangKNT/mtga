# FZF for JavaScript

[![Tests](https://github.com/ajitid/fzf-for-js/actions/workflows/main.yml/badge.svg?branch=dev)](https://github.com/ajitid/fzf-for-js/actions/workflows/main.yml)
[![Docs deployment status](https://img.shields.io/netlify/e4324b0d-d5b2-4139-a688-e58f32a5af6b?label=Docs&logo=netlify)](https://app.netlify.com/sites/fzf/deploys)

[//]: # "Image, text and counter/assist image needs to follow this order to be correctly aligned"

<img src="assets/landing.gif" align="right" />

[Docs](https://fzf.netlify.app) · [Demo](https://fzf.netlify.app/docs/latest/basic) · [GitHub](https://github.com/ajitid/fzf-for-js) · [NPM](https://www.npmjs.com/package/fzf)

Originally available as [a fuzzy finder for CLIs](https://github.com/junegunn/fzf), FZF for JavaScript is a port of FZF's main algorithm so it can be used in browser context.

<img src="assets/landing-assist.png" width="100%" height="0.001px" />

## Quick look

Install FZF for JavaScript using:

```sh
npm i fzf
```

Then you can use it like:

<!-- prettier-ignore -->
```js
import { Fzf } from 'fzf'

const list = ['go', 'javascript', 'python', 'rust', 
              'swift', 'kotlin', 'elixir', 'java', 
              'lisp', 'v', 'zig', 'nim', 'rescript', 
              'd', 'haskell']

const fzf = new Fzf(list)
const entries = fzf.find('li')
console.log('ranking is:')
entries.forEach(entry => console.log(entry.item)) // lisp kotlin elixir
```

For more ways to use this library, [visit documentation](https://fzf.netlify.app/).

## Motivation

Command palette is becoming ubiquitous – you can find it in code editors ([Sublime Text](https://www.sublimetext.com/blog/articles/sublime-text-2-beta), VS Code), design tools ([Figma](https://forum.figma.com/t/new-quick-actions-menu/1788)), project management apps ([Height](https://twitter.com/michaelvillar/status/1347276324772192256), [Linear](https://linear.app/)), source control tools ([Fork](https://fork.dev/blog/posts/quick-launch/), Sublime Merge). Web apps are becoming more prevalent as well. FZF has a great fuzzy finding mechanism which could be used outside of CLI and into these palettes.

There is [a very good read](https://capiche.com/e/consumer-dev-tools-command-palette) about command palettes if you want to learn more.

## Thanks

- Junegunn Choi (author of FZF, [website](https://junegunn.kr/)) – for making his work available and accessible to us. You can [sponsor his project](https://github.com/junegunn/fzf).
