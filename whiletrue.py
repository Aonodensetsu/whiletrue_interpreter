#--- Initialize command input
commands = []

#--- Set the extended commands status
extendedFeatures = 1

#--- Allow overwriting previously declared functions
overwriteFunctions = 0

#--- Change the input style from one command per line to commands separated by semicolon (for sharing programs)
briefInput = 0

#----- Test programs (uncomment to overwrite custom parser)

#--- Manual: How to end a program?
# commands = ['value 0', 'jump']

#--- Manual: How to define a function?
# commands = ['value name', 'define', 'defined', 'value 0', 'jump']

#--- Manual: MATH variable input order explanation
# commands = ['value 1', 'value 2', 'value 3', 'math A+B+C', 'print', 'value 0', 'jump']

#--- Manual: Naming of functions 
# commands = ['value hi how are you', 'define', 'defined', 'value 0', 'jump']
# commands = ['value 1', 'value 2', 'math A+B', 'define', 'defined', 'value 0', 'jump']
# commands = ['input', 'define', 'defined', 'value 0', 'jump']

#--- Manual: Undefined functions 
# commands = ['value hi', 'call', 'value hi', 'define', 'value hi', 'print', 'defined', 'value hi', 'call', 'value 0', 'jump']

#--- Manual: Recursion
# commands = ['value hi', 'define', 'value hi', 'print', 'value hi', 'call', 'defined', 'value hi', 'call', 'value 0', 'jump']
# commands = ['value hi', 'define', 'value hi', 'print', 'value hello', 'call', 'defined', 'value hello', 'define', 'value hello', 'print', 'value hi', 'call', 'defined', 'value hi', 'call', 'value 0', 'jump']

#--- Manual: Why CALL? 
# commands = ['value 3', 'define', 'defined', 'value 1', 'value 2', 'math A+B', 'call', 'value 0', 'jump']

#--- Manual: Why LOOK? 
# commands = ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3', 'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8', 'value line 9', 'value line 10', 'value 12', 'look', 'value 2', 'math A+B', 'print', 'value 0', 'jump']
# commands = ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3', 'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8', 'value line 9', 'value line 10', 'math K', 'print', 'value 0', 'jump']

#--- Manual: Conditional jumps? 
# commands = ['value loop', 'define', 'value hi', 'print', 'globalr', 'math A+1', 'globalw', 'defined', 'value loop', 'call', 'globalr', 'math A>3', 'math (A==0) * 5 + (A!=0) * (-1)', 'jump', 'value 0', 'jump']

#--- Manual: What can we do with this? 
# commands = ['value 1', 'define', 'value 1', 'print', 'value 1', 'call', 'defined', 'input', 'call', 'value 0', 'print', 'value 0', 'jump']
# commands = ['value step', 'define', 'globalr', 'math A%2 * (3*A+1) + (A%2==0) * A/2', 'globalw', 'globalr', 'print', 'defined', 'value enter an arbitrary integer', 'print', 'input', 'globalw', 'globalr', 'print', 'math (B!=1) * (-1) + (B==1) * (-3)', 'jump', 'value step', 'call', 'globalr', 'math (A!=1) * 4 + (A==1) * (-1)', 'jump', 'value 0', 'jump']

#--- Extended manual: CALL
# commands = ['value hi', 'globalw hello', 'value hello', 'define', 'globalr A', 'print', 'defined', 'value hello', 'call A', 'globalr A', 'print', 'value 0', 'jump']
# commands = ['value hello', 'define', 'value hi', 'globalw A', 'globalr A', 'print', 'defined', 'value hi', 'value hello', 'call B', 'value 0', 'jump']

#--------------------------------------------------------------------------------------------------------------------------		
#-------------------------------------------------DEVELOPER-SPACE----------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

#--- Make program able to stop at any time by calling exit()
from sys import exit

#--- Make CALL take time before recursing infinitely
from time import sleep

#--- Shortcut for alphabet array
from string import ascii_uppercase
alphabet = list(ascii_uppercase)

#--- Enable ANSI color support in Windows
from os import system
system('')

#--- Initialize variables
executeArray = ['_main']
pointerArray = [0]
variables = {'_global': 0}
functions = {}
custom = 0

#--- Show beginning message
print('Input the\u001b[31;1m While(true){\u001b[0m code one instruction per line')
print('Uses eval() in MATH commands, make sure to\u001b[31;1m sanitize\u001b[0m it (it removes all letters so should be pretty safe)')
print()

#--- Custom input parser
if not briefInput:
	if not commands:
		custom = 1
		while True:
			command = input().strip()
			if command == '':
				break
			commands.append(command)
else:
	commands = []
	for i in input().strip().split(';'):
		if i != '':
			commands.append(i.strip())

#--- Assign commands to the _main function
functions['_main'] = commands

#--- Initialize variables for main function
for i, v in enumerate(commands):
	variables['_main_'+str(i)] = 0
	# --- Print all commands for presets
	if not custom:
		print(v)
if not custom:
	print()

#--- Delete temporary variables
commands = None
del commands
command = None
del command
custom = None
del custom

#--- Handle interpretation
def interpreter():
	
	#--- Import global variables
	global executeArray
	global pointerArray
	global functions
	global variables
	global alphabet
	global extendedFeatures
	global overwriteFunctions
	
	#--- Get current pointer, function and its commands
	functionname = executeArray[-1]
	pointer = pointerArray[-1]
	commands = functions[functionname]
	
	#--- Exit function on end or repeat main program
	if pointer >= len(commands):
		if functionname == '_main':
			pointerArray[-1] = 0
			return
		else:
			for i, v in enumerate(alphabet):
				if '_'+v in variables:
					variables.pop('_'+v)
			del executeArray[-1]
			del pointerArray[-1]
			return
	
	#--- Get current command	
	command = commands[pointer]

	#--- CALL command definition
	if command.startswith('call'):
		val = command[5:]
		letters = []
		#--- Extended functionality (pass variables)
		if extendedFeatures == 1:
			#--- Sanity check for only uppercase letters
			val = val.upper()
			#--- Loop for replacing variables
			for i, v in enumerate(alphabet):
				#--- Sanity check for accessing a non-existing variable
				try:
					if v in val:
						letters.append(variables[functionname+'_'+str(pointer-i-1)])
				except Exception:
					print('\u001b[31;1mException\u001b[0m while handling variables in CALL')
					input('Accessed a non-existing variable')
					exit()
			else:
				for i, v in enumerate(alphabet):
					if not letters:
						break
					variables['_'+v] = letters[0]
					letters = letters[1:]	
		else:
			if val:
				print('\u001b[31;1mException\u001b[0m while handling syntax in CALL')
				input('Extended features not enabled, CALL does not take arguments')
				exit()
		
		funname = str(variables[functionname+'_'+str(pointer-1)])
		
		#--- Do not allow _ (which is used internally) to be in input
		if '_' in funname:
			print('\u001b[31;1mException\u001b[0m while handling input in CALL')
			input('Value cannot contain an underscore')
			exit()
		
		#--- If function exists, call it
		if funname in functions:
			#--- If the function you're calling was called previously
			#--- And has not ended (still in executeArray)
			#--- Then delete everything after that function in executeArray
			#--- Since functions are calling themselves in a loop
			if funname in executeArray:
				variables[functionname+'_'+str(pointer)] = 1
				if funname != functionname:
					pointerArray = pointerArray[:executeArray.index(funname)+1]
					executeArray = executeArray[:executeArray.index(funname)+1]
				#--- Reset the pointer of the called function to 0
				pointerArray[-1] = 0
			else:
				variables[functionname+'_'+str(pointer)] = 1
				#--- Update pointer for this function to not get stuck on CALL
				pointerArray[-1] += 1
				
				#--- Add the function to the queue
				executeArray.append(funname)
				pointerArray.append(0)
			#--- Delay to not spam in case of infinite recursion
			sleep(0.02)
			return
		
		#--- Delete temporary variables
		funname = None
		del funname
		val = None
		del val
	
	#--- DEFINE command definition
	elif command.startswith('define'):
		if command.startswith('defined'):
			variables[functionname+'_'+str(pointer)] = 1
			pointerArray[-1] += 1
			return
		funname = str(variables[functionname+'_'+str(pointer-1)])
		dpointer = str(pointer)
		
		#--- Do not allow _ (which is used internally) to be in input
		if '_' in funname:
			print('\u001b[31;1mException\u001b[0m while handling input in DEFINE')
			input('Value cannot contain an underscore')
			exit()
		
		#--- Sanity check for overwriting functions
		if funname in functions:
			if overwriteFunctions == 0:
				print('\u001b[31;1mException\u001b[0m while handling input in DEFINE')
				input('Overwriting functions is not enabled')
				exit()
		
		#--- Add commands
		lines = []
		while True:
			pointer += 1
			pointerArray[-1] += 1
			if commands[pointer] == 'defined':
				variables[functionname+'_'+str(pointer)] = 1
				break
			lines.append(commands[pointer])
		
		#--- Sanity check for overwriting functions
		if overwriteFunctions != 0:
			functions.pop(funname, None)
			functions[funname] = lines
			variables[functionname+'_'+dpointer] = 1
		else:
			functions[funname] = lines
			variables[functionname+'_'+dpointer] = 1	
				
		#--- Delete temporary variables
		funname = None
		del funname
		nodefine = None
		del nodefine
		dpointer = None
		del dpointer
		lines = None
		del lines
	
	#--- GLOBALW command definition
	elif command.startswith('globalw'):
		access = '_global'
		
		#--- Extended functionality (custom global variables)
		if extendedFeatures == 1:
			access = command[8:]
			
			#--- Do not allow _ (which is used internally) to be in input
			if '_' in access:
				print('\u001b[31;1mException\u001b[0m while handling input in GLOBALR (extended functionality)')
				input('Value cannot contain an underscore')
				exit()
			
			#--- Replacing variables (extended functionality of CALL)
			if functionname != '_main':
				for i, v in enumerate(alphabet):				
					if v in access:
						#--- Sanity check for accessing a non-existing variable
						try:
							access = access.replace(v, str(variables['_'+v]))
						except Exception:
							pass
			
			#--- If extended features are enabled but not used, reset to default
			if access == '':
				access = '_global'
		
		else:
			if command[8:] != '':
				print('\u001b[31;1mException\u001b[0m while handling syntax in GLOBALW')
				input('Extended features not enabled, GLOBALW does not take arguments')
				exit()
		
		#--- Sanity check for accessing a non-existing variable
		try:
			variables[access] = variables[functionname+'_'+str(pointer-1)]
		except Exception:
			print('\u001b[31;1mException\u001b[0m while handling variables in GLOBALW')
			input('Accessed a non-existing variable')
			exit()
		
		#--- Delete temporary variables
		access = None
		del access
		
	#--- GLOBALR command definition
	elif command.startswith('globalr'):
		access = '_global'
		
		#--- Extended functionality (custom global variables)
		if extendedFeatures == 1:
			access = command[8:]
			
			#--- Do not allow _ (which is used internally) to be in input
			if '_' in access:
				print('\u001b[31;1mException\u001b[0m while handling input in GLOBALR (extended functionality)')
				input('Value cannot contain an underscore')
				exit()
			
			#--- Replacing variables (extended functionality of CALL)
			if functionname != '_main':
				for i, v in enumerate(alphabet):
					if v in access:
						#--- Sanity check for accessing a non-existing variable
						try:
							access = access.replace(v, str(variables['_'+v]))
						except Exception:
							pass
			
			#--- If extended features are enabled but not used, reset to default
			if access == '':
				access = '_global'
		
		else:
			if command[8:] != '':
				print('\u001b[31;1mException\u001b[0m while handling syntax in GLOBALR')
				input('Extended features not enabled, GLOBALR does not take arguments')
				exit()
		
		#--- Sanity check for accessing a non-existing variable
		try:
			variables[functionname+'_'+str(pointer)] = variables[access]
		except Exception:
			print('\u001b[31;1mException\u001b[0m while handling variables in GLOBALR')
			input('Accessed a non-existing variable')
			exit()
		
		#--- Delete temporary variables
		access = None
		del access
		
	#--- INPUT command definition
	elif command.startswith('input'):
		val = input(': ')
		
		#--- Do not allow _ (which is used internally) to be in input
		if '_' in val:
				print('\u001b[31;1mException\u001b[0m while handling input in INPUT')
				input('Value cannot contain an underscore')
				exit()
		
		#--- Empty string is not a valid input
		if val != '':
			variables[functionname+'_'+str(pointer)] = val
		
		#--- Delete temporary variables
		val = None
		del val
	
	#--- JUMP command definition
	elif command.startswith('jump'):
		#--- Sanity check for random values
		try:
			val = variables[functionname+'_'+str(pointer-1)]
			val = int(val)
		except ValueError:
			print('\u001b[31;1mException\u001b[0m while handling variables in JUMP')
			input('Can only jump to a number')
			exit()
		#--- Sanity check for accessing a non-existing variable
		try:
			if val == 0:
				variables[functionname+'_'+str(pointer)] = 1
				input('--- Pause for running pythonw ---')
				exit()
			else:
				pointerArray[-1] = pointer-val
				variables[functionname+'_'+str(pointer)] = 1
				val = None
				del val
				return
		except Exception:
			print('\u001b[31;1mException\u001b[0m while handling variables in JUMP')
			input('Accessed a non-existing variable')
			exit()
		
		#--- Delete temporary variables
		val = None
		del val
	
	#--- LOOK command definition
	elif command.startswith('look'):
		#--- Sanity check for acessing a non-existing variable
		try:
			if variables[functionname+'_'+str(pointer-1)] >= 0:
				variables[functionname+'_'+str(pointer)] = variables[functionname+'_'+str(pointer-variables[functionname+'_'+str(pointer-1)])]
			else:
				print('\u001b[31;1mException\u001b[0m while handling variables in LOOK')
				input('LOOK can only take positive values')
				exit()
		except Exception:
			print('\u001b[31;1mException\u001b[0m while handling variables in LOOK')
			input('Accessed a non-existing variable')
			exit()
		
		#--- Delete temporary variables
		val = None
		del val
	
	#--- MATH command definition
	elif command.startswith('math'):
		equation = command[5:]
		
		#--- Sanity check for only uppercase letters (to prevent arbitrary code)
		equation = equation.upper()
		
		#--- Assign variables
		for i, v in enumerate(alphabet):
			if v in equation:
				if extendedFeatures == 1:
					if functionname == '_main':
						equation = equation.replace(v, str(variables[functionname+'_'+str(pointer-i-1)]))
					else:
						#--- Replacing variables (extended functionality of CALL)
						try:
							equation = equation.replace(v, str(variables[v]))
						except Exception:
							equation = equation.replace(v, str(variables[functionname+'_'+str(pointer-i-1)]))
				else:
					equation = equation.replace(v, str(variables[functionname+'_'+str(pointer-i-1)]))
		
		#--- All the letters were replaced by values so eval should be safe
		variables[functionname+'_'+str(pointer)] = int(eval(equation))
		
		#--- Delete temporary variable
		equation = None
		del equation
	
	#--- PRINT command definition
	elif command.startswith('print'):
		#--- Sanity check for accessing a non-existing variable
		try:
			print(str(variables[functionname+'_'+str(pointer-1)]))
			variables[functionname+'_'+str(pointer)] = 1
		except Exception:
			print('\u001b[31;1mException\u001b[0m while handling variables in PRINT')
			input('Accessed a non-existing variable')
			exit()
	
	#--- VALUE command definition
	elif command.startswith('value'):
		val = command[6:]
		
		#--- Do not allow _ (which is used internally) to be in input
		if '_' in val:
			print('\u001b[31;1mException\u001b[0m while handling input in VALUE')
			input('Value cannot contain an underscore')
			exit()
		
		#--- Extended functionality
		if extendedFeatures == 1:
			#--- Replacing variables (extended functionality of CALL)
			for i, v in enumerate(alphabet):
				if v in val:
					if functionname != '_main':
						#--- Sanity check for accessing a non-existing variable
						try:
							val = val.replace(v, str(variables[v]))
						except Exception:
							val = val.replace(v, str(variables[functionname+'_'+str(pointer-i-1)]))
		
		#--- Convert to integer if possible
		try:
			int(val)
			variables[functionname+'_'+str(pointer)] = int(val)
		except ValueError:
			variables[functionname+'_'+str(pointer)] = str(val)
		
		#--- Delete temporary variables
		val = None
		del val
	
	#--- Sanity check for wrong command
	else:
		input('--- Unrecognized command ---')
		exit()
	
	#--- Update current pointer
	pointerArray[-1] += 1

#--- Make interpreter calls
def main():
	if len(functions['_main']) != 0:
		while True:
			interpreter()
	else:
		print('\u001b[31;1mException\u001b[0m while setting up interpreter')
		input('Length of program must be non-zero')
		exit()

#--- Sanity check for importing
if __name__=='__main__':
	main()