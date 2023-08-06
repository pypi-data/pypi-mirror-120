import os
import time
import subprocess

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def compilePython(file):
    path = ''
    if(len(file.split('/')) > 1):
        path = file.split('/')[0] + '/'

    run = 'python ' + file
    os.system('cls')
    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
    time.sleep(0.25)
    os.system('cls')
    print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
    time.sleep(0.25)
    process = subprocess.Popen(run, shell=True)

    changes = os.path.getmtime(file)

    while(True):
        if changes < os.path.getmtime(file):
            startTime = time.time()
            changes = os.path.getmtime(file)
            while(startTime > time.time() - 0.75):
                if(changes < os.path.getmtime(file)):
                    process.terminate()
                    changes = os.path.getmtime(file)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
                    time.sleep(0.25)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
                    process = subprocess.Popen(run, shell=True)

        time.sleep(0.1)


def compileJava(file):
    run = ''
    compile = 'javac ' + file
    path = ''
    if(len(file.split('/')) > 1):
        path = file.split('/')[0] + '/'

    os.system(compile)

    if path == '':
         run = 'java ' + file.replace('.java', '').replace(path, '')
    else:
        run = 'java -cp ' + path + ' ' + file.replace('.java', '').replace(path, '')

    os.system('cls')
    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
    time.sleep(0.25)
    os.system('cls')
    print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
    process = subprocess.Popen(run, shell=True)

    changes = os.path.getmtime(file)

    while(True):
        if changes < os.path.getmtime(file):
            startTime = time.time()
            changes = os.path.getmtime(file)
            while(startTime > time.time() - 0.75):
                if changes < os.path.getmtime(file):
                    process.terminate()
                    changes = os.path.getmtime(file)
                    os.system(compile)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
                    time.sleep(0.25)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
                    process = subprocess.Popen(run, shell=True)

        time.sleep(0.1)

def compileNode(file):
    path = ''
    if(len(file.split('/')) > 1):
        path = file.split('/')[0] + '/'

    run = 'node ' + file
    os.system('cls')
    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
    time.sleep(0.25)
    os.system('cls')
    print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
    time.sleep(0.25)
    process = subprocess.Popen(run, shell=True)

    changes = os.path.getmtime(file)

    while(True):
        if changes < os.path.getmtime(file):
            startTime = time.time()
            changes = os.path.getmtime(file)
            while(startTime > time.time() - 0.75):
                if(changes < os.path.getmtime(file)):
                    process.terminate()
                    changes = os.path.getmtime(file)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
                    time.sleep(0.25)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
                    process = subprocess.Popen(run, shell=True)

        time.sleep(0.1)
