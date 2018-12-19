import random


# Setting
LOW_COLOR  = "white"
HIGH_COLOR = "blue"
MATRIX     = [[random.random() for i in range(7)] for j in range(10)]
FILE       = "demo.tex"
ENCODE     = "utf-8"

# Main
MAIN = r"""
\documentclass{standalone}
%% Configure
\newcommand{\LowColor}{%s}
\newcommand{\HighColor}{%s}
%% Default
\usepackage{tikz}
\usepackage{collcell}
\newcommand*{\MinNumber}{0}%%
\newcommand*{\MaxNumber}{1}%%
\newcommand{\ApplyGradient}[1]{%%
  \pgfmathsetmacro{\PercentColor}{100.0*(#1-\MinNumber)/(\MaxNumber-\MinNumber)}
  \hspace{-0.33em}\colorbox{\HighColor!\PercentColor!\LowColor}{}
}
\newcolumntype{R}{>{\collectcell\ApplyGradient}c<{\endcollectcell}}
\renewcommand{\arraystretch}{0}
\setlength{\fboxsep}{3mm} %% box size
\setlength{\tabcolsep}{0pt}
\begin{document}
\begin{tabular}{*{%d}{R}}
%s
\end{tabular}
\end{document}
"""

length = len(MATRIX[0])
result = " \\\\\n".join(map(lambda e: " & ".join(map(str, e)), MATRIX))

with open(FILE, "w", encoding=ENCODE) as f:
	f.write(MAIN%(LOW_COLOR, HIGH_COLOR, length, result))