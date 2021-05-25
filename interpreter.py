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
#--- Set the extended commands status
extended = 1
#--- Initialize variables
lines = []
variables = {'global':'0'}
functions = {}
nextfunction = ''
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
		#--- Manual: How to define a function?
		# lines = ['value name', 'define', 'defined', 'value 0', 'jump']
		#--- Manual: MATH variable input order explanation
		# lines = ['value 1', 'value 2', 'value 3', 'math A+B+C', 'print', 'value 0', 'jump']
		#--- Manual: Naming of functions 
		# lines = ['value hi how are you', 'define', 'defined', 'value 0', 'jump']
		# lines = ['value 1', 'value 2', 'math A+B', 'define', 'defined', 'value 0', 'jump']
		# lines = ['input', 'define', 'defined', 'value 0', 'jump']
		#--- Manual: Undefined functions 
		# lines = ['value hi', 'call', 'value hi', 'define', 'defined', 'value hi', 'call', 'value 0', 'jump']
		#--- Manual: Why CALL? 
		# lines = ['value 3', 'define', 'defined', 'value 1', 'value 2', 'math A+B', 'call', 'value 0', 'jump']
		#--- Manual: Why LOOK? 
		# lines = ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3', 'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8', 'value line 9', 'value line 10', 'value 12', 'look', 'value 2', 'math A+B', 'print', 'value 0', 'jump']
		# lines = ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3', 'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8', 'value line 9', 'value line 10', 'math K', 'print', 'value 0', 'jump']
		#--- Manual: Conditional jumps? 
		# lines = ['value loop', 'define', 'value hi', 'print', 'globalr', 'math A+1', 'globalw', 'defined', 'value loop', 'call', 'globalr', 'math A>3', 'math (A==0) * 5 + (A!=0) * (-1)', 'jump', 'value 0', 'jump']
		#--- Manual: What can we do with this? 
		# lines = ['value 1', 'define', 'value 1', 'print', 'value 1', 'call', 'defined', 'input', 'call', 'value 0', 'print', 'value 0', 'jump']
		# lines = ['value step', 'define', 'globalr', 'math A%2 * (3*A+1) + (A%2==0) * A/2', 'globalw', 'globalr', 'print', 'defined', 'value enter an arbitrary integer', 'print', 'input', 'globalw', 'globalr', 'print', 'math (B!=1) * (-1) + (B==1) * (-3)', 'jump', 'value step', 'call', 'globalr', 'math (A!=1) * 4 + (A==1) * (-1)', 'jump', 'value 0', 'jump']
		#--- Extended manual: CALL
		# lines = ['value hi', 'globalw hello', 'value hello', 'define', 'globalr A', 'print', 'defined', 'value hello', 'call A', 'globalr A', 'print', 'value 0', 'jump']
		#--- Custom input parser
		if lines:
			raise
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
			handler(lines, pointer, 'maininterpretercall')
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
def handler(lines, pointer, infunction):
	#--- Import global variables
	global extended
	global variables
	global functions
	global call_pointer
	global pointerset
	global alphabet
	global nextfunction
	#--- Update executed instruction
	value = lines[pointer]
	#--- CALL command definition
	if value.startswith('call'):
		variables[pointer] = 0
		#--- Toggle extended features
		if extended == 1:
			#--- Sanity check for only uppercase letters
			var = value[5:].upper()
			#--- Loop for replacing variables
			for index, letter in enumerate(alphabet):
				#--- Sanity check for accessing a non-existing variable
				try:
					if infunction == 'maininterpretercall':
						if letter in var:
							variables[letter] = variables[pointer-1-index]
					else:
						if letter in var:
							if not letter in variables:
								variables[letter] = variables[pointer-1-index]
				except Exception:
					pass
		funname = str(variables[pointer-1])
		#--- If called from within a function of the same name, reset the function - infinite recursion
		if call_pointer != 0:
			if funname == infunction:
				variables[pointer] = 1
				call_pointer = 0
				return
			else:
				call_pointer = 2147483647
				nextfunction = funname
				return
		#--- Only call if function exists
		if funname in functions:
			while True:
				variables[pointer] = 1
				run = functions[funname]
				#--- Sanity check for empty functions
				while len(run) > 0:
					handler(run, call_pointer, funname)
					#--- Slowdown for functions to not hang the device
					sleep(0.02)
					#--- Update the function pointer
					if call_pointer < len(run)-1:
						call_pointer += 1
					else:
						call_pointer = 0
						break
				#--- Jump to another function if called
				if not nextfunction == '':
					funname = nextfunction
					nextfunction = ''
				else:
					for index, letter in enumerate(alphabet):
						variables.pop(letter, None)
					break
			#--- Delete temporary variables
			funname = None
			del funname
			run = None
			del run
	#--- DEFINE command definition
	elif value.startswith('define'):
		#--- Sanity check for non-opened functions 
		if value.startswith('defined'):
			del lines[pointer]
			return
		variables[pointer] = 0
		nodefine = 0
		funname = str(variables[pointer-1])
		#--- Sanity check for overwriting functions
		if funname in functions:
			nodefine = 1 # Comment this to enable overwriting functions
			if not nodefine == 1:
				functions.pop(funname, None)
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
		#--- Add function to dictionary if defining
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
	#--- GLOBALW command definition
	elif value.startswith('globalw'):
		variables[pointer] = 0
		access = 'global'
		if extended == 1:
			access = value[8:]
			#--- Loop for replacing variables
			for index, letter in enumerate(alphabet):
				if not infunction == 'maininterpretercall':
					if letter in access:
						if letter in variables:
							access = access.replace(letter, str(variables[letter]))
			if access == '':
				access = 'global'
		#--- Sanity check for accessing a non-existing variable
		try:
			variables[access] = variables[pointer-1]
			variables[pointer] = 1
		except Exception:
			return
		#--- Delete temporary variable
		access = None
		del access
	#--- GLOBALR command definition
	elif value.startswith('globalr'):
		access = 'global'
		if extended == 1:
			access = value[8:]
			#--- Loop for replacing variables
			for index, letter in enumerate(alphabet):
				if not infunction == 'maininterpretercall':
					if letter in access:
						if letter in variables:
							access = access.replace(letter, str(variables[letter]))
		if access == '':
			access = 'global'
		try:
			variables[pointer] = variables[access]
		except Exception:
			variables[pointer] = 0
		#--- Delete temporary variable
		access = None
		del access
	#--- INPUT command definition
	elif value.startswith('input'):
		variables[pointer] = input(': ')
		#--- Sanity check for empty input
		if variables[pointer] == '':
			variables[pointer] = 0
	#--- JUMP command definition
	elif value.startswith('jump'):
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
			return
	#--- LOOK command definition
	elif value.startswith('look'):
		variables[pointer] = 0
		#--- Sanity check for accessing a non-existing variable
		try:
			variables[pointer] = variables[pointer-variables[pointer-1]]
		except Exception:
			return
	#--- MATH command definition
	elif value.startswith('math'):
		variables[pointer] = 0
		equation = value[5:]
		
		#--- Variable assigning loop
		for index, letter in enumerate(alphabet):
			#--- Sanity check for accessing a non-existing variable
			try:
				#--- Sanity check for only uppercase letters
				equation = equation.upper()
				if letter in equation:
					if extended == 1:
						if infunction == 'maininterpretercall':
							equation = equation.replace(letter, str(variables[pointer-1-index]))
						else:
							try:
								equation = equation.replace(letter, str(variables[letter]))
							except Exception:
								equation = equation.replace(letter, str(variables[pointer-1-index]))
					else:
						equation = equation.replace(letter, str(variables[pointer-1-index]))
			except Exception:
				#--- Delete the equation if wrong input
				equation = None
				del equation
				return
		#--- This shouldn't contain any letters because of the loop above so it's pretty safe
		variables[pointer] = int(eval(equation))
		#--- Delete temporary variable
		equation = None
		del equation
	#--- PRINT command definition
	elif value.startswith('print'):
		variables[pointer] = 0
		#--- Sanity check for accessing a non-existing variable
		try:
			print(str(variables[pointer-1]))
			variables[pointer] = 1
		except Exception:
			return
	#--- VALUE command definition
	elif value.startswith('value'):
		variables[pointer] = 0
		var = value[6:]
		for index, letter in enumerate(alphabet):
			#--- Sanity check for accessing a non-existing variable
			try:
				if letter in var:
					if extended == 1:
						if infunction == 'maininterpretercall':
							pass
						else:
							try:
								var = var.replace(letter, str(variables[letter]))
							except Exception:
								pass
			except Exception:
				pass
		#--- Conversion to int if possible
		try:
			int(var)
			variables[pointer] = int(var)
		except ValueError:
			variables[pointer] = str(var)
		#--- Delete temporary variable
		var = None
		del var
	#--- Sanity check for wrong command
	else:
		input('--- Unrecognized command ---')
		halt()
#--- Sanity check for importing
if __name__=='__main__':
	interpreter()