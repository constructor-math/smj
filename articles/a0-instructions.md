# Instructions for Authors

Documentation for anyone adding a new article to the SMJ. This file is not
compiled — it lives in the source tree so contributors can read it next to
the real article files.

---

## What an article file looks like

Every `articles/aN-<slug>.tex` is a thin wrapper with exactly three parts,
in this order:

1. `\smjarticle{<label>}{ metadata }`
2. optional counter configuration
3. `\import{articles/papers/<slug>/}{main.tex}`

The real content of the article lives under `articles/papers/<slug>/`, not
in the wrapper.

---

## Part 1 — Metadata

```latex
\smjarticle{art:<slug>}{%
  title       = {Full Title},
  cover-title = {Short Title for the Cover},
  toc-title   = {Short Title for the ToC},
  author      = {Author Name},
  year        = {PROGRAM'YY},
  affil       = {UgS N},
  category    = {article},
  abstract    = {Short paragraph},
  no-header   = {true},
}
```

### Keys

| Key             | Required | Meaning                                                                                                                                                                           |
| --------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`       | yes      | Full title. Used in the article header and as fallback for`cover-title` and `toc-title`.                                                                                      |
| `cover-title` | no       | Used on the front-page cover grid and as the running header. Falls back to`title`.                                                                                              |
| `toc-title`   | no       | Used in the Table of Contents. Falls back to`title`.                                                                                                                            |
| `author`      | yes      | Bare name. No title, no degree.                                                                                                                                                   |
| `year`        | yes      | Convention:`PROGRAM'YY` (e.g. `CS'27`, `ECE'27`, `PHDS'26`). Rendered gray-italic under the author.                                                                       |
| `affil`       | no       | Convention:`UgS I` … `UgS N`, the seminar the paper originated in. Appears in the ToC but not on the cover.                                                                  |
| `category`    | yes      | `article` (full paper) or `editorial` (front-matter piece). `editorial` switches the header to a centered title with no author line and skips the per-article bibliography. |
| `abstract`    | no       | If present, rendered inside a centered minipage between two crimson rules on the first page.                                                                                      |
| `no-header`   | no       | If`true`, `\smjemitarticleheader` suppresses even the automatic title block. Use for short front-matter pieces that provide their own title.                                  |

**Label convention:** `art:<slug>`. Must be unique across the document.
It becomes the hyperref anchor for the article.

---

## Part 2 — Counter configuration

By default, theorem-like environments number flat:

```
Theorem 1, Theorem 2, Lemma 3, …
```

Some articles prefer per-section numbering:

```
Theorem 3.1, Theorem 3.2, Lemma 3.3, …
```

To switch, wrap the `\import` with:

```latex
\counterwithin{thrmctr}{section}
\import{articles/papers/<slug>/}{main.tex}
\counterwithout{thrmctr}{section}
```

**Why both lines?** `\counterwithin` permanently couples `thrmctr` to
`section`. Without the matching `\counterwithout` afterward, the **next**
article inherits per-section numbering and its theorems reset at every
section break. The restore line returns the global state to flat.

Which articles do this today:

| Article          | Numbering   |
| ---------------- | ----------- |
| `a1-shor`      | flat        |
| `a2-shannon`   | per-section |
| `a3-putt-putt` | flat        |
| `a4-divisors`  | per-section |
| `a5-agreement` | flat        |

The same wrapping works for any other counter you need to scope, e.g.
`\counterwithin{equation}{section}`.

---

## Part 3 — The `\import` call

```latex
\import{articles/papers/<slug>/}{main.tex}
```

`\import` differs from `\input` in one important way: it temporarily sets
the working directory to the first argument, so everything the sub-file
inputs — sections, figures, bibliography — resolves relative to that
folder. Without `\import`, each sub-file would have to write long relative
paths for its own assets.

The sub-file `articles/papers/<slug>/main.tex` is responsible for
inputting its own `sections/`, its preamble, and calling
`\smjbibliography` at the end.

---

## File naming

```
Wrapper:      articles/aN-<slug>.tex
Sub-folder:   articles/papers/<slug>/
Sub-entry:    articles/papers/<slug>/main.tex
Sections:     articles/papers/<slug>/sections/*.tex
Assets:       articles/papers/<slug>/assets/*
Refs:         articles/papers/<slug>/references.bib
```

`<slug>` is lowercase, hyphenated, and stable. Examples: `shor`,
`shannon`, `putt`, `divisors`, `agreement`.

---

## Bibliography

Each article's `main.tex` ends with:

```latex
\smjbibliography{articles/papers/<slug>/references}
```

This prints the "References" heading, runs `\putbib` on the given `.bib`
file, and closes the bibunit that `\smjarticle` opened at the start of the
article.

For an article with no citations, call:

```latex
\smjbibliography{}
```

to close the bibunit without printing a refs section.

Editorial pieces skip bibunits entirely, so `\smjbibliography` is not
needed for them.

---

## Theorem-like environments

Boxed, with optional title and optional label:

```latex
\begin{smjtheorem}[Optional Title]{optional:label}
    ...
\end{smjtheorem}
```

**Boxed environments:**
`smjtheorem`, `smjlemma`, `smjproposition`, `smjcorollary`,
`smjdefinition`, `smjnamedtheorem`

**Unboxed environments:**
`smjremark`, `smjnote`, `smjfact`, `smjexample`

Cross-reference with `\Cref{label}`. The environment type ("Theorem",
"Lemma", …) is inferred automatically.

---

## Common pitfalls

1. **Do not write content directly in the wrapper file.** Only the three
   parts above belong here.
2. **Do not forget `\counterwithout` if you used `\counterwithin`.**
   Leaving it out will silently change numbering of every article that
   follows.
3. **Do not re-use labels across articles.** Prefix with the slug:
   `sec:shor-prelim`, not `sec:prelim`.
4. **Do not manually `\clearpage` at the start of an article.**
   `\smjemitarticleheader` does it for you.
5. **Order is set in `main.tex`, not by filenames.** The order in
   `main.tex` determines the order in the PDF, the cover grid, and the
   ToC. Wrapper filenames (`a1`, `a2`, …) do not imply order.

---

## Template — copy into a new file

Create `articles/aN-<slug>.tex` with the following, filled in:

```latex
% ============================================================
%  articles/aN-<slug>.tex
%  <Full Title> — <Author Name>
% ============================================================

\smjarticle{art:<slug>}{%
  title       = {<Full Title>},
  cover-title = {<Short Title>},
  toc-title   = {<Short Title>},
  author      = {<Author Name>},
  year        = {<PROGRAM'YY>},
  affil       = {UgS <N>},
  category    = {article},
  abstract    = {<Short abstract, two to six sentences.>},
}

% Uncomment the two lines below only if this article should
% number theorems per section (3.1, 3.2, …).
% \counterwithin{thrmctr}{section}
\import{articles/papers/<slug>/}{main.tex}
% \counterwithout{thrmctr}{section}
```

Then create the sub-folder `articles/papers/<slug>/` with at least
`main.tex` and `references.bib`, and register the wrapper in `main.tex`:

```latex
\input{articles/aN-<slug>}
```
