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
	beq,t1,t2,L6
L3:
	j L4
L4:
	lw t1,-12(sp)
	li t2,1
	beq,t1,t2,L6
L5:
	j L8
L6:
	li t1,1
	lw t0,-8(sp)
	sw t1,0(t0)
L7:
	j L14
L8:
	lw t1,-12(sp)
	li t2,1
	sub t1,t1,t2
	sw t1,-16(sp)
L9:
	addi fp,sp,28
	lw t0,-16(sp)
	sw t0, -12(fp)
L10:
	addi t0,sp,-20
	sw t0,-8(fp)
L11:
	sw sp,-4(fp)
	addi sp,sp,28
	jal L1
	addi sp,sp,-28
L12:
	lw t1,-12(sp)
	lw t2,-20(sp)
	mul t1,t1,t2
	sw t1,-24(sp)
L13:
	lw t1,-24(sp)
	lw t0,-8(sp)
	sw t1,0(t0)
L14:
	lw ra,0(sp)
	jr ra
Lmain:
L15:
	addi,sp,sp,24
	mv gp,sp
L16:
	li a7,5
	ecall
	sw a0,-16(sp)
L17:
	lw t0,-16(sp)
	sw t0,-12(sp)
L18:
	addi fp,sp,28
	lw t0,-12(sp)
	sw t0, -12(fp)
L19:
	addi t0,sp,-20
	sw t0,-8(fp)
L20:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,28
	jal L1
	addi sp,sp,-28
L21:
	lw t0,-20(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L22:
	li a0,0
	li a7,93
	ecall
L23:
	lw ra,0(sp)
	jr ra
