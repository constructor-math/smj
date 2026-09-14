
# Instructions for Editorials

Documentation for anyone writing front-matter editorial pieces. This file is
not compiled — it lives in the source tree so contributors can read it next
to the real editorial files.

---

## What an editorial file looks like

Every `editorial/eN-<slug>.tex` is a thin wrapper with exactly two parts,
in this order:

1. `\smjarticle{<label>}{ metadata }`
2. the body content — headings, prose, acknowledgements

Unlike articles, editorials do **not** use `\import`. There is no
sub-folder; the wrapper *is* the content.

---

## Part 1 — Metadata

```latex
\smjarticle{art:<slug>}{%
  title    = {Editorial Title},
  author   = {Author Name},
  year     = {MATH'25},
  affil    = {},
  category = {editorial},
}
```

### Keys

| Key             | Required | Meaning                                                                                   |
| --------------- | -------- | ----------------------------------------------------------------------------------------- |
| `title`       | yes      | Editorial title. Used in the header and as fallback for`cover-title` and `toc-title`. |
| `author`      | yes      | Bare name.                                                                                |
| `year`        | yes      | Convention:`PROGRAM'YY` (e.g. `MATH'25`). Rendered gray-italic.                       |
| `affil`       | no       | Usually empty for editorials.                                                             |
| `category`    | yes      | **Must be `editorial`.** This is what switches the layout.                        |
| `cover-title` | no       | Rarely needed for editorials — they typically don't appear on the front cover grid.      |
| `toc-title`   | no       | Falls back to`title`.                                                                   |
| `abstract`    | no       | Editorials typically don't have abstracts.                                                |
| `no-header`   | no       | Not used for editorials.                                                                  |

**Label convention:** `art:<slug>`. Must be unique across the document.
Examples: `art:volume`, `art:address`.

---

## What `category = {editorial}` does

It is not cosmetic. Setting it changes three things in the build:

1. **Header layout.** Instead of the two-rule author block used for
   articles, the editorial gets a centered `\LARGE\bfseries` title with a
   gold rule underneath and no author line.
2. **No bibliography.** The `\smjarticle` macro only opens a `bibunit`
   when `category = {article}`. Editorials are skipped, so you must
   **not** call `\smjbibliography` at the end.
3. **Cover and ToC filtering.** When the cover or ToC calls
   `\smjcoverentries{article}` or `\smjcontentsentries{article}`,
   editorials are excluded. To include editorials in a listing, pass
   `{editorial}` or `{all}` instead.

Forgetting to set `category = {editorial}` will make the piece render as
a full article with author line and open a bibunit that never closes —
build-breaking.

---

## Part 2 — Body

The body is plain LaTeX. Conventions used by existing editorials:

### Section headings

Use the inline heading macros, **not** `\section`:

```latex
\smjsubheading{A Short Story}
\vspace{0.3cm}
... prose ...
```

`\smjsubheading` produces a crimson bold heading one size down from
`\smjheading`. Because editorials have no section numbering, numbered
`\section` is not appropriate here.

### Paragraph spacing

`\vspace{0.25cm}` between paragraphs is the house style for editorials.
`\vspace{0.3cm}` after a heading. Don't introduce new spacing values
unless you have a reason.

### Links

Center a block of URLs with a `center` environment:

```latex
\begin{center}
  \href{https://example.com}{\texttt{example.com}}\\
\end{center}
```

### Lists

Lists work. For a two-column list of names, use `multicols`:

```latex
\begin{multicols}{2}
\begin{itemize}
  \item Name One {\color{smjgray}CS'27}
  \item Name Two {\color{smjgray}ECE'27}
\end{itemize}
\end{multicols}
```

### Ending

Every editorial ends with a gold rule:

```latex
\smjgoldline{1.2pt}
```

Some add `\newpage` after it. Check whether the file is the last editorial
in `main.tex` before adding it — an extra `\newpage` at the end of the
document produces a blank trailing page.

---

## File naming and placement

```
editorial/eN-<slug>.tex
```

`<slug>` is lowercase, hyphenated, and stable. Examples: `thisvolume`,
`editorial`.

Load order is set in `main.tex`:

```latex
\input{editorial/e1-thisvolume}
\input{editorial/e2-editorial}
```

Filenames suggest order but do not enforce it.

---

## Common pitfalls

1. **Do not forget `category = {editorial}`.** Without it, the piece
   renders as an article and opens a bibunit that never closes.
2. **Do not call `\smjbibliography`.** Editorials skip bibunits, so the
   call would silently do nothing at best, error at worst.
3. **Do not use `\section`, `\subsection`, etc.** Use `\smjsubheading`
   instead. Numbered sections make no sense in an unnumbered piece and
   will clash with the editorial header.
4. **Do not manually `\clearpage` at the start.** `\smjemitarticleheader`
   handles page breaks.
5. **Do not add an `\import` line.** Editorials have no sub-folder.
6. **Do not re-use labels across editorials.** Prefix with the slug:
   `art:volume`, `art:address` — never a bare `art:editorial`.

---

## Template — copy into a new file

Create `editorial/eN-<slug>.tex` with the following, filled in:

```latex
% ============================================================
%  editorial/eN-<slug>.tex — <Editorial Title>
% ============================================================
\smjarticle{art:<slug>}{%
  title    = {<Editorial Title>},
  author   = {<Author Name>},
  year     = {<PROGRAM'YY>},
  affil    = {},
  category = {editorial},
}

\noindent <Opening line>,

\vspace{0.25cm}

<Body paragraph.>

\vspace{0.25cm}

\smjsubheading{<Optional Subheading>}

\vspace{0.3cm}

<Body paragraph.>

\vspace{0.4cm}

\noindent\textit{Yours Sincerely, }\\
\textbf{<Author Name> --- <PROGRAM'YY>}\\
<Role>

\vspace{0.15cm}

\smjgoldline{1.2pt}

\vspace{0.3cm}
```

Then register it in `main.tex`:

```latex
\input{editorial/eN-<slug>}
```
