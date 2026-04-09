import { composeParslet } from './Parslet.js'
import { Precedence } from '../Precedence.js'
import { assertRootResult } from '../assertTypes.js'
import { UnexpectedTypeError } from '../errors.js'
import type { RootResult, InferResult } from '../result/RootResult.js'

export const genericParslet = composeParslet({
  name: 'genericParslet',
  accept: (type, next) => type === '<' || (type === '.' && next === '<'),
  precedence: Precedence.GENERIC,
  parseInfix: (parser, left) => {
    const dot = parser.consume('.')
    parser.consume('<')

    const elements: Array<RootResult | InferResult> = []

    do {
      if (parser.consume('infer')) {
        const name = parser.parseIntermediateType(Precedence.SYMBOL)
        if (name.type !== 'JsdocTypeName') {
          throw new UnexpectedTypeError(name, 'A typescript infer always has to have a name.')
        }
        elements.push({
          type: 'JsdocTypeInfer',
          element: name
        })
      } else {
        elements.push(parser.parseType(Precedence.PARAMETER_LIST))
      }
    } while (parser.consume(','))

    if (!parser.consume('>')) {
      throw new Error('Unterminated generic parameter list')
    }

    return {
      type: 'JsdocTypeGeneric',
      left: assertRootResult(left),
      elements,
      meta: {
        brackets: 'angle',
        dot
      }
    }
  }
})
