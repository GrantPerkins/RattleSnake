	global _main
	extern _printf
	section .text
_main:
	mov    ecx, 180
	mov    edx, 7
	add    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
	mov    ecx, 9
	mov    edx, 7
	sub    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
	mov    ecx, 4
	mov    edx, 5
	imul    ecx, edx
	push    ecx
	push    out
	call    _printf
	add    esp, 4
    ret
out:
	db    "%d", 0DH, 0AH, 0
