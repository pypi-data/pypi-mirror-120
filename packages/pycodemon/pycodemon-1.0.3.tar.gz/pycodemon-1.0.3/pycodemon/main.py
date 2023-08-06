import sys
from pycodemon.start import start
from pycodemon.compiler import colored

def main():
    args = sys.argv[1:]
    if(len(args) == 1):
        if(args[0] == 'help'):
            print(colored(255, 216, 66, 'To Run A File In Codemon, Type') + colored(255, 236, 80, '"cm file.extension".') + colored(255, 216, 66, '\nIt will then auto-reload your program every time you press the save command two times in a row.'))
            return
        elif(args[0] == 'new'):
            print(colored(20, 170, 224, 'Enter File Directory/Name: '), end='')
            file = input()
            open(file, 'a')
            return
        start(args[0])
    else:
        print(colored(255, 16, 57, "Wrong Number Of Arguments"))

if(__name__ == '__main__'):
    main()
