#!/usr/bin/env python3.8
"""
TIS-100 like assembly interpreter
made in python
"""

from sys import exit, argv, stderr, platform
from os.path import isfile
from os import system
from time import time
from random import randint

labels = {}
variables = {
	"ACC": 0,
	"BAK": 0,
	"RANDOM": randint(0, 32767)
}
current_line = 0

if len(argv) < 2:
	print(argv[0], "[FILE]")
	exit(1)

if not isfile(argv[1]):
	print("File:", argv[1], "\nNot a file or file not found")
	exit(1)

f = open(argv[1], "r")

# Functions to add the logic of the commands
def MOV(src, dst, lineno): # If the variable does not exists it creates one
	isVar = False
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
			isVar = True
			variables[dst] = str(variables[src])
		else:
			variables[dst] = eval(src)

	if isVar:
		try:
			variables[src]
		except KeyError:
			print("Variable:", src, "\nnot found\nline:", lineno+1)
			exit(1)

	if dst == "OUT":
		if src[0] == "\"" or src[0] == "'":
			string = False
		else:
			string = True

		src = src.strip("\"'")

		if string:	
			if src.isalpha():
				print(variables[src], end="")
			else:
				print(src, end="")
		else:
			print(src, end="")
	elif dst == "ERR":
		printTime = False
		if src[0] == "\"" or src[0] == "'":
			string = False
		else:
			string = True

		src = src.strip("\"'")

		if string:	
			if src.isalpha():
				stderr.write(src)
			else:
				stderr.write(src)
		else:
			stderr.write(src)


def ADD(val, lineno):
	val = val.strip("\n")
	if val[0] == "\"" or val[0] == "'" or val[-1] == "\"" or val[-1] == "'":
		print("String not allowed in add command\nline:", lineno+1)
		f.close()
		exit(1)

	if type(variables["ACC"]) is str:
		variables["ACC"] = 0

	variables["ACC"] = int(variables["ACC"])
	if val.isalpha():
		variables["ACC"] += int(variables[val])
	else:
		variables["ACC"] += int(val)

def SUB(val, lineno):
	val = val.strip("\n")
	if val[0] == "\"" or val[0] == "'" or val[-1] == "\"" or val[-1] == "'":
		print("String not allowed in sub command\nline:", lineno+1)
		f.close()
		exit(1)

	variables["ACC"] = int(variables["ACC"])
	if type(variables["ACC"]) is str:
		variables["ACC"] = 0

	variables["ACC"] = int(variables["ACC"])
	if val.isalpha():
		variables["ACC"] -= int(variables[val])
	else:
		variables["ACC"] -= int(val)

def INP(var):
	var = var.strip("\n")
	variables[var] = input()

def LAB(label, lineno): # Declares a label with the value as the line number
	label = label.strip("\n")
	labels[label] = lineno

# These that jump gets the value of the label name provided
# And sets the current line being parsed to the label line
def JMP(label):
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)
		
	global i
	label = label.strip("\n")
	i = labels[label]

def JEZ(label):
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)
		
	if int(variables["ACC"]) == 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JNZ(label):
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)
		
	if int(variables["ACC"]) != 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JGZ(label):
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)
		
	if int(variables["ACC"]) > 0:
		global i
		label = label.strip("\n")
		i = labels[label]

def JLZ(label):
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)

	if int(variables["ACC"]) < 0:
		global i
		label = label.strip("\n")
		i = labels[label]

# Jumps a amount of lines in the offset variable
# By setting the current line being parsed
# If the value is negative it jumps back
def JRO(offset):
	global i
	i += offset

def SAV():
	variables["ACC"] = variables["BAK"]

def SWP():
	ACC = variables["ACC"]
	BAK = variables["BAK"]
	variables["ACC"] = BAK
	variables["BAK"] = ACC

def MUL(val, lineno):
	val = val.strip("\n")
	if val[0] == "\"" or val[0] == "'" or val[-1] == "\"" or val[-1] == "'":
		print("String not allowed in mul command\nline:", lineno+1)
		f.close()
		exit(1)

	variables["ACC"] = int(variables["ACC"])
	if type(variables["ACC"]) is str:
		variables["ACC"] = 0

	variables["ACC"] = int(variables["ACC"])
	if val.isalpha():
		variables["ACC"] *= int(variables[val])
	else:
		variables["ACC"] *= int(val)

def DIV(val, lineno):
	val = val.strip("\n")
	if val[0] == "\"" or val[0] == "'" or val[-1] == "\"" or val[-1] == "'":
		print("String not allowed in div command\nline:", lineno+1)
		f.close()
		exit(1)

	variables["ACC"] = int(variables["ACC"])
	if type(variables["ACC"]) is str:
		variables["ACC"] = 0

	variables["ACC"] = int(variables["ACC"])
	if val.isalpha():
		variables["ACC"] /= int(variables[val])
	else:
		variables["ACC"] /= int(val)

def TET(txt, txt2, label, lineno):
	label = label.strip("\n")
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)

	global i
	try:
		variables[txt]
	except KeyError:
		print("Variable:", txt, "\nNot found\nline:", lineno+1)
		exit(1)

	try:
		variables[txt2]
	except KeyError:
		print("Variable:", txt2, "\nNot found\nline:", lineno+1)
		exit(1)

	if variables[txt] == variables[txt2]:
		i = labels[label]

def TNT(txt, txt2, label, lineno):
	label = label.strip("\n")
	try:
		labels[label]
	except KeyError:
		print("Label:", label, "\nNot found\nline:", lineno+1)
		exit(1)

	global i
	try:
		variables[txt]
	except KeyError:
		print("Variable:", txt, "\nNot found\nline:", lineno+1)
		exit(1)

	try:
		variables[txt2]
	except KeyError:
		print("Variable:", txt2, "\nNot found\nline:", lineno+1)
		exit(1)

	if variables[txt] != variables[txt2]:
		i = labels[label]

def CLR():
	if platform == "win32" or platform == "cygwin" or platform == "msys":
		system("cls")
	else:
		system("clear")

def NEG():
	acc = eval("-" + str(variables["ACC"]))
	variables["ACC"] = int(acc)

def get_command(line: str):
		first_word = line.split(" ")[0]
		first_word = first_word.split("\n")[0]
		return first_word

start_time = time()
line = f.readlines()

i = 0
# Parse file
while True: # This loop adds the labels to the labels dictionary and the value is the line number

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
		elapsed_time = time() - start_time
		print("\n-----------------------\nProgram closed in:", str(elapsed_time)[0:7])
		f.close()
		exit(0)

	currline = line[i]
	cmd = get_command(line[i])
	if line[i].startswith(";"):
		pass
	elif cmd == "MOV":
		# Made this so we can use spaces on the mov command
		scdi = 0
		for l in currline:
			if l == "|":
				second: str = currline[4:scdi-1]
				dstnum = scdi + 2
			scdi += 1
		try:
			third: str = currline[dstnum:]
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
		labcount = 0
		while True:
			if i >= len(line):
				break
			currline = line[i]
			first_word = currline.split(" ")
			first_word = currline.split("\n")

			if first_word[0] == "LAB":
				labcount += 1
			elif first_word[0] == "LBD" and labcount != 0:
				labcount -= 1
			elif first_word[0] == "LBD" and labcount == 0:
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
	elif cmd == "NWL":
		print()
	elif cmd == "EXT":
		second: str = currline.split(" ")[1]
		second = second.strip("\n")
		exit(eval(second))
	elif cmd == "TET":
		second: str = currline.split(" ")[1]
		third: str = currline.split(" ")[2]
		fourth: str = currline.split(" ")[3]
		TET(second, third, fourth, i)
	elif cmd == "TNT":
		second: str = currline.split(" ")[1]
		third: str = currline.split(" ")[2]
		fourth: str = currline.split(" ")[3]
		TNT(second, third, fourth, i)
	elif cmd == "CLR":
		CLR()
	elif cmd == "NEG":
		NEG()
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
	variables["RANDOM"] = randint(0, 32767)
