# connection_finder_prague
Python implementation of route based public transport routing algorithm - RAPTOR in form of CLI app myraptor
## Introduction
The  app implements the Raptor routing algorithm using public transit data in GTFS format. It uses data on Prague public transport.
## Algorithm
The connection search algorithm used in this project is based on RAPTOR-Round (bAsed Public Transit Optimized Router) algorithm (available at: https://renatowerneck.files.wordpress.com/2016/06/dpw14-raptor.pdf). The algorithm is NOT based on graph.
Instead, it operates in rounds, one per transfer, and computes arrival times by traversing every route (such as an underground line) at most once per round.

The algorithm works as follow:
For allowed number of transfers, it runs loop with following steps:  
      A) Get all currently reachable stops (initially, just the start stop) and find associated routes and for each route the soonest available trip (dependent on              arrival time to the stop).  
      B) For all stops reachable by previously found trip, use arrival and departure data to figure out how long to reach other stops in the trip. The reached stops             are marked as reachable for next round.  

Alogrithm used in this project doesn't include footsteps, transfer time, and timetable dependent on particular dates (e.g.weekends).
## Data
Data used in this project are GTFS data publicly available at: https://opendata.iprpraha.cz/DPP/JR/jrdata.zip. Data are processed with jupyter notebook, and saved in format of Timetable object in file timetable_metro_tram_bus.csv. Due to large amount of data needed to be processed, the app uses preprocessed data.

## How to use Myraptor
The CLI app requires following inputs:
1) start_stop and target_stop must be names of the stops in the exactly same format used in GTFS. If you enter wrong format of stop name, all possible stops will be listed. 
2) start_time must be entered in form of HH:MM:SS. (TODO: problem with encoding, to be resolved - If not working, please try to use english keybord)
3) allowed_number_of_transfers must be in form of integer (1:10)

Input

Please enter start station: Florenc  
Please enter target station: Motol  
Please enter start time in form HH:MM:SS   :   13:33:33  
Please enter maximum allowed transfers in form of number in range (0,10): 2  

Output

stop: Florenc,  departure time: 13:34:20,  take line: B  
stop: Anděl,  arrival time: 13:41:20,  departure time: 13:43:00,  change to line: 9  
stop: Motol,  arrival time: 13:55:00  

## Technologies
The project is written in Python 3.9

## Instalation
