import matplotlib.pyplot as plt

from pyorbital.orbital import Orbital
from datetime import datetime, timedelta
from sys import argv
from requests import get, exceptions
from math import radians, tan, sin, cos
from numpy import arange, float32, float64
from os.path import isfile
from prettytable import PrettyTable
from pathlib import Path


from .config import *
from .TLE import update



__all__ = [
    "getCoords",
    "getSatellitePasses",
    "getSchedule",
    "degreesToDegreesAndMinutes",
    "getCoordsWithC4STrack",
    "getCoordsWithL2STrack",
    "generateC4STrack",
    "generateL2STrack",
    "findPasses",
    "sats",
    "version"
]



# Function that gets the user's coordinates by his ip
# Out:
#   float float lon, float lat, float alt
#
# If there is an error: lon=0, lat=0, alt=0
def getCoords():
    try:
        print( "Get coordinates by IP.." )
        query = get("http://ip-api.com/json").json()
        
        lat = query['lat']
        lon = query['lon']

        # temporary return only elevation by coordinates
        query = get(f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}').json()
        alt = query['results'][0]['elevation']
    
    except exceptions.ConnectionError:
        print('Error when get coordinates')
        print("No internet connection\n")
        lat = 0
        lon = 0
        alt = 0

    except Exception as e:
        print('Error when get coordinates')
        print(str(e))
        lat = 0
        lon = 0
        alt = 0

    print(f"Youre coordinates: {lon} {lat} {alt}m\n")
    
    return lon, lat, alt/1000


# Function that calculates satellite passes by input parametres
# In:
#   str satellite, datetime start, int length, float lon, float lat, float alt, float tol, int horizon
# Out:
#   datetime start, datetime end, datetime apogee
def getSatellitePasses(start, length, satellite, lon, lat, alt, tol = 0.001, horizon=defaultHorizon): 
    update(showLog=False)

    orb = Orbital(satellite, join( tlePath, "tle.txt" ) )

    return orb.get_next_passes(start, length, lon, lat, alt, tol, horizon)


# Function that makes up the schedule, according to the parameters
# In:
#   str output, datetime start, int timeZone, int length, float lon, float lat, float alt, float tol, int horizon, bool printTable
# Out:
#   PrettyTable table
# Saves the schedule in "output" and prints it if necessary
# Not the best implementation but there is no other one yet
# It does not take into account time zone curves, since I am too lazy to saw the implementation for the sake of several points of the planet
def getSchedule(output, start, timeZone, length, lon, lat, alt, tol = 0.001, horizon=defaultHorizon, printTable=True):
    update(showLog=False)

    passes = {}
    allPasses = []

    th = ["Satellite", "DateTime", "Azimuth", "Elevation"]
    td = []

    # Iterating through all the passes
    for satellite in sats.values():
        pas = getSatellitePasses(start, length, satellite, lon, lat, alt, tol = tol,  horizon=horizon)
        
        # Flights of a specific satellite
        passes[satellite] = pas

        # All passes
        for i in pas:
            allPasses.append(i)

    # Generate table
    for onePass in sorted(allPasses):
        satName = ''

        # Going through the list of satellites
        for satellite in sats.values():
            # If the selected span corresponds to a satellite
            if onePass in passes[satellite]:
                satName = satellite
                break

        orb = Orbital(satellite, join( tlePath, "tle.txt" ) )

        
        # if apogee > minApogee
        if orb.get_observer_look(onePass[2], lon, lat, alt)[1] >= minApogee:
            td.append([satName, (onePass[0] + timedelta(hours=timeZone)).strftime("%Y.%m.%d %H:%M:%S"), *map( lambda x: round(x, 2), orb.get_observer_look(onePass[0], lon, lat, alt)) ])
            td.append([satName, (onePass[2] + timedelta(hours=timeZone)).strftime("%Y.%m.%d %H:%M:%S"), *map( lambda x: round(x, 2), orb.get_observer_look(onePass[2], lon, lat, alt)) ])
            td.append([satName, (onePass[1] + timedelta(hours=timeZone)).strftime("%Y.%m.%d %H:%M:%S"), *map( lambda x: round(x, 2), orb.get_observer_look(onePass[1], lon, lat, alt)) ])
            td.append([" ", " ", " ", " "])
    
    table = PrettyTable(th)

    # Adding rows to tables
    for i in td:
        table.add_row(i)

    start += timedelta(hours=timeZone)
    stop = start + timedelta(hours=length) + timedelta(hours=timeZone)

    # Generate schedule string
    schedule = f"Satellits Schedule / LorettOrbital {version}\n\n"
    schedule += f"Coordinates of the position: {round(lon, 4)}° {round(lat, 4)}°\n"
    schedule += f"Time zone: UTC {'+' if timeZone >= 0 else '-'}{abs(timeZone)}:00\n"
    schedule += f"Start: {start.strftime('%Y.%m.%d %H:%M:%S')}\n"
    schedule += f"Stop:  {stop.strftime('%Y.%m.%d %H:%M:%S')}\n"
    schedule += f"Minimum Elevation: {horizon}°\n"
    schedule += f"Minimum Apogee: {minApogee}°\n"
    schedule += f"Number of passes: {len(td)//4}\n\n"
    schedule += table.get_string()
        
    if printTable:
        print()
        print(schedule)

    try:
        with open(output, 'w') as file:
            file.write(schedule)

    except Exception as e:
        print("ERROR:", e)

    return table


# Function that translates coordinates from the spherical to the Cartesian coordinate system (a, e, F) --> (x, y)  
# (The central reflection is taken into account)
# In:
#   float azimuth, float elevation, float mirrorFocus ( In degrees and meters )
# Out:
#   float x, float y
def sphericalToDecart(azimuth, elevation, mirrorFocus=defaultFocus):
    # tan(90') does not exist, at this moment the satellite is at the zenith above us
    if elevation == 90:
        return 0, 0

    azimuth = radians( (azimuth + azimuthCorrection) % 360 )
    elevation = radians(elevation)

    
    y = -(mirrorFocus / tan(elevation)) * cos(azimuth) 
    x = -(mirrorFocus / tan(elevation)) * sin(azimuth)
    
    return x, y


# A function that translates angular coordinates to the form degrees:minutes (a, e) --> (a:m, e:m)  
# In:
#   float azimuth, float elevation ( In degrees )
# Out:
#   str azimuth:minutes, str elevation:minutes
#
# Returns False if incorrect data is given
def degreesToDegreesAndMinutes(azimuth, elevation):
    typeAz = type(azimuth)
    if typeAz == float or typeAz == float32 or typeAz == float64:
        minutes = azimuth * 60
        degrees = minutes // 60
        minutes %= 60
        
        azimuthM = f"{int(degrees):03}:{int(minutes):02}"

    elif typeAz == int:
        azimuthM = f"{azimuth:03}:00"

    else:
        return False
    

    typeEl = type(elevation)
    if typeEl == float or typeEl == float32 or typeEl == float64:
        minutes = elevation * 60
        degrees = minutes // 60
        minutes %= 60
        
        elevationM = f"{int(degrees):03}:{int(minutes):02}"

    elif typeEl == int:
        elevationM = f"{elevation:03}:00"
    
    else:
        return False

    return azimuthM, elevationM


# Function that draws the path of the irradiator on the pyplot scheme  
# In:
#   float coordsX[], float coordsY[], float mirrorRadius, str satellite, str start, bool save, bool show ( numbers in meters )
# Out:
#   None
def printAndSavePlotTrack(coordsX, coordsY, mirrorRadius=defaultRadius, satellite="Untitled", start="", currentPath="", save=True, show=True):
    if save or show:
        ax=plt.gca()
        ax.set_aspect('equal', adjustable='box')

        Path( join(currentPath, "tracksSchemes") ).mkdir(parents=True, exist_ok=True)

        # Plot mirror
        circle = plt.Circle((0, 0), mirrorRadius, color=mirrorCircleColor)
        ax.add_patch(circle)

        # Set window title
        fig = plt.figure(1)
        fig.canvas.manager.set_window_title(satellite + "   " + start)

        # Generate OX and OY Axes
        steps = list(round(i, 1) for i in arange(-mirrorRadius, mirrorRadius + 0.1, 0.1))

        plt.title(satellite + "   " + start)

        # Plot OX and OY Axes
        plt.plot( [0]*len(steps), steps, '--k' )
        plt.plot( steps, [0]*len(steps), '--k' )

        # Plot track
        plt.plot(coordsX, coordsY, '-.r')

        # Plot start and end points
        plt.plot( coordsX[0], coordsY[0], ".b")
        plt.plot( coordsX[-1], coordsY[-1], ".r")

        # Plot north
        plt.plot( 0, mirrorRadius, "^r")

        if save:
            fileName = f"{satellite.replace(' ', '-')}_{start.replace('   ', '-').replace(':', '-')}.png"
            plt.savefig( join(currentPath, "tracksSchemes", fileName) )

        if show:
            from threading import Thread
            Thread(target=plt.show).start()
            #plt.show()


# Function that reads coordinates from the track-file Copter4Space 
# In:
#   str filePath, bool printTrack, bool saveTrack
# Out:
#   str times[], float coordsX[], float coordsY[]
def getCoordsWithC4STrack(filePath, currentPath, printTrack=True, saveTrack=True):
    times = []
    coordsX = []
    coordsY = []
    
    # Let's imagine that this is a "dirty" call
    #lines = open(filePath).readlines()

    with open(filePath) as file:
        lines = file.readlines()

    satellite = lines[0].split(" ", 1)[1].strip()
    startTime = lines[1].split(":", 1)[1].strip().replace("   ", " ")

    lines = lines[6:]

    print("Time:", "X:", "Y:", sep="\t\t")

    # Reading track steps
    for i in lines:
        strTime, azimuth, elevation, x, y = i.strip().split("\t\t")

        times.append(strTime)
        coordsX.append(float(x))
        coordsY.append(float(y))

        print(strTime, x, y, sep="\t\t")

    if printTrack or saveTrack:
        printAndSavePlotTrack(coordsX, coordsY, satellite=satellite, start=startTime, currentPath=currentPath, show=printTrack, save=saveTrack)

    return times, coordsX, coordsY


# Function that reads coordinates from the track-file Link2Space 
# In:
#   str filePath, bool printTrack, bool saveTrack
# Out:
#   str times[], float coordsX[], float coordsY[]
def getCoordsWithL2STrack(filePath, currentPath, printTrack=True, saveTrack=True):
    times = []
    coordsX = []
    coordsY = []

    # Let's imagine that this is a "dirty" call
    #lines = open(filePath).readlines()
    
    with open(filePath) as file:
        lines = file.readlines()
    
    satellite = lines[0].split(" ", 1)[1].strip()
    startTime = lines[1].split(":", 1)[1].strip().replace("   ", " ")

    lines = lines[6:]

    # Reading track steps
    for i in lines:
        strTime, azimuth, elevation = i.split("   ")

        # Convert degrees:minutes to degrees
        azimuth = round(float(azimuth.split(":")[0]) + float(azimuth.split(":")[1])/60, 2)
        elevation = round(float(elevation.split(":")[0]) + float(elevation.split(":")[1])/60, 2)
        
        # Convert degrees to Cartesian coords
        coords = sphericalToDecart(azimuth, elevation, defaultFocus)

        times.append(strTime)
        coordsX.append(coords[0])
        coordsY.append(coords[1])

        string = '{}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'.format(strTime, azimuth, elevation, coords[0], coords[1])
        print(string, sep="\t\t", end="")
    
    if printTrack or saveTrack:
        printAndSavePlotTrack(coordsX, coordsY, satellite=satellite, start=startTime, currentPath=currentPath, show=printTrack, save=saveTrack)

    return times, coordsX, coordsY


# Function that generates the track-file Copter4Space
# In:
#   str satellite, Turple satPass, bool printTrack, bool saveTrack
# Out:
#   str times[], float coordsX[], float coordsY[]
def generateC4STrack(satellite, satPass, lon, lat, alt, currentPath, printTrack=True, saveTrack=True):

    update(showLog=False)

    orb = Orbital(satellite, join( tlePath, "tle.txt" ) )
    
    Path( join(currentPath, "tracks") ).mkdir(parents=True, exist_ok=True)

    fileName = f"{satellite.replace(' ', '-')}_C4S_{satPass[0].strftime('%Y-%m-%dT%H-%M')}.txt"

    with open( join(currentPath, "tracks", fileName), "w") as file: 
        
        print( "Pass duration:")
        print( str((satPass[1]-satPass[0])).rsplit('.', 1)[0] )

        times = []
        coordsX = []
        coordsY = []

        startTime = satPass[0].strftime('%Y-%m-%d   %H:%M:%S') + " UTC"

        # Write metadata
        file.write(f"Satellite: {satellite}\n")
        file.write(f"Start date & time: {startTime}\n")
        file.write(f"Orbit: {orb.get_orbit_number(satPass[0])}\n")
        file.write("Time(UTC)\t\tAzimuth(d)\tElevation(d) X(m)\t\tY(m)\n\n")

        # Generating track steps
        for i in range((satPass[1] - satPass[0]).seconds):
        
            dateTimeForCalc = satPass[0] + timedelta(seconds=i)
            strTime = dateTimeForCalc.strftime("%H:%M:%S")

            # Convert degrees to Cartesian coords
            sphCoords = orb.get_observer_look(dateTimeForCalc, lon, lat, alt)
            coords = sphericalToDecart(*sphCoords, defaultFocus)

            times.append(strTime)
            coordsX.append(coords[0])
            coordsY.append(coords[1])

            string = '{}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\t\t{:.2f}\n'.format(strTime, sphCoords[0], sphCoords[1], coords[0], coords[1])
            file.write(string)

            print(string, end="")

    if printTrack or saveTrack:
        printAndSavePlotTrack(coordsX, coordsY, satellite=satellite, start=startTime, currentPath=currentPath, show=printTrack, save=saveTrack)

    return times, coordsX, coordsY


# Function that generates the track-file Link2Space
# In:
#   str satellite, Turple satPass, bool printTrack, bool saveTrack
# Out:
#   str times[], str azimuth:minutes[], str elevation:minutes[]
def generateL2STrack(satellite, satPass, lon, lat, alt, currentPath, printTrack=True, saveTrack=True):

    update(showLog=False)

    orb = Orbital(satellite, join( tlePath, "tle.txt" ) )

    Path( join(currentPath, "tracks") ).mkdir(parents=True, exist_ok=True)

    fileName = f"{satellite.replace(' ', '-')}_L2S_{satPass[0].strftime('%Y-%m-%dT%H-%M')}.txt"

    with open( join(currentPath, "tracks", fileName), "w") as file:

        print( "Pass duration:")
        print( str((satPass[1]-satPass[0])).rsplit('.', 1)[0] )

        times = []
        coordsX = []
        coordsY = []
        sphCoordsAZ = []
        sphCoordsEL = []

        startTime = satPass[0].strftime('%Y-%m-%d   %H:%M:%S') + " UTC"

        # Write metadata
        file.write(f"Satellite: {satellite}\n")
        file.write(f"Start date & time: {startTime}\n")
        file.write(f"Orbit: {orb.get_orbit_number(satPass[0])}\n")
        file.write("Time (UTC)   Azimuth (deg:min)   Elevation (deg:min)\n\n")

        # Generating track steps
        for i in range((satPass[1] - satPass[0]).seconds):
        
            dateTimeForCalc = satPass[0] + timedelta(seconds=i)
            strTime = dateTimeForCalc.strftime("%H:%M:%S")

            # Convert degrees to degrees:minutes
            observerLook =  orb.get_observer_look(dateTimeForCalc, lon, lat, alt)
            sphCoords = degreesToDegreesAndMinutes(*observerLook)
            # Convert degrees to Cartesian coords for create a plot
            coords = sphericalToDecart( *observerLook, defaultFocus)

            times.append(strTime)
            coordsX.append(coords[0])
            coordsY.append(coords[1])            
            sphCoordsAZ.append(sphCoords[0])
            sphCoordsEL.append(sphCoords[1])

            string = f"{strTime}   {sphCoords[0]}   {sphCoords[1]}\n"
            file.write(string)

            print(string, end="")
        
    if printTrack or saveTrack:
        printAndSavePlotTrack(coordsX, coordsY, satellite=satellite, start=startTime, currentPath=currentPath, show=printTrack, save=saveTrack)

    return times, sphCoordsAZ, sphCoordsEL


# Maybe there will be another more convenient format
def generateNeboscopeTrack(satellite, satPass, printTrack=True, saveTrack=True):
    ...

def getCoordsWithNeboscopeTrack(filePath, printTrack=True, saveTrack=True):
    ...

def convertL2SToC4STrack():
    ...

def convertC4SToL2STrack():
    ...


def findPasses(satellite, lon, lat, alt, length=30, currentPath="", printTrack=True, saveTrack=True):        

    print(f"Passes over the next {length} hours for {satellite}\n")
    print("UTC time now:", datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S"), end="\n\n")

    count = 1

    update(showLog=False)
    
    orb = Orbital(satellite, join( tlePath, "tle.txt" ) )
    
    # Print satellite passes in the format:
    # UTC time is used!
    # 1. datetime start         datetime end         datetime apogee    apogee elevation
    print("UTC time is used!")
    print("   Start:\t\t\tStop:\t\t\t\tApogee:\t\t\t\tApogee elevation:")

    passes = getSatellitePasses(datetime.utcnow(), length, satellite, lon, lat, alt, horizon=defaultHorizon)
    for satPass in passes:
        print(f"{count}. ", end="")

        for date in satPass:
            print(date.strftime("%d.%m.%Y %H:%M:%S"), end="\t\t")

        count+=1

        print( round(orb.get_observer_look(satPass[2], lon, lat, alt)[1], 2) )
    

    # console track generator
    if input("Create track-file ? (y/n) ").lower() == "y":

        number = int( input("Enter pass number: ") )-1

        while number >= len(passes):
            print("Invalid pass number, try again.. ")
            number = int( input("Enter pass number: ") )-1
        
        print("Supported Track formats:")
        for trackFormat in trackFormats:
            print(trackFormat, end=", ")
        print()

        trackType = input("Enter track format: ").lower()

        while True:
            if trackType == "l2s":
                generateL2STrack(satellite, passes[number], lon, lat, alt, currentPath=currentPath, saveTrack=saveTrack, printTrack=printTrack)
                break
            
            elif trackType == "c4s":
                generateC4STrack(satellite, passes[number], lon, lat, alt, currentPath=currentPath, saveTrack=saveTrack, printTrack=printTrack)
                break
            
            else:
                print("Format is not recognized")
                trackType = input("Enter track format: ").lower()



if __name__ == "__main__":
     
    # if program has been started with additional parametres
    # for example: $python3 orbital.py METOP-A 
    if len(argv) > 1:

        # if additional parameter contain correct satellite name
        if argv[1] in sats.keys():
            satellite = sats[argv[1]]
        
        else:
            print("Satellite name not recognized")
            exit()

    else:        
        satellite = "NOAA 19"
        

    lon, lat, alt = getCoords()

    # meters --> kilometers
    alt /= 1000  

    print(f"Passes over the next 30 hours for {satellite}\n")
    print("UTC time now:", datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S"), end="\n\n")

    count = 1

    update(showLog=False)
    
    orb = Orbital(satellite, join( tlePath, "tle.txt" ) )
    
    # Print satellite passes in the format:
    # UTC time is used!
    # 1. datetime start         datetime end         datetime apogee    apogee elevation
    print("UTC time is used!")
    print("   Start:\t\t\tStop:\t\t\t\tApogee:\t\t\t\tApogee elevation:")

    passes = getSatellitePasses(datetime.utcnow(), 30, satellite, lon, lat, alt, horizon=defaultHorizon)
    for satPass in passes:
        print(f"{count}. ", end="")

        for date in satPass:
            print(date.strftime("%d.%m.%Y %H:%M:%S"), end="\t\t")

        count+=1

        print( round(orb.get_observer_look(satPass[2], lon, lat, alt)[1], 2) )
    
    if count > 1:
        # console track generator
        if input("Create track-file ? (y/n) ").lower() == "y":

            number = int( input("Enter pass number: ") )-1

            while number >= len(passes):
                print("Invalid pass number, try again.. ")
                number = int( input("Enter pass number: ") )-1

            print("Supported Track formats:")
            for trackFormat in trackFormats:
                print(trackFormat, end=", ")
            print()

            trackType = input("Enter track format: ").lower()

            while True:
                if trackType == "l2s":
                    generateL2STrack(satellite, passes[number], saveTrack=True, printTrack=True)
                    break
                
                elif trackType == "c4s":
                    generateC4STrack(satellite, passes[number], saveTrack=True, printTrack=True)
                    break
                
                else:
                    print("Format is not recognized")
                    trackType = input("Enter track format: ").lower()
    else:
        print("")

    
