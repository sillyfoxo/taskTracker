# importing modules we will need
import json, datetime, pathlib

#define globals
global prompt, promptInput, commandPrefix, filePrefix, workingDir, currentDir, defaultTasksDir

#declare variables
commandPrefix = 'task'
filePrefix = 'tsk'
prompt = lambda prompt : print(f"{datetime.datetime.now().strftime("%H:%M:%S")} - [PROMPT] {prompt}\n")
promptInput = lambda prompt : input(f"{datetime.datetime.now().strftime("%H:%M:%S")} - [INPUT] {prompt}\n> ")
workingDir = None
plibPath = pathlib.Path
currentDir = plibPath.cwd()
defaultTasksDir = plibPath("./tasksLists/")


class fileOperations():
    def getTasks():
        jsonFiles = []
        for fileName in pathlib.os.listdir(workingDir):
            if(fileName.startswith(filePrefix) and fileName.endswith(".json")):
                #add the files found, name + creation time
                fileCreationTime = datetime.datetime.fromtimestamp(plibPath(f"{workingDir}/{fileName}").stat().st_ctime).strftime("%D - %H:%M:%S")
                jsonFiles.append([fileName,fileCreationTime])

        return jsonFiles

    def changeDir(directory):
        global workingDir
        directoryPath = plibPath(directory)
        directory = directory.lower()
        if(directory == "current" or directory == "here"):
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
            plibPath(f"{workingDir}/{filePrefix}{name}.json").touch()
        except Exception as exception:
            prompt(f"Error creating file with error \n {exception}")
    
    def checkIfTaskExists(taskFName):
        if(jsonFName in pathlib.os.listdir(workingDir)):
            return True
        else: 
            return False

###### WIP ######
class taskParser():
    def loadTasks(taskName):
        jsonFName = filePrefix+taskName+".json"
        loadedFile = json.load(workingDir.joinpath(jsonFName).open())
        getTasks = loadedFile["tasks"]
        return getTasks
    def writeToTask(taskName):
        pass

####### ON START #######
#check for the tasksLists folder, then prompt if missing, do this everytime we start the program

### EXAMPLE 1 OF STARTING THE PROGRAM (ASK FOR DEFAULT FOLDER AND ETC.)
'''
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
'''
### PROGRAM START 2ND IMPLMENTATION

prompt('Scanning for existing folders')
for path in pathlib.os.listdir(currentDir): 
    # FETCH FOLDERS
    if (plibPath.is_dir(pathlib.Path(path)) and not path.startswith(".")): #filter out the hidden directories
        if(plibPath(path) == defaultTasksDir):
            defaultPrompt = promptInput("default folder \"tasksList/\" exists, do you want to continue using the default folder?").lower()
            if(defaultPrompt == 'yes' or defaultPrompt == '1'):
                workingDir = defaultTasksDir
            else:
                dirPrompt = promptInput("enter the directory you wish to use")
                try:
                    fileOperations.changeDir(dirPrompt)
                except Exception as e:
                    prompt("error trying to change directories")

#### PROGRAM START DIRECTORY MEMES DONE

print(taskParser.loadTasks('example1'))