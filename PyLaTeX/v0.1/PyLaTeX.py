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

# Args
args = parser.parse_args()

# mkdir
if not os.path.exists(args.dir):
	os.makedirs(args.dir)

# extract the content
with open(file="%s.tex"%args.main, mode="r", encoding="utf-8") as f:
	pattern = "(?<=\\\\begin{pylatex})[\s\S]+?(?=\\\\end{pylatex})"
	envs = re.findall(pattern, f.read())

# evaluate the content
output = sys.stdout
index  = args.start
for env in envs:
	file   = "%s/%s%d.pytex"%(args.dir,args.file,index)
	index += 1
	outputfile = open(file=file, mode="w", encoding="utf-8")
	sys.stdout = outputfile
	exec(env.strip().strip("{}"))
	outputfile.close()
sys.stdout = output
