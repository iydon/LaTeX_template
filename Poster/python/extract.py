from strmat import strmat
import sys, re


ENCOD = "utf-8"


def title_process(f, name):
    lines = name.split("\n")
    dct   = dict()
    for i in range(len(lines)):
        idx = lines[i].index(":")
        key = f(lines[i][:idx])
        val = lines[i][idx+1:].strip()
        dct[key] = val
    return dct

def option(obj, idx):
    result    = []
    start,end = obj.part[idx]
    pos       = tuple((start[i]+1)//3 for i in [0,-1])
    shp       = obj.get_box_shape(idx)
    result   += ["name=poster%s"%(obj.convert_to_roman(idx).lower()),\
                 "row=%s"%(pos[0]), "span=%s"%(shp[0]//2), \
                 "column=%s"%(pos[-1]), "span=%s"%(shp[-1]//2)]
    if end[0] == obj.shape[0]-1:
        result += ["above=bottom"]
    if start[0] != 0:
        tmp = obj.get_box_index(start[0]-1,start[-1])
        result += ["below=poster%s"%(obj.convert_to_roman(tmp).lower())]
    return result


with open(sys.argv[1], "r", encoding=ENCOD) as f:
    content = f.read()

layout = re.findall("(?<=:layout{)[^}]+?(?=})", content)[0]
name   = re.findall("(?<=:name{)[^}]+?(?=})", content)[0]

obj   = strmat(layout.strip())
title = title_process(obj.convert_to_arabic, name.strip())

result = "\\begin{postech}\n\n"
keys   = list(obj.part.keys())
for i in range(obj.PARTNUM):
    comment = "%% ------- %s -------\n"%(obj.convert_to_alpha(keys[i]))
    style   = "\\headerbox{%s}{%s}{\n%s}\n\n"
    posit   = ",".join(option(obj, i+1))
    style  %= (title[i+1], posit, "\\poster%s"%(obj.convert_to_roman(i+1).lower()))
    result += comment + style
result += "\n\n\\end{postech}"

with open("postent.tex", "w", encoding=ENCOD) as f:
    f.write(result)
