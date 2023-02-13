from sys import exit
from time import sleep
from os import system
system('')  # Enable ANSI color support in Windows

enableExtendedFeatures = 1
enableTestPrograms = 0

executeArray = ['_main']
pointerArray = [0]
variables = {'_global': 0}
functions = {}
custom = 0
commands = []
if not enableTestPrograms:
	print('Input the\u001b[31;1m While(true){\u001b[0m code separated by colons or newlines, empty for end of input')
	print('Uses eval() in MATH commands, make sure to\u001b[31;1m sanitize\u001b[0m it (it removes all letters so should be pretty safe)')
	print()
else:
	print('''Choose a program from the\u001b[31;1m manual\u001b[0m.
1. How to end a program?
2. How to define a function?
3. MATH variable input order explanation
4. Naming of functions - text
5. Naming of functions - number
6. Naming of functions - INPUT
7. Undefined functions
8. Recursion - calling itself
9. Recursion - calling alternately
10. Why CALL?
11. How to look at a previous result?
12. Conditional jumps?
13. What can we do with this? - truth-machine
14. What can we do with this? - Collatz conjecture''')
	if enableExtendedFeatures:
		print('''15. GLOBALW/R - named globals
16. GLOABLW/R - default
17. CALL - variables
18. CALL - context''')
	p = int(input(': '))
	if enableExtendedFeatures:
		match p:
			case 15:
				commands = ['value hi', 'globalw hello', 'globalr hello', 'value 0', 'jump']
			case 16:
				commands = ['value hi', 'globalw', 'globalr', 'globalr _global', 'value 0', 'jump']
			case 17:
				commands = ['value hi', 'globalw hello', 'value hello', 'define', 'globalr A', 'print', 'defined',
							'value hello', 'call A', 'globalr A', 'print', 'value 0', 'jump']
			case 18:
				commands = ['value hello', 'define', 'value hi', 'globalw A', 'globalr A', 'print', 'defined',
							'value hi', 'value hello', 'call B', 'value 0', 'jump']
	match p:
		case 1:
			commands = ['value 0', 'jump']
		case 2:
			commands = ['value name', 'define', 'defined', 'value 0', 'jump']
		case 3:
			commands = ['value 1', 'value 2', 'value 3', 'math A+B+C', 'print', 'value 0', 'jump']
		case 4:
			commands = ['value hi how are you', 'define', 'defined', 'value 0', 'jump']
		case 5:
			commands = ['value 1', 'value 2', 'math A+B', 'define', 'defined', 'value 0', 'jump']
		case 6:
			commands = ['input', 'define', 'defined', 'value 0', 'jump']
		case 7:
			commands = ['value hi', 'call', 'value hi', 'define', 'value hi', 'print', 'defined', 'value hi', 'call',
						'value 0', 'jump']
		case 8:
			commands = ['value hi', 'define', 'value hi', 'print', 'value hi', 'call', 'defined', 'value hi', 'call',
						'value 0', 'jump']
		case 9:
			commands = ['value hi', 'define', 'value hi', 'print', 'value hello', 'call', 'defined', 'value hello',
						'define', 'value hello', 'print', 'value hi', 'call', 'defined', 'value hi', 'call', 'value 0',
						'jump']
		case 10:
			commands = ['value 3', 'define', 'defined', 'value 1', 'value 2', 'math A+B', 'call', 'value 0', 'jump']
		case 11:
			commands = ['value 1', 'value 2', 'math A+B', 'value line 1', 'value line 2', 'value line 3',
						'value line 4', 'value line 5', 'value line 6', 'value line 7', 'value line 8', 'value line 9',
						'value line 10', 'math K', 'print', 'value 0', 'jump']
		case 12:
			commands = ['value loop', 'define', 'value hi', 'print', 'globalr', 'math A+1', 'globalw', 'defined',
						'value loop', 'call', 'globalr', 'math A>3', 'math (A==0) * 5 + (A!=0) * (-1)', 'jump',
						'value 0', 'jump']
		case 13:
			commands = ['value 1', 'define', 'value 1', 'print', 'value 1', 'call', 'defined', 'input', 'call',
						'value 0', 'print', 'value 0', 'jump']
		case 14:
			commands = ['value step', 'define', 'globalr', 'math A%2 * (3*A+1) + (A%2==0) * A/2', 'globalw', 'globalr',
						'print', 'defined', 'value enter an arbitrary integer', 'print', 'input', 'globalw', 'globalr',
						'print', 'math (B!=1) * (-1) + (B==1) * (-3)', 'jump', 'value step', 'call', 'globalr',
						'math (A!=1) * 4 + (A==1) * (-1)', 'jump', 'value 0', 'jump']
		case _:
			if not commands:
				print('Invalid option')
				exit()

# Custom input parser
if not commands:
	loopBreak = 0
	while not loopBreak:
		command = input().strip().split(';')
		if len(command) > 1:
			for i in command:
				if i.strip() == '':
					loopBreak = 1
					break
				commands.append(i.strip())
		else:
			if command[0] == '':
				loopBreak = 1
				break
			commands.append(command[0])
	del loopBreak
functions['_main'] = commands
for i, v in enumerate(commands):
	variables['_main_'+str(i)] = str(0)
	if enableTestPrograms:  # Print command list for preset programs
		print(v)
if enableTestPrograms:
	print()
del commands


def interpreter():
	global executeArray
	global pointerArray
	global functions
	global variables
	global enableExtendedFeatures
	alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	# Get current pointer, function and its commands
	fn_name = executeArray[-1]
	pointer = pointerArray[-1]
	cmd_list = functions[fn_name]
	# Exit function on end or repeat main program
	if pointer >= len(cmd_list):
		if fn_name == '_main':
			pointerArray[-1] = 0
			return
		else:
			for _, _v in enumerate(alphabet):
				if '_'+_v in variables:
					variables.pop('_'+_v)
			del executeArray[-1]
			del pointerArray[-1]
			return
	# Get current command
	_command = cmd_list[pointer]
	if _command.startswith('call'):
		val = _command[5:]
		letters = []
		# Extended functionality (pass variables)
		if enableExtendedFeatures == 1:
			# Sanity check for only uppercase letters
			val = val.upper()
			# Loop for replacing variables
			for _i, _v in enumerate(alphabet):
				# Sanity check for accessing a non-existing variable
				try:
					if _v in val:
						letters.append(variables[fn_name+'_'+str(pointer-_i-1)])
				except KeyError:
					print('\u001b[31;1mException\u001b[0m while handling variables in CALL')
					input('Accessed a non-existing variable')
					exit()
			else:
				for _i, _v in enumerate(alphabet):
					if not letters:
						break
					variables['_'+_v] = letters[0]
					letters = letters[1:]	
		else:
			if val:
				print('\u001b[31;1mException\u001b[0m while handling syntax in CALL')
				input('Extended features not enabled, CALL does not take arguments')
				exit()
		fun_name = str(variables[fn_name+'_'+str(pointer-1)])
		# Do not allow _ (which is used internally) to be in input
		if '_' in fun_name:
			print('\u001b[31;1mException\u001b[0m while handling input in CALL')
			input('Value cannot contain an underscore')
			exit()
		# If function exists, call it
		if fun_name in functions:
			# If the function you're calling was called previously
			# And has not ended (still in executeArray)
			# Then delete everything after that function in executeArray
			# Since functions are calling themselves in a loop
			if fun_name in executeArray:
				variables[fn_name+'_'+str(pointer)] = 1
				if fun_name != fn_name:
					pointerArray = pointerArray[:executeArray.index(fun_name)+1]
					executeArray = executeArray[:executeArray.index(fun_name)+1]
				# Reset the pointer of the called function to 0
				pointerArray[-1] = 0
			else:
				variables[fn_name+'_'+str(pointer)] = 1
				# Update pointer for this function to not get stuck on CALL
				pointerArray[-1] += 1
				# Add the function to the queue
				executeArray.append(fun_name)
				pointerArray.append(0)
			# Delay to not spam in case of infinite recursion
			sleep(0.02)
			return
		del fun_name
		del val
	elif _command.startswith('define'):
		if _command.startswith('defined'):
			variables[fn_name+'_'+str(pointer)] = 1
			pointerArray[-1] += 1
			return
		fun_name = str(variables[fn_name+'_'+str(pointer-1)])
		# Do not allow _ (which is used internally) to be in input
		if '_' in fun_name:
			print('\u001b[31;1mException\u001b[0m while handling input in DEFINE')
			input('Value cannot contain an underscore')
			exit()
		# Sanity check for overwriting functions
		if fun_name in functions:
			print('\u001b[31;1mException\u001b[0m while handling input in DEFINE')
			input('Overwriting functions is not enabled')
			exit()
		# Add commands
		lines = []
		while True:
			pointer += 1
			pointerArray[-1] += 1
			if cmd_list[pointer] == 'defined':
				variables[fn_name+'_'+str(pointer)] = 1
				break
			lines.append(cmd_list[pointer])
		functions[fun_name] = lines
		variables[fn_name+'_'+str(pointer)] = 1
		del fun_name
		del lines
	elif _command.startswith('globalw'):
		access = '_global'
		# Extended functionality (custom global variables)
		if enableExtendedFeatures == 1:
			access = _command[8:]
			# Do not allow _ (which is used internally) to be in input
			if '_' in access:
				print('\u001b[31;1mException\u001b[0m while handling input in GLOBALR (extended functionality)')
				input('Value cannot contain an underscore')
				exit()
			# Replacing variables (extended functionality of CALL)
			if fn_name != '_main':
				for _i, _v in enumerate(alphabet):
					if _v in access:
						# --- Sanity check for accessing a non-existing variable
						try:
							access = access.replace(_v, str(variables['_'+_v]))
						except KeyError:
							pass
			# If extended features are enabled but not used, reset to default
			if access == '':
				access = '_global'
		else:
			if _command[8:] != '':
				print('\u001b[31;1mException\u001b[0m while handling syntax in GLOBALW')
				input('Extended features not enabled, GLOBALW does not take arguments')
				exit()
		# Sanity check for accessing a non-existing variable
		try:
			variables[access] = variables[fn_name+'_'+str(pointer-1)]
		except KeyError:
			print('\u001b[31;1mException\u001b[0m while handling variables in GLOBALW')
			input('Accessed a non-existing variable')
			exit()
		del access
	elif _command.startswith('globalr'):
		access = '_global'
		if enableExtendedFeatures == 1:
			access = _command[8:]
			# Do not allow _ (which is used internally) to be in input
			if '_' in access:
				print('\u001b[31;1mException\u001b[0m while handling input in GLOBALR (extended functionality)')
				input('Value cannot contain an underscore')
				exit()
			# Replacing variables (extended functionality of CALL)
			if fn_name != '_main':
				for _i, _v in enumerate(alphabet):
					if _v in access:
						# --- Sanity check for accessing a non-existing variable
						try:
							access = access.replace(_v, str(variables['_'+_v]))
						except KeyError:
							pass
			# If extended features are enabled but not used, reset to default
			if access == '':
				access = '_global'
		else:
			if _command[8:] != '':
				print('\u001b[31;1mException\u001b[0m while handling syntax in GLOBALR')
				input('Extended features not enabled, GLOBALR does not take arguments')
				exit()
		# Sanity check for accessing a non-existing variable
		try:
			variables[fn_name+'_'+str(pointer)] = variables[access]
		except KeyError:
			print('\u001b[31;1mException\u001b[0m while handling variables in GLOBALR')
			input('Accessed a non-existing variable')
			exit()
		del access
	elif _command.startswith('input'):
		val = input(': ')
		# Do not allow _ (which is used internally) to be in input
		if '_' in val:
			print('\u001b[31;1mException\u001b[0m while handling input in INPUT')
			input('Value cannot contain an underscore')
			exit()
		# Empty string is not a valid input
		if val != '':
			variables[fn_name+'_'+str(pointer)] = val
		del val
	elif _command.startswith('jump'):
		val = 0
		# Sanity check for random values
		try:
			val = int(variables[fn_name+'_'+str(pointer-1)])
		except ValueError:
			print('\u001b[31;1mException\u001b[0m while handling variables in JUMP')
			input('Can only jump to a number')
			exit()
		# Sanity check for accessing a non-existing variable
		try:
			if val == 0:
				variables[fn_name+'_'+str(pointer)] = 1
				input('--- Program ended ---')
				exit()
			else:
				if pointer-val < 0:
					raise KeyError
				pointerArray[-1] = pointer-val
				variables[fn_name+'_'+str(pointer)] = 1
		except KeyError:
			print('\u001b[31;1mException\u001b[0m while handling variables in JUMP')
			input('Accessed a non-existing pointer')
			exit()
		del val
	elif _command.startswith('math'):
		equation = _command[5:]
		# Sanity check for only uppercase letters (to prevent arbitrary code)
		equation = equation.upper()
		# Assign variables
		for _i, _v in enumerate(alphabet):
			if _v in equation:
				if enableExtendedFeatures == 1:
					if fn_name == '_main':
						try:
							equation = equation.replace(_v, str(variables[fn_name+'_'+str(pointer-_i-1)]))
						except KeyError:
							print('\u001b[31;1mException\u001b[0m while handling variables in MATH')
							print('Accessed a non-existing variable')
							exit()
					else:
						# Replacing variables (extended functionality of CALL)
						try:
							equation = equation.replace(_v, str(variables[_v]))
						except KeyError:
							try:
								equation = equation.replace(_v, str(variables[fn_name+'_'+str(pointer-_i-1)]))
							except KeyError:
								print('\u001b[31;1mException\u001b[0m while handling variables in MATH')
								print('Accessed a non-existing variable')
								exit()
				else:
					try:
						equation = equation.replace(_v, str(variables[fn_name+'_'+str(pointer-_i-1)]))
					except KeyError:
						print('\u001b[31;1mException\u001b[0m while handling variables in MATH')
						print('Accessed a non-existing variable')
						exit()
		# All the letters were replaced by values so eval should be safe
		variables[fn_name+'_'+str(pointer)] = int(eval(equation))
		del equation
	elif _command.startswith('print'):
		# Sanity check for accessing a non-existing variable
		try:
			print(str(variables[fn_name+'_'+str(pointer-1)]))
			variables[fn_name+'_'+str(pointer)] = 1
		except KeyError:
			print('\u001b[31;1mException\u001b[0m while handling variables in PRINT')
			input('Accessed a non-existing variable')
			exit()
	elif _command.startswith('value'):
		val = _command[6:]
		# Do not allow _ (which is used internally) to be in input
		if '_' in val:
			print('\u001b[31;1mException\u001b[0m while handling input in VALUE')
			input('Value cannot contain an underscore')
			exit()
		if enableExtendedFeatures == 1:
			# Replacing variables (extended functionality of CALL)
			for _i, _v in enumerate(alphabet):
				if _v in val:
					if fn_name != '_main':
						# Sanity check for accessing a non-existing variable
						try:
							val = val.replace(_v, str(variables[_v]))
						except KeyError:
							try:
								val = val.replace(_v, str(variables[fn_name+'_'+str(pointer-_i-1)]))
							except KeyError:
								print('\u001b[31;1mException\u001b[0m while handling variables in PRINT')
								input('Accessed a non-existing variable')
								exit()
		# Convert to integer if possible
		try:
			int(val)
			variables[fn_name+'_'+str(pointer)] = int(val)
		except ValueError:
			variables[fn_name+'_'+str(pointer)] = str(val)
		del val
	# Sanity check for wrong command
	else:
		print('--- Unrecognized command ---')
		input(_command)
		exit()
	pointerArray[-1] += 1


# Make interpreter calls
def main():
	if len(functions['_main']) != 0:
		while True:
			interpreter()
	else:
		print('\u001b[31;1mException\u001b[0m while setting up interpreter')
		input('Length of program must be non-zero')
		exit()


# Sanity check for importing
if __name__ == '__main__':
	main()
