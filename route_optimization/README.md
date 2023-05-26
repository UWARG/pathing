Steps to run path optimization on your own computer
==================================================

1. Create a virtual environment using the command "python -m venv venv"

2. Activate the virtual environment using the command ".\venv\Scripts\activate" (This command is for Windows)

3. Install the required libraries by running the command "pip install -r requirements.txt" (Note that if there are still import errors, you can run "pip install <library_name> to install it)

4. Run "python or_tools_algo.py" and the QR scanner should pop up. This will return a string of a list of flight paths.
    
   - In or_tools_algo.py, MAX_DISTANCE is the distance the drone can fly from takeoff to landing
   - Inside main in or_tool_algo.py, flight_paths = calculate_route(1, create_data_model()) (line 199) returns a list of flight paths that completes all the routes given.
   - Below that (line 202) flight_paths.sort(key=lambda p: p.routes_completed / p.distance_flown if p.distance_flown > 0 else 0, reverse=True) sorts the flight paths based on efficiency. You can change this line pretty easily to sort it based on which paths give the greatest points (flight_paths.sort(key=lambda p: p.total_points, reverse=True)) or whatever else the drone needs
   - The for loop at the end of main() just gets enough flight paths so that we complete 50% of the routes.

   - There might be a case where one of the flight paths returned ends with like ['Alpha', 'Alpha'] just ignore the second Alpha :D

# Competition 2023

Code is modified to output both routes (for email) and waypoints (for Mission Planner). Weights were adjusted to penalize routes far from the launch point and long routes. However, the adjustments were not made correctly before the submission deadline.

`emailing.py` contains automated email (Gmail) code from:
* [https://developers.google.com/gmail/api/quickstart/python](https://developers.google.com/gmail/api/quickstart/python)
* [https://developers.google.com/gmail/api/guides/sending](https://developers.google.com/gmail/api/guides/sending)

`distances.py` contains code to create a CSV file of distances for manual route optimization.
