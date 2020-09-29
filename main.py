#!/usr/bin/env python3.8

from sys import exit, argv

labels = {}
variables = {
	"ACC": 0,
	"BAK": ""
}
current_line = 0

f = open(argv[1], "r")

# Functions to add the logic of the commands
def MOV(src, dst, lineno):
	if src == "BAK" or dst == "BAK":
		return

	dst = dst.strip("\n")
	if src[0] == "\"" or src[0] == "'":
		if src[-1] != "\"" and src[-1] != "'":
			print("Did you forgot to close the quotes?\nline:", lineno+1)
			f.close()
			exit(1)

		variables[dst] = eval(src)
	else:
		if src.isalpha():
			variables[dst] = str(variables[src])
		else:
			variables[dst] = eval(src)

	if dst == "OUT":
		if src[0] == "\"" or src[0] == "'":
			var = False
		else:
			var = True

		src = src.strip("\"'")

		if var:	
			if src.isalpha():
				print(variables[src])
			else:
				print(src)
		else:
			print(src)


def ADD(val, lineno):
	val = val.strip("\n")
	if val[0] == "\"" or val[0] == "'" or val[-1] == "\"" or val[-1] == "'":
		print("String not allowed in add command\nline:", lineno+1)
		f.close()
		exit(1)

	if val.isalpha():
		variables["ACC"] += int(variables[val])
	else:
		variables["ACC"] += int(val)

def SUB(val, lineno):
	if val[0] == "\"" or val[0] == "'" or val[-1] == "\"" or val[-1] == "'":
		print("String not allowed in sub command\nline:", lineno+1)
		f.close()
		exit(1)

	variables["ACC"] -= int(val)

def INP(var):
	var = var.strip("\n")
	variables[var] = input()

def LAB(label, lineno):
	label = label.strip("\n")
	labels[label] = lineno

def JMP(label):
	global i
	label = label.strip("\n")
	i = labels[label]

def JEZ(label):
	if variables["ACC"] == 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JNZ(label):
	if variables["ACC"] != 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JGZ(label):
	if variables["ACC"] > 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JLZ(label):
	if variables["ACC"] < 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JRO(offset):
	global i
	i += offset

def SAV():
	variables["ACC"] = BAK

def SWP():
	ACC = variables["ACC"]
	BAK = variables["BAK"]
	variables["ACC"] = BAK
	variables["BAK"] = ACC

def get_command(line: str):
		first_word = line.split(" ")[0]
		return first_word

line = f.readlines()

i = 0
# Parse file
while True:

	if i >= len(line):
		break

	currline = line[i]
	cmd = get_command(line[i])
	if cmd == "LAB":
		second: str = currline.split(" ")[1]
		LAB(second, i)
	else:
		pass

	i += 1

i = 0
while True:

	if i >= len(line):
		f.close()
		exit(0)

	currline = line[i]
	cmd = get_command(line[i])
	if cmd == ";":
		pass
	elif cmd == "MOV":
		second: str = currline.split(" ")[1]
		try:
			third: str = currline.split(" ")[2]
		except:
			print("Missing target\nline:", i+1, "\n-----------------------\n%s-----------------------" % line[i])
			f.close()
			exit(1)
		MOV(second, third, i)
	elif cmd == "ADD":
		second: str = currline.split(" ")[1]
		ADD(second, i)
	elif cmd == "SUB":
		second: str = currline.split(" ")[1]
		SUB(second, i)
	elif cmd == "INP":
		second: str = currline.split(" ")[1]
		INP(second)
	elif cmd == "LAB":
		while True:
			currline = line[i]
			if currline.split(" ")[0] == "LBD":
				break

			i += 1
	elif cmd == "JMP":
		second: str = currline.split(" ")[1]
		JMP(second)
	elif cmd == "JEZ":
		second: str = currline.split(" ")[1]
		JEZ(second)
	elif cmd == "JNZ":
		second: str = currline.split(" ")[1]
		JNZ(second)
	elif cmd == "JGZ":
		second: str = currline.split(" ")[1]
		JGZ(second)
	elif cmd == "JLZ":
		second: str = currline.split(" ")[1]
		JLZ(second)
	elif cmd == "JRO":
		second: str = currline.split(" ")[1]
		JRO(int(second))
	elif cmd == "SAV":
		SAV()
	elif cmd == "SWP":
		SWP()
	elif cmd == "LBD":
		pass
	elif cmd in "\n":
		pass
	elif cmd in " ":
		pass
	elif cmd in "\t":
		pass
	else:
		print("Command not found\nline:", i+1)
		f.close()
		exit(1)

	i += 1