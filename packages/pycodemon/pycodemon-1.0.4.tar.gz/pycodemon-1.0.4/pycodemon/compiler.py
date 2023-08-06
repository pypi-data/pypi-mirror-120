import os
import time
import subprocess

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
    
    os.system('cls')
    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
    time.sleep(0.25)
    os.system('cls')
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
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
                    time.sleep(0.25)
                    os.system('cls')
                    print(colored(20, 170, 224, 'Codemon finished compiling ' + os.path.basename(file) + ' successfully!'))
                    runner.run()
                    break
        time.sleep(0.03)


# def compileJava(file):
#     run = ''
#     compile = 'javac ' + file
#     path = ''
#     if(len(file.split('/')) > 1):
#         path = file.split('/')[0] + '/'

#     os.system(compile)

#     if path == '':
#         run = 'java ' + file.replace('.java', '').replace(path, '')
#     else:
#         run = 'java -cp ' + path + ' ' + file.replace('.java', '').replace(path, '')

#     os.system('cls')
#     print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
#     time.sleep(0.25)
#     os.system('cls')
#     print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
#     process = subprocess.Popen(run, shell=True)

#     changes = os.path.getmtime(file)

#     while(True):
#         if changes < os.path.getmtime(file):
#             startTime = time.time()
#             changes = os.path.getmtime(file)
#             while(startTime > time.time() - 1.25):
#                 if changes < os.path.getmtime(file):
#                     process.terminate()
#                     changes = os.path.getmtime(file)
#                     os.system(compile)
#                     os.system('cls')
#                     print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
#                     time.sleep(0.25)
#                     os.system('cls')
#                     print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
#                     process = subprocess.Popen(run, shell=True)

#         time.sleep(0.03)

# def compileNode(file):
#     path = ''
#     if(len(file.split('/')) > 1):
#         path = file.split('/')[0] + '/'

#     run = 'node ' + file
#     os.system('cls')
#     print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
#     time.sleep(0.25)
#     os.system('cls')
#     print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
#     time.sleep(0.25)
#     process = subprocess.Popen(run, shell=True)

#     changes = os.path.getmtime(file)

#     while(True):
#         if changes < os.path.getmtime(file):
#             startTime = time.time()
#             changes = os.path.getmtime(file)
#             while(startTime > time.time() - 1.25):
#                 if(changes < os.path.getmtime(file)):
#                     process.terminate()
#                     changes = os.path.getmtime(file)
#                     os.system('cls')
#                     print(colored(20, 170, 224, 'Codemon is reloading your changes...'))
#                     time.sleep(0.25)
#                     os.system('cls')
#                     print(colored(20, 170, 224, 'Codemon finished compiling ' + file.replace(path, '') + ' successfully!'))
#                     process = subprocess.Popen(run, shell=True)

#         time.sleep(0.03)
