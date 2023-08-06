from orbital import getCoords, sats, findPasses
from sys import argv



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

    findPasses(satellite, lon, lat, alt, length=30, currentPath="", printTrack=True, saveTrack=True)

