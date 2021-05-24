#--- Make program able to stop at any time by calling exit()
from sys import exit as halt
#--- Make CALL take time before recursing infinitely
from time import sleep
#--- Shortcut for alphabet array
from string import ascii_uppercase as letters
alphabet = list(letters)
#--- Enable ANSI color support in Windows
from os import system as color
color('')	
#--- Initialize variables
lines = []
variables = {'g':'0'}
functions = {}
pointer = 0
call_pointer = 0
pointerset = -1
#--- The interpreter wrapper
def interpreter():
	#--- Input parser
	try:
		#--- Import global variable
		global lines
		print('Input the\u001b[31;1m While(true){\u001b[0m code one instruction per line')
		print('Uses eval() in MATH commands, make sure to\u001b[31;1m sanitize\u001b[0m it (should error out anyway, but just in case)')
		print()
		#----- Test programs (uncomment to overwrite custom parser)
		#--- Manual: How to end a program?
		# lines = ['value 0', 'jump']
		# raise
		#--- Manual: MATH variable input order explanation
		# lines = ['value 1', 'value 2', 'value 3', 'math A+B+C', 'print', 'value 0', 'jump']
		# raise
		#--- Manual: Naming of functions 
		# lines = ['value hi', 'define', 'defined', 'value 1', 'value 2', 'math A+B', 'define', 'defined', 'value 0', 'jump']
		# raise
		#--- Manual: Undefined functions 
		# lines = ['value hi', 'call', 'value hi', 'define', 'defined', 'value hi', 'call', 'value 0', 'jump']
		# raise
		#--- Manual: Why CALL? 
		# lines = ['value 3', 'define', 'defined', 'value 1', 'value 2', 'math A+B', 'call', 'value 0', 'jump']
		# raise
		#--- Manual: Why LOOK? 
		# lines = ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3', 'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8', 'value line 9', 'value line 10', 'value 12', 'look', 'value 2', 'math A+B', 'print', 'value 0', 'jump']
		# raise
		#--- Manual: Conditional jumps? 
		# lines = ['value loop', 'define', 'value hi', 'print', 'globalr', 'math A+1', 'globalw', 'defined', 'value loop', 'call', 'globalr', 'math A>3', 'math 5-6*A', 'jump', 'value 0', 'jump']
		# raise
		#--- Manual: What can we do with this? 
		# lines = ['value 1', 'define', 'value 1', 'print', 'value 1', 'call', 'defined', 'input', 'call', 'value 0', 'print', 'value 0', 'jump']
		# raise
		# Manual: How do you know this is Turing-complete?
		# lines = ['value step', 'define', 'globalr', 'math (A%2==1)*((3*A+1)/2)+(A%2==0)*(A/2)', 'globalw', 'globalr', 'print', 'defined', 'value enter_an_arbitrary_integer', 'print', 'input', 'globalw', 'math (B!=1)*(-1)+(B==0)*(-3)', 'jump', 'value step', 'call', 'globalr', 'math (A==1)*(-1)+(A!=1)*(4)', 'jump', 'value 0', 'jump']
		# raise
		#--- Custom input parser
		custom = 0
		while True:
			line = input().strip()
			if line == '':
				raise
			lines.append(line)
	#--- Input handler
	except Exception:
		#--- Clear temporary variables from the parser
		line = None
		del line
		# --- Print all commands with their indices for preset programs
		try:
			custom += 1
			custom = None
			del custom
		except Exception:
			print('--- Preset program ---')
			for v in lines:
				print(v)
			print()
		#--- Import global variable
		global pointer
		#--- Sanity check for empty programs
		while not len(lines) == 0:
			#--- Import global variable
			global pointerset
			#--- Call the handler
			handler(lines, pointer)
			#--- Update the main pointer
			if pointerset != -1:
				pointer = pointerset
				pointerset = -1
			elif pointer < len(lines)-1:
				pointer += 1
			else:
				#--- Reset pointer if at the end
				pointer = 0
#--- The handler function that actually interprets
def handler(lines, pointer):
	#--- Import global variables
	global variables
	global functions
	global call_pointer
	global pointerset
	global alphabet
	#--- Update executed instruction
	value = lines[pointer]
	#--- Find command in list
	if 'call' in value:
		variables[pointer] = 0
		#--- If call within a function, reset the function - infinite recursion
		if call_pointer != 0:
			variables[pointer] = 1
			call_pointer = 0
			return
		funname = str(variables[pointer-1])
		#--- Only call if function exists
		if funname in functions:
			variables[pointer] = 1
			run = functions[funname]
			#--- Sanity check for empty functions
			while not len(run) == 0:
				handler(run, call_pointer)
				#--- Slowdown for functions to not hang the device
				sleep(0.02)
				#--- Update the function pointer
				if call_pointer < len(run)-1:
					call_pointer += 1
				else:
					call_pointer = 0
					break
			#--- Delete temporary variables
			funname = None
			del funname
			run = None
			del run
	elif 'define' in value:
		#--- Sanity check for non-opened functions 
		if 'defined' in value:
			del lines[pointer]
			return
		variables[pointer] = 0
		nodefine = 0
		funname = str(variables[pointer-1])
		#--- Sanity check for overwriting functions
		if funname in functions:
			#--- Switch comments to enable overwriting functions
			nodefine = 1
			# functions.pop(funname, None)
		commands = []
		#--- Move to the function name and delete it, as well as DEFINE
		pointer -= 1
		del lines[pointer]
		del lines[pointer]
		#--- Loop for removing the function from the main program and adding to the function dictionary
		while True:
			#--- Don't append DEFINED to the function
			if lines[pointer] == 'defined':
				del lines[pointer]
				break
			commands.append(lines[pointer])
			del lines[pointer]
		#--- Add function to dictionary
		if not nodefine == 1:
			functions[funname] = commands
			variables[pointer] = 1
			#--- Update pointer to the correct place
			pointerset = pointer
		#--- Delete temporary variables
		funname = None
		del funname
		commands = None
		del commands
		nodefine = None
		del nodefine
	elif 'globalw' in value:
		variables[pointer] = 0
		#--- Sanity check for accessing a non-existing variable
		try:
			variables['g'] = variables[pointer-1]
			variables[pointer] = 1
		except Exception:
			pass
	elif 'globalr' in value:
		variables[pointer] = variables['g']
	elif 'input' in value:
		variables[pointer] = input(': ')
		#--- Sanity check for empty input
		if variables[pointer] == '':
			variables[pointer] = 0
	elif 'jump' in value:
		variables[pointer] = 0
		#--- Sanity check for accessing a non-existing variable
		try:
			if variables[pointer-1] == 0:
					variables[pointer] = 1
					input('--- Pause for running pythonw ---')
					halt()
			else:
				pointerset = pointer-variables[pointer-1]
				variables[pointer] = 1
		except Exception:
			pass
	elif 'look' in value:
		variables[pointer] = 0
		#--- Sanity check for accessing a non-existing variable
		try:
			variables[pointer] = variables[pointer-variables[pointer-1]]
		except Exception:
			pass
	elif 'math' in value:
		variables[pointer] = 0
		equation = value.split(' ')[1]
		#--- Variable assigning loop
		for index, letter in enumerate(alphabet):
			#--- Sanity check for accessing a non-existing variable
			try:
				if letter in equation:
					equation = equation.replace(letter, str(variables[pointer-1-index]))
			except Exception:
				return
		#--- This shouldn't contain any letters because of the loop so it's pretty safe
		equation = eval(equation)
		#--- Covert truthiness to correct form
		if equation == 'True':
			equation = 1
		elif equation == 'False':
			equation = 0
		variables[pointer] = int(equation)
		#--- Delete temporary variable
		equation = None
		del equation
	elif 'print' in value:
		variables[pointer] = 0
		#--- Sanity check for accessing a non-existing variable
		try:
			print(str(variables[pointer-1]))
			variables[pointer] = 1
		except Exception:
			pass
	elif 'value' in value:
		variables[pointer] = 0
		var = value.split()[1]
		#--- Conversion to int if possible
		try:
			int(var)
			variables[pointer] = int(var)
		except ValueError:
			variables[pointer] = str(var)
		#--- Delete temporary variable
		var = None
		del var
	#--- Sanity check for random input
	else:
		input('--- Unrecognized command ---')
		halt()
#--- Sanity check for importing
if __name__=='__main__':
	interpreter()