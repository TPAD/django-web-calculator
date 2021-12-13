# Tony Padilla
# apadilla
# 17-439 S20 Homework 3 Django Calculator

# Simple django calculator


from django.shortcuts import render

def calculator(request):
	context = {}
	inputs = {}
	nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

	# subsequent to the initial load of the page should only be POST request
	if request.method == 'GET':
		context = processGET(request)
	else:
		# verify that the input parameters are valid
		inputs = checkParameters(request)
		if 'message' in inputs:
			return render(request, 'calculator/errorpage.html', inputs)
		if inputs['button'] in nums:
			context = digitPressed(inputs)
		else:
			context = operationPressed(inputs)
			if 'message' in context:
				return render(request, 'calculator/errorpage.html', context)
	print(context)
	return render(request, 'calculator/calculator.html', context)

def processGET(request): 
	context = {}
	context['button'] = 0
	context['display'] = 0
	context['oldVal'] = 0
	context['operation'] = "plus"
	context['newVal'] = 0
	return context

'''
returns a dictionary of inputs on success
returns a dictionary containing a single error message on failure
sadly will not let user know if more than one thing has gone wrong 
but that is not required of this assignment afaik :-)
'''
def checkParameters(request):
	inputs = {}
	nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	ops = ['plus', 'minus', 'equals', 'times', 'divide']

	# checks request header existance and validity of the button pressed
	if not 'button' in request.POST or not request.POST['button']:
		inputs['message'] = 'MALFORMED INPUT: missing button press information'
		return inputs
	elif not request.POST['button'] in nums and not request.POST['button'] in ops:
		inputs['message'] = 'MALFORED INPUT: button not a valid number or operation'
		return inputs
	else:
		inputs['button'] = request.POST['button']

	# checks request header existance and validity of the calculator display
	if not 'display' in request.POST or not request.POST['display']:
		inputs['message'] = 'MALFORMED INPUT: missing display information'
		return inputs
	elif not request.POST['display'].lstrip("+-").isnumeric():
		inputs['message'] = 'MALFORMED INPUT: display not a valid number'
		return inputs
	else:
		inputs['display'] = request.POST['display']

	# checks request header existance and validity of the previous operation
	if not 'operation' in request.POST or not request.POST['operation']:
		inputs['message'] = 'MALFORMED INPUT: missing last operation'
		return inputs
	elif request.POST['operation'] not in ops:
		inputs['message'] = 'MALFORMED INPUT: previous operation is invalid'
		return inputs
	else:
		inputs['operation'] = request.POST['operation']

	# checks request header existance and validity of the previous value
	if not 'oldVal' in request.POST or not request.POST['oldVal']:
		inputs['message'] = 'MALFORMED INPUT: missing last value'
		return inputs
	elif not request.POST['oldVal'].lstrip("+-").isnumeric():
		inputs['message'] = 'MALFORMED INPUT: previous value is invalid'
		return inputs
	else:
		inputs['oldVal'] = request.POST['oldVal']

	# checks request header existance and validity of the new value
	if not 'newVal' in request.POST or not request.POST['newVal']:
		inputs['message'] = 'MALFORMED INPUT: missing new value'
		return inputs
	elif not request.POST['newVal'].lstrip("+-").isnumeric():
		inputs['message'] = 'MALFORMED INPUT: new value is invalid'
		return inputs
	else:
		inputs['newVal'] = request.POST['newVal']
	return inputs


# defines action for when the input is a digit button press
def digitPressed(context):
	context['newVal'] = int(context['newVal'])*10 + int(context['button'])
	context['display'] = context['newVal']
	return context

'''
defines action for when the input is an operation button press
will fail if it encounters division by zero in which case it will
return a dictionary containing a single error message
'''
def operationPressed(context):
	context['oldVal'] = calculateResult(context)
	if context['oldVal'] == 0 and context['operation'] == 'divide':
		context = {}
		context['message'] = 'ERROR: division by zero is undefined'
		return context
	context['operation'] = context['button']
	context['newVal'] = 0
	context['display'] = context['oldVal']

	return context

# utility function for operationPressed method
def calculateResult(context):
	if context['operation'] == "plus":
		return add(int(context['oldVal']), int(context['newVal']))
	if context['operation'] == "minus":
		return subtract(int(context['oldVal']), int(context['newVal'])) 
	if context['operation'] == "times":
		return multiply(int(context['oldVal']), int(context['newVal']))
	if context['operation'] == "divide":
		return divide(int(context['oldVal']), int(context['newVal']))
	if context['operation'] == "equals":
		return context['newVal']
	return 0

# wrappers for the binary operations available in this calculator
def add(n, m):
	return n + m

def subtract(n, m):
	return n - m

def divide(n, m):
	if (m == 0): 
		return 0
	return n // m

def multiply(n, m):
	return n * m