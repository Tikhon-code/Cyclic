def lexer(*args): # Лексер
	elements = []
	lex = ''
	arg = ''
	command = ''
    
	for comm in args:
		command += comm + ' '

	separate = False   
	l=True
	for i in command:
		if i == ":":
			separate = True
			lex += " "
			continue
		if i == ' ' and l:
			separate = False
			l = False 
		elif l:
			if separate == True:
				elements.append(lex)
			separate = False
			lex += i
		else:
			if separate == True:
				elements.append(arg)
			separate = False
			arg += i
           
	for element in elements:
		print(element)
lexer("192:168:1:")
