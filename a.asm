	global _main
	extern _printf
	section .text
_main:
	mov    ecx, 4
	mov    edx, 1
	mov    ebx, 2
	add    edx, ebx
	imul    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
    ret
out:
	db    "%d", 0DH, 0AH, 0
