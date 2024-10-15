# importing modules we will need
import json, datetime, pathlib,os

#define globals
global prompt, promptInput, commandPrefix, filePrefix, workingDir, currentDir, defaultTasksDir

#declare variables
commandPrefix = 'task'
filePrefix = 'tsk'
prompt = lambda prompt : print(f"{datetime.datetime.now().strftime("%H:%M:%S")} - [PROMPT] {prompt}")
promptInput = lambda prompt : input(f"{datetime.datetime.now().strftime("%H:%M:%S")} - [INPUT] {prompt}\n> ")
workingDir = None
workingFile = None
plibPath = pathlib.Path
currentDir = plibPath.cwd()
defaultTasksDir = currentDir.joinpath(plibPath("./tasksList/"))
state = False


class mainLib:
    class commands:
        def help():
            print(f"""
            prefix is '{commandPrefix}',
            {commandPrefix} create (task name) (optional: status, default is undone) - creates a new task
            {commandPrefix} edit (task name) (new task name) - edits task name
            {commandPrefix} list (optional: status) - lists tasks
            {commandPrefix} update (task name) (new status) - updates the task status
            {commandPrefix} remove (task name) - removes the task
            {commandPrefix} auto-remove - removes the tasks that are marked as 'done'
            quit - exits the program
            """)

        def taskCreate(name, status="undone"):
            mainLib.directoryLib.createTask(name)
            


    class directoryLib:
        def getTaskFiles():
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
                if(mainLib.parseResponse()):
                    if(directoryPath.exists()):
                        workingDir = directoryPath
                    else:
                        currentDir.joinpath(directoryPath).mkdir()
                        workingDir = directoryPath
                    prompt(f"working directory is now \n{workingDir}")
                else:
                    prompt("directory not changed")

        def createDefaultDir():
            try:
                defaultTasksDir.mkdir()
            except Exception as e:
                prompt(f"failed to create default dir with error \n {e}")

        def createTaskFile(name):
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

        def defaultDirExists():
            for path in pathlib.os.listdir(currentDir):
                if (plibPath.is_dir(pathlib.Path(path)) and not path.startswith(".")): #filter out the hidden directories
                    if(currentDir.joinpath(plibPath(path)) == defaultTasksDir):
                        return True
                    else:
                        return False

        def changeTaskFile(taskFName):
            taskFiles = mainLib.directoryLib.getTaskFiles() if (workingDir) else exit()
            for task in taskFiles:
                if(workingDir.joinpath(plibPath(filePrompt)).exists()):
                    workingFile = workingDir.joinpath(plibPath(filePrompt))
        

    ###### WIP ######
    class taskLib:
        def loadTasks(taskName):
            jsonFName = filePrefix+taskName+".json"
            loadedFile = json.load(workingDir.joinpath(jsonFName).open())
            getTasks = loadedFile["tasks"]
            return getTasks
        
        def addTask(name, state):
            if(workingFile):
                if(state in ['done','undone','in progress']):   
                    getJSON = json.load(workingDir.joinpath(workingFile).open())
                    getJSON[name] = state 
                    plibPath(workingFile).write_text(json.JSONEncoder().encode(getJSON))
                else:
                    raise Exception
            else: 
                prompt("error, no file selected")

        def removeTask(name):
            if(workingFile):
                JSONData = json.load(workingDir.joinpath(workingFile).open())
                JSONData.pop(name)
                plibPath(workingFile).write_text(json.JSONEncoder().encode(JSONData))
    
    def parseResponse(response):
        response = str(response).lower().strip()
        agreeResponse = ["yes", "1", "y"]
        if(response in agreeResponse):
            return True
        elif(response not in agreeResponse):
            for value in agreeResponse:
                if(response.count(value) > 0):
                    return True
            else:
                return False
    
    def mainApp(state):
        commands = ['create','edit',"list",'update',"remove",'auto-remove',"exit"]
        if(state):
            os.system('cls' if os.name=='nt' else 'clear')
            print(f"TASKTRACKER v0.1\nCurrent directory: {workingDir}\nTask file: {workingFile}")
            appInput = promptInput("")
            if(appInput in commands):
                pass



####### ON START #######
#check for the tasksLists folder, then prompt if missing, do this everytime we start the program
### PROGRAM START 2ND IMPLMENTATION

prompt('Scanning for existing folders')
if(mainLib.directoryLib.defaultDirExists()):
    defaultPrompt = promptInput("default folder \"tasksList/\" exists, do you want to continue using the default folder?").lower()
    if(mainLib.parseResponse(defaultPrompt)):
        workingDir = defaultTasksDir
    else:
        dirPrompt = promptInput("enter the directory you wish to use")
        try:
            mainLib.directoryLib.changeDir(dirPrompt)
        except Exception as e:
            prompt("error trying to change directories")
else:
    createFolderPrompt = promptInput("wish to create a folder called \"tasksList/\" for your tasks?")
    if(mainLib.parseResponse(createFolderPrompt)):
        mainLib.directoryLib.createDefaultDir()
    else:
        dirPrompt = promptInput("enter the directory you wish to use")
        try:
            mainLib.directoryLib.changeDir(dirPrompt)
        except Exception as e:
            prompt("error trying to change directories")

if(not workingFile):
    prompt("there are no selected files yet, listing files")
    taskFiles = mainLib.directoryLib.getTaskFiles() if (workingDir) else exit()
    for task in taskFiles:
        print(f"'{task[0].removeprefix(filePrefix).removesuffix('.json')}' created at {task[1]}")
    filePrompt = str(promptInput('select a task file to start editing'))
    filePrompt = f"{filePrefix}{filePrompt}.json"
    if(workingDir.joinpath(plibPath(filePrompt)).exists()):
        workingFile = workingDir.joinpath(plibPath(filePrompt))
        prompt(f"task list '{filePrompt}' is now selected")



mainLib.taskLib.addTask("clean house", "undone")
mainLib.taskLib.addTask("balls", "done")
mainLib.taskLib.addTask("balls2", "done")
mainLib.taskLib.addTask("balls3", "done")
mainLib.taskLib.addTask("balls4", "done")
mainLib.taskLib.addTask("balls5", "done")
mainLib.taskLib.removeTask("clean house")

print(json.JSONDecoder().decode(workingFile.read_text()))


#while True:
#    mainLib.mainApp(True)