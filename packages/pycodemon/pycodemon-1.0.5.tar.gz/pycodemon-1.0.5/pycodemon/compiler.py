import os
from platform import system
import time
import subprocess

clear = 'clear'
ops = system()
if(ops == 'Windows'):
    clear = 'cls'

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


class runner():
    def __init__(self, file):
        self.dirname = os.path.dirname(file)
        self.basename = os.path.basename(file)
        self.file = file
        self.process = None
    def run(self):
        assert False , "unimplemented in base class"
    def terminate(self):
        assert self.process, "process is not initialized!"
        self.process.terminate()

class python_runner(runner):
    def run(self):
        run = "python "+self.file
        self.process = subprocess.Popen(run, shell=True)

class node_runner(runner):
    def run(self):
        run = "node "+self.file
        self.process = subprocess.Popen(run, shell=True)

class java_runner(runner):
    def run(self):
        compile = "javac "+self.file
        os.system(compile)
        
        if self.dirname == '':
            run = 'java ' + self.basename
        else:
            run = 'java -cp ' + self.dirname + ' ' + self.basename

        self.process = subprocess.Popen(run, shell=True)

# per language runners



def compileGeneric(file, per_language_runner):
    
    os.system(clear)
    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
    time.sleep(0.25)
    os.system(clear)
    print(colored(20, 170, 224, 'Codemon finished compiling ' + os.path.basename(file) + ' successfully!'))
    time.sleep(0.25)
    
    runner = per_language_runner(file)
    runner.run()
    changes = os.path.getmtime(file)

    while(True):
        if changes < os.path.getmtime(file):
            startTime = time.time()
            changes = os.path.getmtime(file)
            while(startTime > time.time() - 1.25):
                if(changes < os.path.getmtime(file)):
                    runner.terminate()
                    changes = os.path.getmtime(file)
                    os.system(clear)
                    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
                    time.sleep(0.25)
                    os.system(clear)
                    print(colored(20, 170, 224, 'Codemon finished compiling ' + os.path.basename(file) + ' successfully!'))
                    runner.run()
                    break
        time.sleep(0.03)
