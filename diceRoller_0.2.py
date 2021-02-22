import re 
from dr_functions import *

## get presets 
presetsData = readPresetsFile(presetsFileName)

## app loop
while True: 
    cleanedRolls = [] # set default empty rolls list
    ## user input 
    userIn = input('\nEnter dice roll (#d# +/- <modifiers>): ')
    userIn = userIn.strip(replaceChars).lower()
    
    ## check roll type (advantage / disadvantage)
    rollType = setRollType(userIn)
    if rollType != RollType.Normal:
        userIn = userIn[:-2].strip(replaceChars)
    
    ## App Decisions
    if re.match(checkQuit, userIn): # see if the app should quit
        break
    elif re.match(checkSave, userIn): # see if user is trying to save a preset 
        print('--- saving preset ---')
        if not re.search(checkValidBasic, userIn):
            print(f'No roll found in "{userIn}"\nPlease try again.')
            continue

        savePreset(userIn, presetsData)
        continue
    elif re.match(checkDel, userIn):
        print('--- deleting preset ---')
        deletePreset(userIn, presetsData)
        continue
    elif re.match(checkValidBasic, userIn): # see if it's a basic roll 
        cleanedRolls = cleanRollInput(userIn)
    elif re.match(checkHelp, userIn): # help message 
        print(f'Help message: {helpMessage}')
        continue
    else:
        ## check for presets
        presetFound = False
        for pre in presetsData["presets"]:
            if userIn == pre["name"]:
                presetFound = True 
                cleanedRolls = cleanRollInput(pre["roll"])

        ## if no presets were found this will occur, or will skip if there are numbers in the input
        if not presetFound:
            print(f'It looks like you did not enter a vaid input and there were no presets matching: {userIn}')
            userCon = input('Quit? (y/n) ')
            userCon = userCon.strip(replaceChars).lower() 
            if userCon in confirmList:
                break 

    if len(cleanedRolls) < 1:
        print(f'"{userIn}" is not valid. Please try again.')
        continue 

    output = constructOutput(cleanedRolls) 

    ## print results
    print(f'Rolling: {"".join(cleanedRolls)}') 
    print(f'Rolled: {"".join(output[0])}') 
    print(f'Total: {str(output[1])}') 

print(exitMessage)
# input('Press enter to exit . . . ')