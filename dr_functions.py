from os import path
from random import randint
import re 
import json 
from enum import Enum
from vars import *

class RollType(Enum):
    Dis = 0
    Normal = 1
    Adv = 2

## check if user wants to roll with advantage or disadvantage
def setRollType(userIn):
    rollType = RollType.Normal

    if re.search(checkAdvDis, userIn):
        if userIn[-1] == 'a':
            rollType = RollType.Adv
        elif userIn[-1] == 'd':
            rollType = RollType.Dis

    return rollType

## gets data from file or creates default data if file doesn't exist
def readPresetsFile(fileName):
    if path.exists(fileName):
        with open(fileName, mode='r') as pFile:
            presetsData = json.load(pFile)
    else:
        with open(fileName, mode='w') as pFile:
            default = {
                "presets": [
                    {
                        "name": "rolld20",
                        "roll": "1d20"
                    }
                ]
            }
            json.dump(default, pFile, indent=4)

        with open(fileName, mode='r') as pFile:
            presetsData = json.load(pFile)
            
    return presetsData

## Dice rolling
def rollDice(diceRoll):
    dr = re.split('[dD]', diceRoll, maxsplit=2)
    rolls = []
    for i in range(int(dr[0])):
        rolls.append(randint(1, int(dr[1])))

    return rolls

## deciding to add positive or negative number
def addItems(sign, num):
    if type(num) is list:
        num = sum(num)

    if sign == '-':
        return num * -1

    return num

## get list of various rolls and additions / subtractions
def cleanRollInput(rollInput):
    # need to handle: <preset> [+/-] <roll/mod>, <roll/mod>[\s]<roll/mod>
    stripDoubleMods = re.sub(checkDoublePlus, '+', rollInput)
    stripDoubleMods = re.sub(checkDoubleMinus, '-', stripDoubleMods)
    userRolls = re.split(checkMod, stripDoubleMods)
    cleanedRolls = []
    for item in userRolls:
        item = item.strip(replaceChars)
        if len(re.findall(r'[dD]', item)) > 1: # check for multiple "d's" in the roll
            cleanedRolls = []
            return cleanedRolls
        elif re.findall(checkInvalidChars, item):
            cleanedRolls = []
            return cleanedRolls
        # item = re.sub(replaceCharsRegex, '', item)
        cleanedRolls.append(item)
    return cleanedRolls

## construct output and get total roll
def constructOutput(rollInput, rollType):
    if rollType == RollType.Adv:
        print('rolling with advantage')
    elif rollType == RollType.Dis:
        print('rolling with disadvantage')
    else:
        print('normal roll')
    
    total = 0 # total number rolled +/- others
    output = [] # output string list
    for indx, item in enumerate(rollInput):
        if indx > 0:
            sign = rollInput[indx - 1]
        else:
            sign = '+'
        
        if re.match(checkRoll, item) is not None:
            item = rollDice(item)
            total += addItems(sign, item)

            output.append('(')
            for i, val in enumerate(item):
                if i == (len(item) - 1):
                    output.append(str(val))
                else:
                    output.append(str(val) + ' + ')
            output.append(') ')
        elif re.search(checkMod, item) is not None:
            output.append(item + ' ')
        elif re.match(checkDigits, item) is not None:
            output.append(item + ' ')
            item = int(item)
            total += addItems(sign, item)
    
    return [output, total]

## check for existing preset and/or save the new preset
def savePreset(userIn, presetsData):
    # get preset name and value 
    startName = re.match(checkSave, userIn).end()
    endName = re.search(checkValidBasic, userIn).start()
    presetName = userIn[startName:endName].strip(replaceChars)
    print(f'preset name: {presetName} ')
    cleanedRolls = cleanRollInput(userIn[endName:])
    newPreset = {
        "name": presetName,
        "roll": ''.join(cleanedRolls)
    }

    if len(cleanedRolls) > 0 and len(presetName) > 0:
        # check if the preset exists and ask if it should be updated
        existsFlag = False
        for pre in presetsData["presets"]:
            if newPreset["name"] == pre["name"]:
                existsFlag = True
                print(f'Preset already exists: {pre["name"]}')
                print(f'Would you like to update the value from <{pre["roll"]}> to <{newPreset["roll"]}> ?')
                confirmUpdate = input('(y/n) ')
                confirmUpdate = confirmUpdate.strip(replaceChars).lower()
                if confirmUpdate in confirmList:
                    print(f'Updated the preset: {pre["name"]}\n From: {pre["roll"]} | To: {newPreset["roll"]}')
                    pre["roll"] = newPreset["roll"]
                    with open(presetsFileName, mode='w') as pFile:
                        json.dump(presetsData, pFile, indent=4)
                else:
                    print(f'Did not update existing preset: {pre["name"]}, value: {pre["roll"]}')
        # save new preset, use flag to see if it found an existing one.
        if not existsFlag:
            presetsData["presets"].append(newPreset)
            with open(presetsFileName, mode='w') as pFile:
                json.dump(presetsData, pFile, indent=4)
            print(f'Preset added: {newPreset["name"]}, value: {newPreset["roll"]}')
        
        readPresetsFile(presetsFileName) # update presets list in memory
    else:
        print('Invalid preset; not saved. Preset must have name and valid roll.')

## delete existing preset
def deletePreset(userIn, presetsData):
    ## get preset name
    start = re.match(checkDel, userIn).end()
    presetName = userIn[start:]
    presetName = presetName.strip(replaceChars).lower()
    presetFound = False
    for i, pre in enumerate(presetsData["presets"]):
        if presetName == pre["name"]:
            presetFound = True
            print(f'Are you sure you want to delete the preset: {pre["name"]} ?')
            userCon = input(f'Name: {pre["name"]}, Value: {pre["roll"]} Delete? (y/n) ')
            if userCon in confirmList:
                del presetsData["presets"][i]
                print(f'Preset {pre["name"]} deleted.')

                with open(presetsFileName, mode='w') as pFile:
                    json.dump(presetsData, pFile, indent=4)
                    
                presetsData = readPresetsFile(presetsFileName)
            else:
                print('Did not delete the preset.')
    
    if not presetFound:
        print(f'No preset found matching name: "{presetName}"\nPlease try again.') 

