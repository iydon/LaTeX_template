import argparse
import sys
import os
import re


# CONTENT
NAME    = "PyLaTeX"
DESCRIP = "PyLaTeX. This work has the LPPL maintenance status `maintained'."
MAIN_H  = "Read main file and evaluate."
DIR_H   = "New folder using this dir name."
FILE_H  = "New file using this file name."
START_H = "File start from."
# TYPE_H  = "Use `re' or loop to find the pattern."

# New parser
parser = argparse.ArgumentParser()
parser.description = DESCRIP

# Add argument
# python PyLaTeX.py -m main -d pylatex -f output -s 0
parser.add_argument("-v", "--version", action="version", version="%s 0.1"%NAME)
parser.add_argument("-m", "--main",  type=str, help=MAIN_H)
parser.add_argument("-d", "--dir",   type=str, help=DIR_H)
parser.add_argument("-f", "--file",  type=str, help=FILE_H)
parser.add_argument("-s", "--start", type=int, help=START_H)
# parser.add_argument("-t", "--type",  type=int, help=TYPE_H)

# Args
args = parser.parse_args()

# mkdir
if not os.path.exists(args.dir):
    os.makedirs(args.dir)

# extract the content
cmds   = []

def extract_content(file_name):
    with open(file=file_name, mode="r", encoding="utf-8") as f:
        result = ""
        idx    = 0
        count  = 0
        for line in f.readlines():
            file = re.findall("(?<=\\\\input{)[\S]+(?=})", line)
            if file: extract_content("%s.tex"%file[0])
            file = re.findall("(?<=\\\\include{)[\S]+(?=})", line)
            if file: extract_content("%s.tex"%file[0])
            if "\\pylatex{" in line:
                result += line
                count += 1
                continue
            if count:
                for idx in range(len(line)):
                    if line[idx] == "{":
                        count += 1
                    elif line[idx] == "}":
                        count -= 1
                if not count:
                    globals()["cmds"].append(result+line[:idx+1])
                    result = ""
                    continue
                result += line[:idx+1]
extract_content("%s.tex"%args.main)

# evaluate the content
output = sys.stdout
index  = args.start
for cmd in cmds:
    import re
    file   = "%s/%s%d.pytex"%(args.dir,args.file,index)
    index += 1
    outputfile = open(file=file, mode="w", encoding="utf-8")
    sys.stdout = outputfile
    exec(re.findall("(?<=\\\\pylatex{)[\s\S]+(?=})", cmd)[0])
    outputfile.close()
sys.stdout = output
