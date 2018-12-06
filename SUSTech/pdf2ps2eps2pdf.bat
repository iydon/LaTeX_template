@echo off

rem TeX Live 2017+
echo We will process on "%1".

pdftops  "%1"      "%1.ps"
ps2eps   "%1.ps"   "%1.eps"
epspdf   "%1.eps"  "%1-Copy.pdf"

pause