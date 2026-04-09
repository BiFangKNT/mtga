#!/usr/bin/env node

import inspector from 'node:inspector'
import nodeModule from 'node:module'
import process from 'node:process'
import { fileURLToPath } from 'node:url'

// https://nodejs.org/api/module.html#moduleenablecompilecachecachedir
// https://github.com/nodejs/node/pull/54501
if (nodeModule.enableCompileCache && !process.env.NODE_DISABLE_COMPILE_CACHE) {
  try {
    const { directory } = nodeModule.enableCompileCache()
    if (directory) {
      // allow child process to share the same cache directory
      process.env.NODE_COMPILE_CACHE ||= directory
    }
  }
  catch {
    // Ignore errors
  }
}

globalThis.__nuxt_cli__ = {
  startTime: Date.now(),
  entry: fileURLToPath(import.meta.url),
  devEntry: fileURLToPath(new URL('../dist/dev/index.mjs', import.meta.url)),
}

if (
  process.argv.includes('--profile')
  || process.argv.some(a => a.startsWith('--profile='))
) {
  const session = new inspector.Session()
  session.connect()

  try {
    // eslint-disable-next-line antfu/no-top-level-await
    await new Promise((resolve, reject) => {
      session.post('Profiler.enable', (err) => {
        if (err) {
          return reject(err)
        }
        session.post('Profiler.start', (err) => {
          if (err) {
            return reject(err)
          }
          resolve()
        })
      })
    })
    globalThis.__nuxt_cli__.cpuProfileSession = session
  }
  catch (err) {
    session.disconnect()
    throw err
  }
}

// eslint-disable-next-line antfu/no-top-level-await
const { runMain } = await import('../dist/index.mjs')

runMain()
