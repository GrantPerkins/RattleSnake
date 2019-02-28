RattleSnake by Grant Perkins

This project is a very rudimentary compiler for the RattleSnake language. It take a .rsnake file as input, and creates an .exe

Dependencies:

This compiler generates assembly for Windows x86. As such, it only works on windows.

The following commands must run in the command line:
	gcc
	ld
	nasm
	python

These can be installed by:
	gcc/ld:
		Install MinGW for windows. Must install GUI to get necessary packages. Link:
			https://osdn.net/projects/mingw/releases/68260
		packages:
			mingw32-base-bin
			mingw32-gcc-g++-bin
		
	nasm:
		Download Netwide Assembler for Windows here:
			https://www.nasm.us/pub/nasm/releasebuilds/2.14.02/win64/
		Run the .exe (as Adminstrator, prefereably)
		Add the location of the install to Path
			If .exe is run as Adminstrator, Path should include C:\Program Files\NASM

	python
		Download Python 3 if not already installed. Link:
			https://www.python.org/downloads/windows/

How to use compiler:

1. Open CMD
2. Run main.py
3. Select .rsnake file in pop-up that you wish to compiler
	Compiler then generates a.exe, and runs it.


