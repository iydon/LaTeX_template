import re
import rstr
import subprocess
import sys


cmd = "fc-list :lang=zh"
encode = "utf-8"
with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as f:
    popen = f.communicate()[0]

lines = popen.splitlines()
for i in range(len(lines)-1,-1,-1):
    try:
        lines[i] = lines[i].decode(encode)
    except Exception as e:
        del(lines[i])

if "win" in sys.platform:
    fonts = dict()
    pattern = "(?<=/)[^/]+?:[^:]+(?=:)"
    for l in lines:
        tmp = re.findall(pattern,l)
        if tmp:
            k,v = tmp[0].split(":")
            fonts[k] = v

    file = "win-test.tex"
    init_font = "KaiTi"
elif "linux" in sys.platform:
    fonts = dict()
    pattern = "(?<=:)[^:]+(?=:)"
    for l in lines:
        tmp = re.findall(pattern,l)
        if tmp:
            k = tmp[0].strip().split(",")
            fonts[k[0]] = k[-1]

    file = "linux-test.tex"
    init_font = "AR PL UMing CN"

document = r"""
\documentclass{standalone}
\usepackage{ifxetex}
    \ifxetex\else
        \errmessage{You Should Use XeLaTeX To Compile.}
    \fi
\usepackage{fontspec}

\newfontfamily\kaiti{%s}
%s
\begin{document}
\begin{tabular}{|l|c|}
\hline
%s
\end{tabular}
\end{document}
"""

famliy = ""
table  = ""
test   = "你好，世界！"
for k,v in fonts.items():
    command = rstr.xeger("[a-zA-Z]{8}")
    famliy += r"\newfontfamily\%s{%s}"%(command, k) + "\n"
    table  += r"\kaiti %s & \%s %s \\"%(v, command, test) + "\n"

with open(file, "w", encoding=encode) as f:
    f.write(document%(init_font, famliy, table))
