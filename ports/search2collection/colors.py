class colors:

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
    
    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
        yellow =  '\033[48;2;255;255;0m'
        
    class cursor:
        
        blinkon = '\033[5m'
        blinkoff = '\033[0m'

#print(colors.bg.green, "SKk", colors.fg.red, "Amartya")

###############################################################################
if __name__ == '__main__':
 ##############################################################################
 
 
# \033[38;2;<r>;<g>;<b>m     #Select RGB foreground color
# \033[48;2;<r>;<g>;<b>m     #Select RGB background color
 
     print(chr(27) + "[2J")
     print(colors.bg.black, "HELLO WHAT CAN you see?", colors.fg.lightgreen, "Not so good")
     print(colors.bg.yellow, "HELLO WHAT CAN you see?", colors.fg.red, "Not so good")
     print(colors.cursor.blinkon, "HELLO WHAT CAN you see?", colors.cursor.blinkoff, "Not so good")
     print('\033[5mHELLO WHAT CAN you see?', colors.cursor.blinkoff, "Not so good")