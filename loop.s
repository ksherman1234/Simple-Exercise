# Simple counter program in SCRAM assembly.

start:	LDA	count
	ADD	one
	STA	poopy
	JMP	start

count:	DAT	poopy	# counter variable
one:	DAT	1	# constant 1
