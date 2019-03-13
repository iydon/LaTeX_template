# -*- coding: utf-8 -*-
import os
import re


CODE = "code"
PDF  = "pdf"
BODY = "body"
ENCO = "utf-8"
EXT  = ".tex"
CROP = "-crop"
CON  = r"""
\documentclass[AutoFakeBold,AutoFakeSlant]{ctexart}
\usepackage{tcolorbox}
    \tcbuselibrary{listings}
        \newtcblisting{latexbox}[1]%%
            {colback=white,colframe=blue!50!white,fonttitle=\bfseries,%%
             listing options={basicstyle=\ttfamily,%%
             language={TeX},breaklines},title=\texttt{#1}}
    \usepackage{geometry}
        \geometry{margin=1in}
\pagestyle{empty}
%% Packages
%s
\begin{document}
\begin{latexbox}{%s}
%s
%s
\end{latexbox}
\end{document}
"""

BOD  = r"""
\section[%s]{%s\attachfile[description={Source Code},author={Iydon}]{%s}}
\noindent\includegraphics[width=\textwidth]{%s/%s}
"""

pat_doc = "(?<=\\\\begin\{document\}\n)[\s\S]+?(?=\n\\\\end\{document\})"
pat_pre = "\\\\documentclass[\s\S]+?(?=\n\\\\begin\{document\})"
# documentclass写在一行中, 不分行
brk_lin = "\n"
ind_tab = "    "
rpl_ecp = lambda s: s.replace("\\", "/")
rpl_dir = lambda s: s.replace(CODE, PDF, 1)
rpl_com = lambda s: "% " + (brk_lin+"% ").join(s.splitlines())

crop_pdf = []
with open(BODY+EXT, "w", encoding=ENCO) as f:
	pass

for dirpath, dirnames, filenames in os.walk(CODE):
    for filepath in filenames:
        file_path = os.path.join(dirpath, filepath)
        if not file_path.endswith(EXT):
            continue
        file = filepath[:-len(EXT)]
        with open(file_path, "r", encoding=ENCO) as f:
            content = f.read()
        document = re.findall(pat_doc, content)[0]
        preamble = re.findall(pat_pre, content)[0]
        cls,pkg  = preamble.split(brk_lin, maxsplit=1)
        with open(rpl_dir(file_path), "w", encoding=ENCO) as f:
            f.write(CON%(pkg,file,rpl_com(pkg),document))
        os.system("cd %s && latexmk -xelatex %s"%(PDF,rpl_ecp(file)))
        os.system("cd %s && pdfcrop %s.pdf"%(PDF,file))
        crop_pdf.append("%s/%s%s"%(PDF,file,CROP))
        with open(BODY+EXT, "a+", encoding=ENCO) as f:
            f.write(BOD%(file,file,rpl_ecp(file_path),PDF,file+CROP))
os.system("latexmk -xelatex main")

os.system("clear")
print(crop_pdf)
