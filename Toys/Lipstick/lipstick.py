import json
import pprint


# Constant(s)
LIPSTICKJSON  = "lipstick.json"
LIPSTICKCOLOR = "lipstickcolor.sty"
LIPSTICKTEX   = "lipstick.tex"
ENCODE        = "utf-8"
BEGIN         = r"""
\documentclass{ctexart}
\usepackage{lipstickcolor}
\usepackage[top=1in,bottom=1in,left=1in,right=1in]{geometry}
\usepackage{animate,tikz,hyperref}
\usepackage[framemethod=tikz]{mdframed}
\def\lipstick[#1]#2{
  \def\coloredcontent{\textcolor{#1}{#2}}
  \begin{mdframed}[backgroundcolor=#1,roundcorner=8pt]
    \begin{animateinline}{7}
    \parbox{\textwidth}{\coloredcontent}
    \newframe*\parbox{\textwidth}{\centering\textcolor{white}{#2}}
    \newframe*\parbox{\textwidth}{\coloredcontent}
    \relax
    \end{animateinline}
  \end{mdframed}
}
\begin{document}
"""
END           = r"""
\end{document}
"""

# Variable(s)
color  = ""
middle = ""

# Function(s)
PYOUT = pprint.pprint


with open(LIPSTICKJSON, "r", encoding=ENCODE) as f:
    d = json.load(f)

middle += "\\tableofcontents\\clearpage\n"
for brand in d["brands"]:
    # PYOUT(brand["name"])
    middle += "\\section{%s}\n"%(brand["name"])
    for serie in brand["series"]:
        # PYOUT(serie["name"])
        middle += "\\subsection{%s}\n"%(serie["name"])
        for lipstick in serie["lipsticks"]:
            name = "%s-%s-%s-%s"%(brand["name"],
                                   serie["name"],
                                   lipstick["id"],
                                   lipstick["name"])
            show = "%s-%s-\\#%s-%s"%(brand["name"],
                                   serie["name"],
                                   lipstick["id"],
                                   lipstick["name"])
            # print(name, lipstick["color"])
            color  += "\\definecolor{%s}{HTML}{%s}\n"%(name, lipstick["color"][1:])
            middle += "\\lipstick[%s]{%s}\n"%(name, show)
    middle += "\\clearpage\n"

with open(LIPSTICKCOLOR, "w", encoding=ENCODE) as f:
    f.write("\\RequirePackage{xcolor}\n")
    f.write(color)
    f.write("\\endinput")

with open(LIPSTICKTEX, "w", encoding=ENCODE) as f:
	f.write(BEGIN)
	f.write(middle)
	f.write(END)