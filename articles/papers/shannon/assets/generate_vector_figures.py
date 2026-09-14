#!/usr/bin/env python3
"""Generate the two journal-ready vector diagrams used in the paper.

The script creates temporary standalone TikZ sources and compiles the final
vector PDFs into this directory. No third-party Python packages are required.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


OUT = Path(__file__).resolve().parent
ROOT = OUT.parent


HAMMING_BALLS = r"""
\documentclass[tikz,border=4pt]{standalone}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta,calc}
\definecolor{navy}{HTML}{17324D}
\definecolor{blue}{HTML}{2F6FAD}
\definecolor{lightblue}{HTML}{DCEEFF}
\definecolor{orange}{HTML}{E58B2A}
\definecolor{lightorange}{HTML}{FCE7CE}
\begin{document}
\begin{tikzpicture}[font=\sffamily,>=Stealth]
  \def\r{2.05}
  \coordinate (c) at (-3.7,0);
  \coordinate (cp) at (3.7,0);

  \filldraw[fill=lightblue,fill opacity=.68,draw=blue,
            thick,dashed] (c) circle (\r);
  \filldraw[fill=lightorange,fill opacity=.68,draw=orange,
            thick,dashed] (cp) circle (\r);

  \foreach \dx/\dy in {-1.05/-.65,-.95/.62,-.52/-1.18,
      -.45/1.12,.12/-1.32,.10/1.30,.68/-.95,.72/.93,
      1.10/-.35,1.12/.40}{
    \draw[blue,thick,fill=white] ($(c)+(\dx,\dy)$) circle (.11);
    \draw[orange,thick,fill=white] ($(cp)+(\dx,\dy)$) circle (.11);
  }

  \node[draw=navy,very thick,fill=blue,text=white,rounded corners=1.5pt,
        minimum width=.48cm,minimum height=.48cm,font=\bfseries] at (c) {$\mathbf c$};
  \node[draw=navy,very thick,fill=orange,text=white,rounded corners=1.5pt,
        minimum width=.48cm,minimum height=.48cm,font=\bfseries] at (cp) {$\mathbf c'$};

  \node[font=\bfseries] at ($(c)+(0,1.72)$) {$B_t(\mathbf c)$};
  \node[font=\bfseries] at ($(cp)+(0,1.72)$) {$B_t(\mathbf c')$};

  \draw[navy,thick,dashed,<->] ($(c)+(.30,0)$) --
    node[midway,fill=white,inner sep=3pt] {$d_{\min}>2t$}
    ($(cp)+(-.30,0)$);

  \draw[gray,thick,fill=white] (-1.20,-2.32) circle (.11);
  \node[anchor=west,font=\footnotesize] at (-.98,-2.32)
        {possible received word};
\end{tikzpicture}
\end{document}
""".strip()


POLARIZATION_RECURSION = r"""
\documentclass[tikz,border=4pt]{standalone}
\usepackage{amsmath}
\usetikzlibrary{arrows.meta,positioning}
\definecolor{navy}{HTML}{17324D}
\definecolor{blue}{HTML}{2F6FAD}
\definecolor{lightblue}{HTML}{DCEEFF}
\definecolor{orange}{HTML}{E58B2A}
\definecolor{lightorange}{HTML}{FCE7CE}
\definecolor{gray}{HTML}{607080}
\definecolor{lightgray}{HTML}{EEF2F5}
\begin{document}
\begin{tikzpicture}[
  font=\sffamily,
  >=Stealth,
  channel/.style={draw=blue,thick,fill=lightblue,rounded corners=2pt,
                  minimum width=1.55cm,minimum height=.44cm,inner sep=1pt},
  branch/.style={thick,rounded corners=4pt,minimum width=1.20cm,
                 minimum height=.52cm},
  wire/.style={draw=gray,thick}
]
  \node[font=\bfseries] at (-5.15,3.05) {$n=8$ independent uses of $W$};
  \node[font=\bfseries] at (5.15,3.05) {$n=8$ synthetic channels};

  \foreach \i/\y in {1/2.35,2/1.70,3/1.05,4/.40,5/-.40,
                       6/-1.05,7/-1.70,8/-2.35}{
    \node[channel] (in\i) at (-5.15,\y) {$W$ use \i};
    \node[channel] (out\i) at (5.15,\y) {$W_{8}^{(\i)}$};
    \draw[wire] (in\i.east) -- (-3.85,\y);
    \draw[wire] (3.85,\y) -- (out\i.west);
  }

  \draw[navy,very thick] (-3.85,-2.35) -- (-3.85,2.35);
  \draw[navy,very thick] (3.85,-2.35) -- (3.85,2.35);

  \node[draw=gray,very thick,fill=lightgray,rounded corners=10pt,
        minimum width=6.75cm,minimum height=5.15cm] (transform) at (0,0) {};
  \node[font=\bfseries\small,align=center] at (0,2.05)
        {coupled recursive\\polarization transform};
  \node at (0,1.52) {$m=\log_2 n=3$ stages};

  \draw[navy,very thick,->] (-3.85,0) -- (transform.west);
  \draw[navy,very thick,->] (transform.east) -- (3.85,0);

  \node[draw=navy,very thick,circle,fill=white,minimum size=.65cm,
        inner sep=0pt,font=\bfseries] (w) at (-.72,-.15) {$W$};
  \node[branch,draw=orange,fill=lightorange] (minus) at (1.12,.62) {$W^-$};
  \node[branch,draw=blue,fill=lightblue] (plus) at (1.12,-.92) {$W^+$};
  \draw[navy,thick,->] (w) -- (minus);
  \draw[navy,thick,->] (w) -- (plus);
  \node[font=\footnotesize\itshape,below=1pt of minus] {less reliable};
  \node[font=\footnotesize\itshape,below=1pt of plus] {more reliable};
  \node[font=\footnotesize\itshape,text=gray] at (.18,1.13)
        {representative local split};
\end{tikzpicture}
\end{document}
""".strip()


def compile_figure(name: str, source: str) -> Path:
    output_path = OUT / f"{name}.pdf"
    with tempfile.TemporaryDirectory(prefix="shannon-figure-") as temp_dir:
        temp = Path(temp_dir)
        tex_path = temp / f"{name}.tex"
        tex_path.write_text(source + "\n", encoding="utf-8")
        subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={temp}",
                str(tex_path),
            ],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        shutil.copy2(temp / f"{name}.pdf", output_path)
    return output_path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "hamming_balls_discrete": HAMMING_BALLS,
        "polarization_recursion": POLARIZATION_RECURSION,
    }
    for name, source in figures.items():
        path = compile_figure(name, source)
        print(f"generated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
