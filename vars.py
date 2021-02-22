## variables 
presetsFileName = 'presets.json'
# replaceCharsRegex = r'[\s\`\~\!\@\#\$\%\^\&\*\(\)\_\=\[\]\{\}\\\|\;\:\'\"\,\<\>\/\?]'
replaceChars = '`~!@#$%^&*)(_=][}{\\|;:\'",.></? \t\r\n'
confirmList = [
    'y', 'yes', 'yy', 'yees', 'yeees', 'yess', 'yis', 'yep',
    'yeah', 'yea', 'yay', 'ye', 'yee', 'yey', 'yup', 'yuup', 
    'uh-huh', 'uh huh', 'affirmative', 'confirm', 'check', ':)']

## regex checks 
checkSave = r'^(add|set|save)' # starts with set, save, or keep 
checkDel = r'^(delete|del|remove|rem|destroy)' # start with delete, del, remove, or destroy 
checkRoll = r'([0-9]+[dD][0-9]+)' # check for xdx
checkValidBasic = r'(\d+\s*[+-]\s*)+|(\d+[dD]\d+)'
checkMod = r'(\s*[+-]\s*)' # find +/- symbols
checkDoublePlus = r'(\s*[+]\s*){2,}' # find 2 or more +/- in a row
checkDoubleMinus = r'(\s*[-]\s*){2,}' # find 2 or more +/- in a row
checkDigits = r'^\d+$' # check for only digits
checkQuit = r'^(end|exit|stop|quit|zxcv)' # starts with quit, exit, or stop
checkHelp = r'^(help|\-h)' # check for the word 'help'
checkInvalidChars = r'(?:(?![dD0-9+\-])[\x20-\x7e])+' # check for everything that isn't a number or 'd' or +/-
checkAdvDis = r'\-[aAdD]$'

## User Messages
print("Welcome to my simple dice roller. To exit, type: 'end', 'exit', 'stop', or 'quit'.")
print('This dice roller will roll values for any dice entered as the formula: <num>d<num>')
print('It can also handle basic formulas such as; adding multiple dice rolls together, and adding or subtracting modifiers.')
print("Type 'help' for examples and additional features.")

helpMessage = """
    To exit, type: 'end', 'exit', 'stop', or 'quit'
    This dice roller will roll values for any dice entered as the formula: <num>d<num>
    It can also handle basic formulas such as; adding multiple dice rolls together, and adding or subtracting modifiers.
    Input Examples:
        1d20+4
        1d20 + 6 + 2d4
        2d8 + 3

    Saving preset commands:
        Type 'add', 'set', or 'save'; then the name of the preset; then the roll associated with it.
        After it is saved, you can use the preset by just typing the name of it.
        Example save:
            set atk 1d20+5
            save bless atk 1d20 + 4 + 1d4
            keep dmg 1d8 + 3
        Example use:
            atk<press enter> - it will roll the preset value.
            rolld20 - is a default preset you can try

    Deleting a preset:
        Type 'delete', 'del', 'destroy', 'remove', or 'rem'; then the name of the preset
        Enter confirmation, 'y', when asked. It will be removed from your presets file.
    """

exitMessage = "Thanks for using my application!"