# @codemirror/merge [![NPM version](https://img.shields.io/npm/v/@codemirror/merge.svg)](https://www.npmjs.org/package/@codemirror/merge)

[ [**WEBSITE**](https://codemirror.net/) | [**DOCS**](https://codemirror.net/docs/ref/#merge) | [**ISSUES**](https://github.com/codemirror/dev/issues) | [**FORUM**](https://discuss.codemirror.net/c/next/) | [**CHANGELOG**](https://github.com/codemirror/merge/blob/main/CHANGELOG.md) ]

This package implements a merge interface for the
[CodeMirror](https://codemirror.net/) code editor.

The [project page](https://codemirror.net/) has more information, a
number of [examples](https://codemirror.net/examples/) and the
[documentation](https://codemirror.net/docs/ref/#merge).

This code is released under an
[MIT license](https://github.com/codemirror/merge/tree/main/LICENSE).

We aim to be an inclusive, welcoming community. To make that explicit,
we have a [code of
conduct](http://contributor-covenant.org/version/1/1/0/) that applies
to communication around the project.

## Usage

A split merge view can be created like this:

```javascript
import {MergeView} from "@codemirror/merge"
import {EditorView, basicSetup} from "codemirror"
import {EditorState} from "@codemirror/state"

let doc = `one
two
three
four
five`

const view = new MergeView({
  a: {
    doc,
    extensions: basicSetup
  },
  b: {
    doc: doc.replace(/t/g, "T") + "\nSix",
    extensions: [
      basicSetup,
      EditorView.editable.of(false),
      EditorState.readOnly.of(true)
    ]
  },
  parent: document.body
})
```

Or a unified view like this:

```javascript
import {EditorView, basicSetup} from "codemirror"
import {unifiedMergeView} from "@codemirror/merge"

const view = new EditorView({
  parent: document.body,
  doc: "one\ntwo\nthree\nfour",
  extensions: [
    basicSetup,
    unifiedMergeView({
      original: "one\n...\nfour"
    })
  ]
})
```
