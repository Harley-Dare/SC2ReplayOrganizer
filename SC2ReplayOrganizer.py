import shutil
import os
import sc2reader
from tkinter import filedialog

# Brings up GUI to select folder to organize
def setPath():
    print('Please choose a folder containing the SC2 replay files you wish to organize. \nThis program will go through this folder and all subfolders and organize the 1v1 sc2 replay files\n')
    folder = filedialog.askdirectory()
    return folder

# Walk through folder and subfolders, return list of filepaths.
def gatherReplayFilePaths(folder):
    fileList = []
    for folderName, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".SC2Replay"):
                file = folderName + '/' + filename
                fileList.append(file)
    return fileList

# Loads the replay when given a filepath and load level (int)
def loadReplay(file, loadLevel):
    replay = sc2reader.load_replay(file, load_level = loadLevel)
    return replay

# Finds the two races and returns the matchup. Also adds players to a set
def findMatchUp(replay):
    firstFound = False
    # # firstRace = ""
    secondRace = ""
    playerNumber = 1
    for player in replay.players:
        if player.pick_race == "Zerg" and playerNumber == 2:
            secondRace = "Zerg"
        elif player.pick_race == "Protoss" and playerNumber == 2:
            secondRace = "Protoss"
        elif player.pick_race == "Terran" and playerNumber == 2:
            secondRace = "Terran"
        if player.pick_race == "Zerg" and playerNumber == 1:
            firstRace = "Zerg"
            playerNumber += 1
        elif player.pick_race == "Protoss" and playerNumber == 1:
            firstRace = "Protoss"
            playerNumber += 1
        elif player.pick_race == "Terran" and playerNumber == 1:
            firstRace = "Terran"
            playerNumber += 1
    matchup = defineMatchup(firstRace, secondRace, replay)
        
    return matchup

# Takes two race inputs and returns the matchup. 
def defineMatchup(firstRace, secondRace, replay):
    if (firstRace == "Zerg" and secondRace == "Terran") or (firstRace == "Terran" and secondRace == "Zerg"):
        return "ZvT"
    if (firstRace == "Zerg" and secondRace == "Protoss") or (firstRace == "Protoss" and secondRace == "Zerg"):
        return "ZvP"
    if (firstRace == "Terran" and secondRace == "Protoss") or (firstRace == "Protoss" and secondRace == "Terran"):
        return "TvP"
    if (firstRace == "Terran" and secondRace == "Terran"):
        return "TvT"
    if (firstRace == "Protoss" and secondRace == "Protoss"):
        return "PvP"
    if (firstRace == "Zerg" and secondRace == "Zerg"):
        return "ZvZ"

# Makes matchup specific directories in a user specified path
def createMatchupSpecificDirectories():
    print("Please select where you would like the matchup specific directories to go")
    folder = filedialog.askdirectory()
    try:
        os.mkdir(os.path.join(folder, "ZvZ"))
    except:
        print("ZvZ is already an existing directory, no new directory made")
    try:
        os.mkdir(os.path.join(folder, "TvT"))
    except:
        print("TvT is already an existing directory, no new directory made")
    try:
        os.mkdir(os.path.join(folder, "PvP"))
    except:
        print("PvP is already an existing directory, no new directory made")
    try:
        os.mkdir(os.path.join(folder, "ZvT"))
    except:
        print("ZvT is already an existing directory, no new directory made")
    try:
        os.mkdir(os.path.join(folder, "ZvP"))
    except:
        print("ZvP is already an existing directory, no new directory made")
    try:
        os.mkdir(os.path.join(folder, "TvP"))
    except:
        print("TvP is already an existing directory, no new directory made")
    return folder

# Takes replay file path and currentMatchup and calls functions to copy replays into the correct folder
def copyToMatchupSpecificDirectory(file, matchup, organizedFolderPath):
    path = os.path.join(organizedFolderPath, matchup)
    try:
        if matchup == "ZvT":
            shutil.copy(file, path)
        elif matchup == "ZvP":
            shutil.copy(file, path)
        elif matchup == "TvP":
            shutil.copy(file, path)
        elif matchup == "PvP":
            shutil.copy(file, path)
        elif matchup == "ZvZ":
            shutil.copy(file, path)
        elif matchup == "TvT":
            shutil.copy(file, path)
    except shutil.SameFileError:
        print("Found duplicate file, ignoring and moving on")
        pass

loadLevel = 2
mainFolderPath = setPath()
replayFilePaths = gatherReplayFilePaths(mainFolderPath)
organizedFolderPath = createMatchupSpecificDirectories()

# Organize by Matchup
for file in replayFilePaths:
    replay = loadReplay(file, loadLevel)
    if len(replay.players) == 2:
        currentMatchup = findMatchUp(replay)
        copyToMatchupSpecificDirectory(file, currentMatchup, organizedFolderPath)

        




