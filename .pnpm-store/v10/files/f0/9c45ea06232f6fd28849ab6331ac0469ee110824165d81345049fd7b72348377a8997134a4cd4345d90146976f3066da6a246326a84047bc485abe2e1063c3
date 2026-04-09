import type { Token } from './Token.js'
import type { Rule } from './LexerRules.js'

const breakingWhitespaceRegex = /^\s*\n\s*/v

export class Lexer {
  private readonly text: string = ''
  public readonly lexerRules: Rule[]
  public readonly current: Token
  public readonly next: Token
  public readonly previous: Token | undefined

  public static create (lexerRules: Rule[], text: string): Lexer {
    const current = this.read(lexerRules, text)
    text = current.text
    const next = this.read(lexerRules, text)
    text = next.text
    return new Lexer(lexerRules, text, undefined, current.token, next.token)
  }

  private constructor (lexerRules: Rule[], text: string, previous: Token | undefined, current: Token, next: Token) {
    this.lexerRules = lexerRules
    this.text = text
    this.previous = previous
    this.current = current
    this.next = next
  }

  private static read (lexerRules: Rule[], text: string, startOfLine = false): { text: string, token: Token } {
    startOfLine ||= breakingWhitespaceRegex.test(text)

    const start = text.length
    const initialWhitespace = (/^\s+/v).exec(text)?.[0] ?? ''
    text = text.trimStart()
    const trimmed = start - text.length

    for (const rule of lexerRules) {
      const partial = rule(text)
      if (partial !== null) {
        const initialLines = initialWhitespace.split('\n')
        const currentLines = partial.text.split('\n')
        const token = {
          ...partial,
          startOfLine,
          reduced: trimmed + partial.text.length,
          line: initialLines.length + currentLines.length - 2,
          column: currentLines.length === 1
            /* c8 ignore next 3 -- Defaults are for TS */
            ? (initialLines.at(-1)?.length ?? 0) +
              (currentLines.at(-1)?.length ?? 0)
            : (currentLines.at(-1)?.length ?? 0)
        }
        text = text.slice(token.text.length)
        return { text, token }
      }
    }
    throw new Error(`Unexpected Token ${text}`)
  }

  remaining (): string {
    return this.next.text + this.text
  }

  advance (): Lexer {
    const next = Lexer.read(this.lexerRules, this.text)
    return new Lexer(
      this.lexerRules, next.text, this.current, this.next, next.token
    )
  }
}
