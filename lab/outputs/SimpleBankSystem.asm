	.data
str_nl:.asciz "\n"
	.text
LO:
	j Lmain
L1:
	sw ra,0(sp)
L2:
	lw t1,-12(sp)
	li t2,0
	blt,t1,t2,L4
L3:
	j L9
L4:
	lw t1,-12(gp)
	lw t2,-12(sp)
	add t1,t1,t2
	sw t1,-16(sp)
L5:
	lw t0,-16(sp)
	sw t0,-12(gp)
L6:
	lw t1,-12(gp)
	lw t2,-12(sp)
	add t1,t1,t2
	sw t1,-20(sp)
L7:
	lw t1,-20(sp)
	lw t0,-8(sp)
	sw t1,0(t0)
L8:
	j L10
L9:
	li t1,-1
	lw t0,-8(sp)
	sw t1,0(t0)
L10:
	lw ra,0(sp)
	jr ra
L11:
	sw ra,0(sp)
L12:
	lw t1,-12(sp)
	li t2,0
	bgt,t1,t2,L14
L13:
	j L20
L14:
	lw t1,-12(sp)
	lw t2,-12(gp)
	ble,t1,t2,L16
L15:
	j L20
L16:
	lw t1,-12(gp)
	lw t2,-12(sp)
	sub t1,t1,t2
	sw t1,-16(sp)
L17:
	lw t0,-16(sp)
	sw t0,-12(gp)
L18:
	lw t0,-12(gp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L19:
	j L25
L20:
	lw t1,-12(sp)
	lw t2,-12(gp)
	bgt,t1,t2,L22
L21:
	j L24
L22:
	li t1,0
	lw t0,-8(sp)
	sw t1,0(t0)
L23:
	j L25
L24:
	li t1,-1
	lw t0,-8(sp)
	sw t1,0(t0)
L25:
	lw ra,0(sp)
	jr ra
Lmain:
L26:
	addi,sp,sp,40
	mv gp,sp
L27:
	li t0,0
	sw t0,-12(sp)
L28:
	li a7,5
	ecall
	sw a0,-24(sp)
L29:
	lw t0,-24(sp)
	sw t0,-16(sp)
L30:
	li a7,5
	ecall
	sw a0,-28(sp)
L31:
	lw t0,-28(sp)
	sw t0,-20(sp)
L32:
	lw t1,-16(sp)
	li t2,1
	beq,t1,t2,L34
L33:
	j L39
L34:
	addi fp,sp,28
	lw t0,-20(sp)
	sw t0, -12(fp)
L35:
	addi t0,sp,-32
	sw t0,-8(fp)
L36:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,28
	jal L1
	addi sp,sp,-28
L37:
	lw t0,-32(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L38:
	j L46
L39:
	lw t1,-16(sp)
	li t2,2
	beq,t1,t2,L41
L40:
	j L46
L41:
	addi fp,sp,24
	lw t0,-20(sp)
	sw t0, -12(fp)
L42:
	addi t0,sp,-36
	sw t0,-8(fp)
L43:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,24
	jal L11
	addi sp,sp,-24
L44:
	lw t0,-36(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L45:
	j L46
L46:
	li a0,0
	li a7,93
	ecall
L47:
	lw ra,0(sp)
	jr ra
