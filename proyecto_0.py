class fileInfo:
     procedures = {}
     variables = {}
     nativeProc = {}


#------------- Syntaxis del lenguaje ------------------
integers = ["1","2","3","4","5","6","7","8","9","0"]
controlStructures = ["if", "while", "repeat"]
conditionStructures = ["facing", "can", "not"]
directions = ["north","south","east", "west"]
#------------------------------------------------------

def verifyFile(fileName):

    #Convertir el archivo en un solo string
    wholeText = ""
    with open(fileName, "r") as file:
        for line in file:
                wholeText += line.strip()
    
    #Informacion del archivo  
    shortTimeMemory = ""
    currentState = None  #Posibles estados: "Var", "Proc_name", "Proc_parameters", "Proc_cblock", "Command_block", "Control_structure"
    secondState = None #Posibles estados: "Check_var"
    currentProcName = None
    variables = fileInfo.procedures
    procedures = fileInfo.variables
    procedures = updateProcedures(procedures)
    fileInfo.nativeProc = procedures
    calledProcVariables = {}
    

    i = 0
    #Iteramos sobre cada caracter
    while i < len(wholeText):
        character = wholeText[i]
        print(shortTimeMemory)
        i += 1
        if character == " ":
                continue
        
        # Aun no sabemos si esta definiendo una varible,
        # un procedimiento, o un bloque de comandos
        if currentState == None:

            unkownState = shortTimeMemory
        
            if unkownState == "defVar":
                currentState = "Var"
                shortTimeMemory = ""
                i -= 1
                continue

            if unkownState == "defProc":
                currentState = "Proc_naming"
                shortTimeMemory = ""
                i -=1
                continue

            if unkownState == "{":
                currentState = "Command_block"
                shortTimeMemory = ""
                i -=1
                continue

            shortTimeMemory += character
            continue

        #Ya sabemos qué se esta definiendo     

        if currentState == "Var":
            
            if character in integers:
                newVarible = shortTimeMemory
                integer = checkForIntegerAhead(wholeText, i-1)
                print(integer)
                if integer[1]:
                    variables[newVarible] = integer[0]
                    print(variables)
                    shortTimeMemory = ""
                    currentState = None
                    i = integer[1] # to skip the number since we already read it with checkForIntegerAhead() 
                    continue
                else:
                    print("Integer",integer[0],"is not valid")
                    break

            shortTimeMemory += character
            continue
            
        if currentState == "Proc_naming":
            if character == "(":
                newProcedure = shortTimeMemory
                procedures[newProcedure] = []
                shortTimeMemory = ""
                #para la siguiente etapa:
                currentProcName = newProcedure
                currentState = "Proc_parameters"
                continue
        
            shortTimeMemory += character
            continue

        if currentState == "Proc_parameters":

            if character == ",":
                newParameter = shortTimeMemory
                procedures[currentProcName].append(newParameter)
                shortTimeMemory = ""
                continue

            if character == ")":
                newParameter = shortTimeMemory
                procedures[currentProcName].append(newParameter)
                shortTimeMemory = ""
                #para la siguiente etapa:
                currentState = "Command_block"
                checkError = checkForSymbolAhead(wholeText, ["{"],i)
                if not checkError:
                    print("Seems you forgot to add {")
                    break
                i = checkError + 1 # to skip "{" since we already know its there
                continue
            
            shortTimeMemory += character
            continue

        if currentState == "Command_block":
                
                if shortTimeMemory in controlStructures:
                    controlStructure = shortTimeMemory
                    shortTimeMemory = ""
                    verifyControlStructure(wholeText, i, controlStructure)

                if secondState == "Check_var": # means we are checking varibles called of a procedure

                    if character == ",":
                        try:
                            calledVarible = shortTimeMemory
                            shortTimeMemory = ""
                            if ItsaNumber(calledVarible):
                                calledProcVariables[calledProc] += 1
                                continue
                            if currentProcName == None:
                                variables[calledVarible]
                                calledProcVariables[calledProc] += 1 
                                continue
                            if (calledVarible in procedures[currentProcName]) or variables[calledVarible]:
                                calledProcVariables[calledProc] += 1 
                                continue

                        except Exception as e:
                            print("Could not find varible", calledVarible)
                            break

                    if character == ")":

                        try:
                            calledVarible = shortTimeMemory
                            shortTimeMemory = ""
                            minParameters = len([x for x in procedures[calledProc] if x != "opt"])
                            maxParameters = len(procedures[calledProc])


                            if ItsaNumber(calledVarible):
                                calledProcVariables[calledProc] += 1

                            elif currentProcName == None:
                                variables[calledVarible]
                                calledProcVariables[calledProc] += 1 
                            
                            elif (calledVarible in procedures[currentProcName]) or variables[calledVarible]:
                                calledProcVariables[calledProc] += 1 
                            
                            numberVariblesCalled = calledProcVariables[calledProc]

                            if not (minParameters <= numberVariblesCalled <= maxParameters): 
                                print("The procedure '",calledProc,"' takes at least",minParameters,"parameters and maximum",maxParameters)
                                break

                            checkError = checkForSymbolAhead(wholeText, [";","}"], i)
                            if not checkError:
                                print("Seems you forgot to add ; or }")
                                break
                            i = checkError + 1 # to skip ";" since we already know its there
                            if checkError == "}":
                                currentState = None
                                currentProcName = None
                                continue
                            else:
                                secondState = None
                                continue
                        except Exception as e:
                            print("Could not find varible", calledVarible)
                            break

                if character == "(": #means this is a procedure
                    try:
                        calledProc = shortTimeMemory
                        procedures[calledProc]
                        calledProcVariables[calledProc] = 0
                        secondState = "Check_var"
                        shortTimeMemory = ""
                        continue
                        
                    except Exception as e:
                        print("Could not find the procedure",calledProc,"as either native or previously defined")
                        break

                if character == "=": #means this is an assignment
                    try:
                        calledVarible = shortTimeMemory
                        variables[calledVarible]
                        shortTimeMemory = ""
                        checkError = checkForSymbolAhead(wholeText, [";","}"], i)
                        if not checkError:
                            print("Seems you forgot to add ; or }",)
                            break
                        i = checkError + 1 # to skip ";" since we already know its there
                        if checkError == "}":
                            currentState = None
                            secondState = None
                        continue
                        
                    except Exception as e:
                        print("Could not find varible", calledVarible)
                        break
                
                shortTimeMemory += character
                continue

    if shortTimeMemory == "" and (i >= len(wholeText)):
        return "Nice! Kevin aproves your file\nCorrect File!"
    else:
        return "Sorry, Kevin could not understand your code\nIncorrect File!"


#--------------------------------------
# FUNCTIONS FOR CONTROL STRUCTURES
#--------------------------------------

def verifyControlStructure(wholeText, pos, controlStructure):
    


def verifyIfSutructure(wholeText, pos):
        
    checkError = verifyConditionStructure(wholeText, pos)
    if not checkError:
        return False
    else:
        pos = checkError
    
    shortTimeMemory = ""
    while pos < len(wholeText):
        character = wholeText[pos]
        shortTimeMemory += character
        if character == "{":
            break
        continue

    if shortTimeMemory[-1:] != ")":
        print("Seems you forgot to close the parentheses")
        return False
    
    verifyCommandBlock(wholeText, pos)



def verifyConditionStructure(wholeText, pos, conditionStructure):
    shortTimeMemory = ""

    while pos < len(wholeText):
        character = wholeText[pos]
        pos += 1
        if character == "(":
            break
        shortTimeMemory += character
        continue


    unkownCondition = shortTimeMemory.replace(" ","").replace("not","")

    if unkownCondition == "facing":
        direction = lookForDirection(wholeText, pos)

        if not directions:
            print("Unvalid direction for conditional _facing()_")
            return False
        
        return direction

    elif unkownCondition == "can":
        command = verifySimpleCommand(wholeText, pos)
        if not command:
            print("Unvalid command for conditional _can()_")
            return False
        
        return direction

    print("Unvalid conditional",unkownCondition)
    return False


def verifySimpleCommand(wholeText, pos):
    variables = fileInfo.variables
    procedures = fileInfo.procedures
    shortTimeMemory = ""

    while pos < len(wholeText):

        character = wholeText[pos]
        if character == "(":
            break
        shortTimeMemory += character
    
    simpleCommand = shortTimeMemory.replace(" ","")
    shortTimeMemory = ""
    if simpleCommand in fileInfo.nativeProc:

        while pos < len(wholeText):

            character = wholeText[pos]
            if character == ")":
                break
            shortTimeMemory += character

        numberVariables = len(shortTimeMemory.replace(" ","").split(","))

        minParameters = len([x for x in procedures[simpleCommand] if x != "opt"])
        maxParameters = len(procedures[simpleCommand])

        if not (minParameters <= numberVariables <= maxParameters): 
            print("The procedure '",simpleCommand,"' takes at least",minParameters,"parameters and maximum",maxParameters)
            return False
        return pos
    else:
        print("Could not find procedure",simpleCommand)
        return False


def verifyCommandBlock(wholeText, pos):
    variables = fileInfo.variables
    procedures = fileInfo.procedures

    i = pos
    calledProcVariables = {}
    shortTimeMemory  = ""

    while i < len(wholeText):
        character = wholeText[i]
        print(shortTimeMemory)
        i += 1

        if character == " ":
                continue

        if secondState == "Check_var": # means we are checking varibles called of a procedure

            if character == ",":
                try:
                    calledVarible = shortTimeMemory
                    shortTimeMemory = ""
                    if ItsaNumber(calledVarible):
                        calledProcVariables[calledProc] += 1
                        continue
                    if currentProcName == None:
                        variables[calledVarible]
                        calledProcVariables[calledProc] += 1 
                        continue
                    if (calledVarible in procedures[currentProcName]) or variables[calledVarible]:
                        calledProcVariables[calledProc] += 1 
                        continue

                except Exception as e:
                    print("Could not find varible", calledVarible)
                    break

            if character == ")":

                try:
                    calledVarible = shortTimeMemory
                    shortTimeMemory = ""
                    minParameters = len([x for x in procedures[calledProc] if x != "opt"])
                    maxParameters = len(procedures[calledProc])


                    if ItsaNumber(calledVarible):
                        calledProcVariables[calledProc] += 1

                    elif currentProcName == None:
                        variables[calledVarible]
                        calledProcVariables[calledProc] += 1 
                    
                    elif (calledVarible in procedures[currentProcName]) or variables[calledVarible]:
                        calledProcVariables[calledProc] += 1 
                    
                    numberVariblesCalled = calledProcVariables[calledProc]

                    if not (minParameters <= numberVariblesCalled <= maxParameters): 
                        print("The procedure '",calledProc,"' takes at least",minParameters,"parameters and maximum",maxParameters)
                        break

                    checkError = checkForSymbolAhead(wholeText, [";","}"], i)
                    if not checkError:
                        print("Seems you forgot to add ; or }")
                        break
                    i = checkError + 1 # to skip ";" since we already know its there
                    if checkError == "}":
                        currentState = None
                        currentProcName = None
                        continue
                    else:
                        secondState = None
                        continue
                except Exception as e:
                    print("Could not find varible", calledVarible)
                    break

        if character == "(": #means this is a procedure
            try:
                calledProc = shortTimeMemory
                procedures[calledProc]
                calledProcVariables[calledProc] = 0
                secondState = "Check_var"
                shortTimeMemory = ""
                continue
                
            except Exception as e:
                print("Could not find the procedure",calledProc,"as either native or previously defined")
                break

        if character == "=": #means this is an assignment
            try:
                calledVarible = shortTimeMemory
                variables[calledVarible]
                shortTimeMemory = ""
                checkError = checkForSymbolAhead(wholeText, [";","}"], i)
                if not checkError:
                    print("Seems you forgot to add ; or }",)
                    break
                i = checkError + 1 # to skip ";" since we already know its there
                if checkError == "}":
                    currentState = None
                    secondState = None
                continue
                
            except Exception as e:
                print("Could not find varible", calledVarible)
                break
        
        shortTimeMemory += character
        continue


def lookForDirection(wholeText, pos):
    shortTimeMemory = ""

    while pos < len(wholeText) and len(shortTimeMemory) <= 5:

        character = wholeText[pos]
        if character == " ":
            pos += 1
            continue
        shortTimeMemory += character
    
    direction = shortTimeMemory
    if (direction in directions):
        return pos
    if (direction[:-1] in directions):
        return pos
    return False


#-------------------------------------
# FUNCTIONS TO VERIFY CORRECT SYNTAX
#-------------------------------------


def checkForSymbolAhead(wholeText, symbol, pos):
    while pos < len(wholeText):
        character = wholeText[pos]
        if character == " ":
            pos += 1
            continue
        if character in symbol:
            return pos
        else:
            return False
    return False


def checkForIntegerAhead(wholeText, pos):
    shortTimeMemory = ""
    while pos < len(wholeText):
        character = wholeText[pos]
        if character == " ":
            pos += 1
            continue
        if character in integers:
            shortTimeMemory += character
            pos += 1
        else:
            break
    try:
        k = float(shortTimeMemory)
        return (k,pos)
    except Exception as e:
        return (shortTimeMemory, False)


def ItsaNumber(number):
    try:
        int(number)
        return True
    except Exception as e:
        return False


#---------------------------------
# FUNCTION TO UPDATE PROCEDURES
#---------------------------------

def updateProcedures(procedures):
    procedures["jump"] = ["v","v"]
    procedures["walk"] = ["v","opt"]
    procedures["leap"] = ["v","opt"]
    procedures["turn"] = ["v"]
    procedures["turnto"] = ["v"]
    procedures["drop"] = ["v"]
    procedures["get"] = ["v"]
    procedures["grab"] = ["v"]
    procedures["letGo"] = ["v"]
    procedures["nop"] = None
    return procedures



#---------------------------------
#           CONSOLE
#---------------------------------

Continue = False
print("Hi! i'm Kevin, i'll help you check your file syntax")

while Continue:
    fileName = input("Enter the name of the file you'd like to test: ")
    isItCorrect = verifyFile(fileName)
    print(isItCorrect)
    print("\nEnter 0 to leave\n\n")


file_path = "command_block.txt"

print(verifyFile(file_path))




    