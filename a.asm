	global _main
	extern _printf
	section .text
_main:
	mov    ecx, 1
	mov    edx, 2
	mov    ebx, 1
	sub    edx, ebx
	add    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
	mov    ecx, 1
	mov    edx, 9
	mov    ebx, 7
	imul    edx, ebx
	add    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
	mov    ecx, 2
	mov    edx, 3
	mov    ebx, 4
	imul    edx, ebx
	imul    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
    ret
out:
	db    "%d", 0DH, 0AH, 0
