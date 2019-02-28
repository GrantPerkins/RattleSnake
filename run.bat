@echo off
python main.py
nasm -fwin32 a.asm
gcc a.obj
a