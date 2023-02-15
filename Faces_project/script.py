# Import Libraries
from psychopy import visual, core, event
from psychopy import gui
import pandas as pd
import glob
import random

#Defining GUI
introgui=gui.Dlg(title = "Is this a face?")
introgui.addField("Participant ID:")
introgui.addField("Age:")
introgui.addField("Gender:", choices=["Female","Male","other"])
introgui.show()
if introgui.OK:
    ID=introgui.data[0]
    Age=introgui.data[1]
    Gender=introgui.data[2]
    [ID,Age,Gender]=introgui.data
elif introgui.Cancel:
    core.quit()

from psychopy import data
#defining cols
cols=["ID","Age","Gender","Stimulus", "ReactionTime", "Face","Key"]
#creating df
logfile=pd.DataFrame(columns=cols)
#Get data
date=data.getDateStr()
 #Create a Window
win=visual.Window(color="black", fullscr=True)

# Create a Text Stimulus

# Load Images
stimuli=glob.glob("stimuli/*.jpg")
#face=visual.ImageStim(win, image = "image_stim.jpg")
black=visual.ImageStim(win, image = "black.jpg")
#face_i=visual.ImageStim(win, image = "stimuli/failure.jpg")
#thing=visual.ImageStim(win, image = "stimuli/failure.jpg")
random.shuffle(stimuli)

#Intro
msg=visual.TextStim(win, text = "Welcome, press any key to continue, have a blast! Your task for today will be to decide as soon as possible whether the presented stimulus remind you of a face or not. You will be able to answer via left arrow for no and right arrow for yes")
msg.draw()
win.flip()
event.waitKeys()
# Loop Through Trials
for stimulus in stimuli:
    msg_2=visual.TextStim(win, text = "Left arrow = NO, Right arrow = YES")
    pic=visual.ImageStim(win,stimulus)
    # Draw the Stimuli
    pic.draw()
    msg_2.draw()
    win.flip()
    #define clock watch
    stopwatch=core.Clock()
    # Reset and Start the Clock
    stopwatch.reset()
    #key recording
    key=event.waitKeys(keyList = ["left","right","escape"])
    #RT
    reaction_time = stopwatch.getTime()
    
    resp_key=event.getKeys(keyList = ("left","right"), timeStamped=False)
    print(key)
    #if resp_key==["left"] or ["right"]:
     #   event.getKeys()
    #escape
    print(reaction_time)
    if key[0] == "escape":
        core.quit()
    if key==["left"] and stimulus[-7]=="F":
        stopwatch = core.Clock()
        black.draw()
    else:
        black.draw()
    win.flip()
    core.wait(1.5)
    
    #data saving
    logfile=logfile.append({
        "Data": date,
        "ID": ID, 
        "Age": Age,
        "Gender": Gender,
        "Stimulus": stimulus,
        "ReactionTime" : reaction_time,
        "Key" : key
        },ignore_index=True)


#logfile name
logfile_name="logfiles/logfile_{}_{}.csv".format(ID,date)

#Saving the log file
logfile.to_csv(logfile_name)