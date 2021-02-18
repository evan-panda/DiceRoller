# DiceRoller
Welcome to my simple, text-based, dice rolling application. 
Type "help" in the application for the following information.
## Usage
    To exit, type: 'end', 'exit', 'stop', or 'quit'.
    This dice roller will roll values for any dice entered as the formula: <num>d<num>
    It can also handle basic formulas such as; adding multiple dice rolls together, and adding or subtracting modifiers. 
    (see input exaples below)
### Basic Input Examples:
    1d20+4
    1d20 + 6 + 2d4
    2d8 + 3
### Saving preset commands:
    Type 'add', 'set', or 'save'; then the name of the preset; then the roll associated with it.
    After it is saved, you can use the preset by just typing the name of it.
#### Example save:
    set atk 1d20+5
    save bless atk 1d20 + 4 + 1d4
    keep dmg 1d8 + 3
#### Example use:
    atk<press enter> - it will roll the preset value.
    rolld20 - is a default preset you can try

### Deleting a preset:
    Type 'delete', 'del', 'destroy', or 'remove'; then the name of the preset
    Enter confirmation, 'y', when asked. It will be removed from your presets file.
