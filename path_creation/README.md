Steps to run path optimization on your own computer
==================================================

1. Create a virtual environment using the command "python -m venv venv"

2. Activate the virtual environment using the command ".\venv\Scripts\activate" (This command is for Windows)

3. Install the required libraries by running the command "pip install -r requirements.txt" (Note that if there are still import errors, you can run "pip install <library_name> to install it)

4. Change the filename variable in PathOptimization.py and waypoint_uploadFINAL.py (Use the absolute file path or else Mission Planner can't read it)

How to run Path Optimization Task 1 for Competition
===================================================

### In Mission Planner ... ###

1. In Mission Planner on the bottom left there is an option named Scripts (if you can't see it use the scroll function)

2. Click on the Select Script button and choose the python file "waypoint_uploadFINAL.py"

3. Click Run Script (Note that it should be printing out Empty Line. Essentially what is happening is the code is checking the paths.txt file. If the file is empty it prints out empty line. However, once the QR code is scanned it will update paths.txt with the waypoints. When a non-empty line is detected waypoint_uploadFINAL.py will stop reading the text file and upload the waypoints to Mission Planner)

### In VS Code ###

1. In VSCode navigate to the path_optimization directory and run the command "python PathOptimization.py" (This will boot up the QR Scanner)

2. Now simply scan the QR code and the waypoints should be sent to Mission Planner :)

Notes
=====

1. When I upload the points to Mission Planner I run into an error saying "SystemError: Timeout on read - setWP". I suspect that this is because the hardware is not plugged in on my computer. This should be resolved when everything is set up on Icarus for competition.

# Competition 2023

Only the files below were used for the 2022-2023 competition.

`waypoint_current_location.py` is a script loaded into Mission Planner to get the drone's current location. The current location is currently unused.

## Task 1

`waypoint_file_write.py` creates a path for Mission Planner, respecting flight boundaries.

`waypoint_boundary.py` creates a fence for Mission Planner, to indicate the restricted area.

There was no time to integrate diversion to create a new path before the flight window.

## Task 2

Task 2 route generation is currently in [this repository](https://github.com/Chrisytz/Task2).

`waypoint_manual.py` creates a path for Mission Planner with included takeoff and hover commands from manually hardcoded waypoint names. At the flight window, only basic waypointing was implemented, not takeoff and hover commands.
