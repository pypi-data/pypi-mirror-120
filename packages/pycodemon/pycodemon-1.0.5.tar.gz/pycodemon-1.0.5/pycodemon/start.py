from pycodemon.compiler import *

def start(filename):
    prefix = ''
    if(not os.path.exists(filename)):
        print(colored(255, 15, 67, 'That Directory Does Not Exist'))
        exit()

    if(not len(filename.split('.')) > 1):
        print(colored(255, 15, 67, 'Please Specify The File Type') + colored(237, 140, 43, ('(ex. file.py)')))
        exit()
    else:
        prefix = filename.split('.')[1]

    if(prefix == 'py'):
        compileGeneric(filename, python_runner)
    elif(prefix == 'java'):
        compileGeneric(filename, java_runner)
    elif(prefix == 'js'):
        compileGeneric(filename, node_runner)
    else:
        print(colored(255, 216, 66, 'This File Type Is Not Supported.'))
