	.data
str_nl:.asciz "\n"
	.text
LO:
	j Lmain
L1:
	sw ra,0(sp)
L2:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-28(sp)
L3:
	lw t0,-28(sp)
	sw t0,-12(gp)
L4:
	lw t1,-12(sp)
	lw t2,-16(sp)
	bgt,t1,t2,L6
L5:
	j L10
L6:
	lw t1,-12(sp)
	lw t2,-20(sp)
	bgt,t1,t2,L8
L7:
	j L10
L8:
	lw t0,-12(sp)
	sw t0,-24(sp)
L9:
	j L17
L10:
	lw t1,-16(sp)
	lw t2,-12(sp)
	bgt,t1,t2,L12
L11:
	j L16
L12:
	lw t1,-16(sp)
	lw t2,-20(sp)
	bgt,t1,t2,L14
L13:
	j L16
L14:
	lw t0,-16(sp)
	sw t0,-24(sp)
L15:
	j L17
L16:
	lw t0,-20(sp)
	sw t0,-24(sp)
L17:
	lw ra,0(sp)
	jr ra
L18:
	sw ra,0(sp)
L19:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-16(sp)
L20:
	lw t0,-16(sp)
	sw t0,-12(gp)
L21:
	lw t1,-12(sp)
	li t2,0
	blt,t1,t2,L23
L22:
	j L25
L23:
	li t1,-1
	lw t0,-8(sp)
	sw t1,0(t0)
L24:
	j L41
L25:
	lw t1,-12(sp)
	li t2,0
	beq,t1,t2,L29
L26:
	j L27
L27:
	lw t1,-12(sp)
	li t2,1
	beq,t1,t2,L29
L28:
	j L31
L29:
	li t1,1
	lw t0,-8(sp)
	sw t1,0(t0)
L30:
	j L41
L31:
	lw t1,-12(sp)
	li t2,1
	sub t1,t1,t2
	sw t1,-20(sp)
L32:
	addi fp,sp,44
	lw t0,-20(sp)
	sw t0, -12(fp)
L33:
	addi t0,sp,-24
	sw t0,-8(fp)
L34:
	sw sp,-4(fp)
	addi sp,sp,44
	jal L18
	addi sp,sp,-44
L35:
	lw t1,-12(sp)
	li t2,2
	sub t1,t1,t2
	sw t1,-28(sp)
L36:
	addi fp,sp,44
	lw t0,-28(sp)
	sw t0, -12(fp)
L37:
	addi t0,sp,-32
	sw t0,-8(fp)
L38:
	sw sp,-4(fp)
	addi sp,sp,44
	jal L18
	addi sp,sp,-44
L39:
	lw t1,-24(sp)
	lw t2,-32(sp)
	add t1,t1,t2
	sw t1,-36(sp)
L40:
	lw t1,-36(sp)
	lw t0,-8(sp)
	sw t1,0(t0)
L41:
	lw ra,0(sp)
	jr ra
L42:
	sw ra,0(sp)
L43:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-20(sp)
L44:
	lw t0,-20(sp)
	sw t0,-12(gp)
L45:
	lw t1,-16(sp)
	lw t2,-12(sp)
	div t1,t1,t2
	sw t1,-24(sp)
L46:
	lw t1,-24(sp)
	lw t2,-12(sp)
	mul t1,t1,t2
	sw t1,-28(sp)
L47:
	lw t1,-16(sp)
	lw t2,-28(sp)
	beq,t1,t2,L49
L48:
	j L51
L49:
	li t1,1
	lw t0,-8(sp)
	sw t1,0(t0)
L50:
	j L52
L51:
	li t1,0
	lw t0,-8(sp)
	sw t1,0(t0)
L52:
	lw ra,0(sp)
	jr ra
L53:
	sw ra,0(sp)
L54:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-20(sp)
L55:
	lw t0,-20(sp)
	sw t0,-12(gp)
L56:
	li t0,2
	sw t0,-16(sp)
L57:
	lw t1,-16(sp)
	lw t2,-12(sp)
	blt,t1,t2,L59
L58:
	j L70
L59:
	addi fp,sp,36
	lw t0,-16(sp)
	sw t0, -12(fp)
L60:
	lw t0,-12(sp)
	sw t0, -16(fp)
L61:
	addi t0,sp,-24
	sw t0,-8(fp)
L62:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,36
	jal L42
	addi sp,sp,-36
L63:
	lw t1,-24(sp)
	li t2,1
	beq,t1,t2,L65
L64:
	j L67
L65:
	li t1,0
	lw t0,-8(sp)
	sw t1,0(t0)
L66:
	j L67
L67:
	lw t1,-16(sp)
	li t2,1
	add t1,t1,t2
	sw t1,-28(sp)
L68:
	lw t0,-28(sp)
	sw t0,-16(sp)
L69:
	j L57
L70:
	li t1,1
	lw t0,-8(sp)
	sw t1,0(t0)
L71:
	lw ra,0(sp)
	jr ra
L72:
	sw ra,0(sp)
L73:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-16(sp)
L74:
	lw t0,-16(sp)
	sw t0,-12(gp)
L75:
	lw t1,-12(sp)
	lw t2,-12(sp)
	mul t1,t1,t2
	sw t1,-20(sp)
L76:
	lw t1,-20(sp)
	lw t0,-8(sp)
	sw t1,0(t0)
L77:
	lw ra,0(sp)
	jr ra
L78:
	sw ra,0(sp)
L79:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-20(sp)
L80:
	lw t0,-20(sp)
	sw t0,-12(gp)
L81:
	addi fp,sp,28
	lw t0,-12(sp)
	sw t0, -12(fp)
L82:
	addi t0,sp,-24
	sw t0,-8(fp)
L83:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,28
	jal L72
	addi sp,sp,-28
L84:
	addi fp,sp,28
	lw t0,-12(sp)
	sw t0, -12(fp)
L85:
	addi t0,sp,-28
	sw t0,-8(fp)
L86:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,28
	jal L72
	addi sp,sp,-28
L87:
	lw t1,-24(sp)
	lw t2,-28(sp)
	mul t1,t1,t2
	sw t1,-32(sp)
L88:
	lw t0,-32(sp)
	sw t0,-16(sp)
L89:
	lw t1,-16(sp)
	lw t0,-8(sp)
	sw t1,0(t0)
L90:
	lw ra,0(sp)
	jr ra
L91:
	sw ra,0(sp)
L92:
	lw t1,-12(gp)
	li t2,1
	add t1,t1,t2
	sw t1,-16(sp)
L93:
	lw t0,-16(sp)
	sw t0,-12(gp)
L94:
	lw t1,-12(sp)
	li t2,4
	rem t1,t1,t2
	sw t1,-20(sp)
L95:
	lw t1,-20(sp)
	li t2,0
	beq,t1,t2,L97
L96:
	j L100
L97:
	lw t1,-12(sp)
	li t2,100
	rem t1,t1,t2
	sw t1,-24(sp)
L98:
	lw t1,-24(sp)
	li t2,0
	bne,t1,t2,L103
L99:
	j L100
L100:
	lw t1,-12(sp)
	li t2,400
	rem t1,t1,t2
	sw t1,-28(sp)
L101:
	lw t1,-28(sp)
	li t2,0
	beq,t1,t2,L103
L102:
	j L105
L103:
	li t1,1
	lw t0,-8(sp)
	sw t1,0(t0)
L104:
	j L106
L105:
	li t1,0
	lw t0,-8(sp)
	sw t1,0(t0)
L106:
	lw ra,0(sp)
	jr ra
Lmain:
L107:
	addi,sp,sp,56
	mv gp,sp
L108:
	li t0,0
	sw t0,-12(sp)
L109:
	li a7,5
	ecall
	sw a0,-20(sp)
L110:
	lw t0,-20(sp)
	sw t0,-16(sp)
L111:
	lw t0,-16(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L112:
	li t0,1600
	sw t0,-16(sp)
L113:
	lw t1,-16(sp)
	li t2,2000
	ble,t1,t2,L115
L114:
	j L122
L115:
	addi fp,sp,36
	lw t0,-16(sp)
	sw t0, -12(fp)
L116:
	addi t0,sp,-24
	sw t0,-8(fp)
L117:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,36
	jal L91
	addi sp,sp,-36
L118:
	lw t0,-24(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L119:
	lw t1,-16(sp)
	li t2,400
	add t1,t1,t2
	sw t1,-28(sp)
L120:
	lw t0,-28(sp)
	sw t0,-16(sp)
L121:
	j L113
L122:
	addi fp,sp,36
	li t0,2023
	sw t0, -12(fp)
L123:
	addi t0,sp,-32
	sw t0,-8(fp)
L124:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,36
	jal L91
	addi sp,sp,-36
L125:
	lw t0,-32(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L126:
	addi fp,sp,36
	li t0,2024
	sw t0, -12(fp)
L127:
	addi t0,sp,-36
	sw t0,-8(fp)
L128:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,36
	jal L91
	addi sp,sp,-36
L129:
	lw t0,-36(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L130:
	addi fp,sp,44
	li t0,3
	sw t0, -12(fp)
L131:
	addi t0,sp,-40
	sw t0,-8(fp)
L132:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,44
	jal L78
	addi sp,sp,-44
L133:
	lw t0,-40(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L134:
	addi fp,sp,44
	li t0,5
	sw t0, -12(fp)
L135:
	addi t0,sp,-44
	sw t0,-8(fp)
L136:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,44
	jal L18
	addi sp,sp,-44
L137:
	lw t0,-44(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L138:
	li t0,1
	sw t0,-16(sp)
L139:
	lw t1,-16(sp)
	li t2,12
	ble,t1,t2,L141
L140:
	j L148
L141:
	addi fp,sp,40
	lw t0,-16(sp)
	sw t0, -12(fp)
L142:
	addi t0,sp,-48
	sw t0,-8(fp)
L143:
	lw t0,-4(sp)
	sw t0,-4(fp)
	addi sp,sp,40
	jal L53
	addi sp,sp,-40
L144:
	lw t0,-48(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L145:
	lw t1,-16(sp)
	li t2,1
	add t1,t1,t2
	sw t1,-52(sp)
L146:
	lw t0,-52(sp)
	sw t0,-16(sp)
L147:
	j L139
L148:
	lw t0,-12(sp)
	mv a0,t0
	li a7,1
	ecall
	la a0,str_nl
	li a7,4
	ecall
L149:
	li a0,0
	li a7,93
	ecall
L150:
	lw ra,0(sp)
	jr ra
