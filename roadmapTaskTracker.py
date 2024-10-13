# importing modules we will need
import json, datetime, pathlib

#define globals
global prompt, promptInput, commandPrefix, filePrefix, workingDir, currentDir, tasksDir


#declare variables
commandPrefix = 'task'
filePrefix = 'tsk'
prompt = lambda prompt : print(f"{datetime.datetime.now().strftime("%H:%M:%S")} - [PROMPT] {prompt}\n")
promptInput = lambda prompt : input(f"{datetime.datetime.now().strftime("%H:%M:%S")} - [INPUT] {prompt}\n> ")
workingDir = None
currentDir = pathlib.Path.cwd()
tasksDir = pathlib.Path("./tasksLists/")

class fileOperations():
    def getTasks():
        jsonFiles = []
        for fileName in pathlib.os.listdir(workingDir):
            if(fileName.startswith(filePrefix) and fileName.endswith(".json")):
                #add the files found, name + creation time
                fileCreationTime = datetime.datetime.fromtimestamp(pathlib.Path(f"{workingDir}/{fileName}").stat().st_ctime).strftime("%D - %H:%M:%S")
                jsonFiles.append([fileName,fileCreationTime])

        return jsonFiles

    def changeDir(directory):
        global workingDir
        directoryPath = pathlib.Path(directory)
        directory = directory.lower()
        if(directory == "folder"):
            workingDir = tasksDir
        elif(directory == "current" or directory == "here"):
            workingDir = currentDir
        else:
            changeDirPrompt = str(promptInput(f"are you sure you want to use directory:\n\"{currentDir.joinpath(directoryPath)}\"")).lower()
            if(changeDirPrompt == 'yes' or changeDirPrompt == 'y' or changeDirPrompt == '1'):
                if(directoryPath.exists()):
                    workingDir = directoryPath
                else:
                    currentDir.joinpath(directoryPath).mkdir()
                    workingDir = directoryPath
                prompt(f"working directory is now \n{workingDir}")
            else:
                prompt("directory not changed")
                    
    def createTask(name):
        try:
            prompt(f"creating file at {workingDir}")
            pathlib.Path(f"{workingDir}/{filePrefix}{name}.json").touch()
        except Exception as exception:
            prompt(f"Error creating file with error \n {exception}")
    
class taskParser():
    pass

####### ON START #######
#check for the tasksLists folder, then prompt if missing, do this everytime we start the program

if(not pathlib.Path.exists(tasksDir)):
    folderPrompt = promptInput("do you want to create a folder for your tasks list?")
    if ('yes' in folderPrompt.lower() or "1" in folderPrompt):
        tasksDir.mkdir()
        prompt(f"folder taskLists created at {tasksDir}")
        workingDir = tasksDir
    else:
        prompt("program will create the tasks in the current directory.")
        workingDir = currentDir
else:
    match promptInput("default folder exists, do you want to continue using the folder?").lower():
        case "yes":
            workingDir = tasksDir
        case "no":
            fileOperations.changeDir(str(promptInput(f"state the directory you want to use: it will be created at {currentDir}")))


fileOperations.createTask("example1")
fileOperations.changeDir("uwuTasks")
fileOperations.createTask("owo")
