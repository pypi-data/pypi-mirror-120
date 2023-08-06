from os import getcwd
from os.path import abspath, join, dirname, isfile
from pathlib import Path



version = "0.0.2"

# Should I use the current cwd directory to store TLE and tracks or save him in library path
# Later, it will be possible to configure it normally
useCwd = False
root = abspath(getcwd()) if useCwd else abspath(dirname(__file__))


# additional directories
tlePath = join( root, "tle" )
Path( tlePath ).mkdir(parents=True, exist_ok=True)

tracksPath = join( root, "tracks" )
Path( tracksPath ).mkdir(parents=True, exist_ok=True)

tracksSchemesPath = join( root, "tracksSchemes" )
Path( tracksSchemesPath ).mkdir(parents=True, exist_ok=True)


# mirror specifications
defaultFocus = 0.77
defaultRadius = 0.55
defaultHorizon = 55
minApogee = 65
azimuthCorrection = 0


# colors
mirrorCircleColor = '#66ccff'


# list of supported Track formats
trackFormats = [
    "l2s",
    "c4s"
]


# For calculate the number of days since the beginning of the year (leap years are not taken into account)
daysForMonth = [
    0, 
    31,     # January
    59,     # February
    90,     # March
    120,    # April
    151,    # May
    181,    # June
    212,    # July
    243,    # August
    273,    # September
    304,    # October
    334,    # November
    365     # December
]

# dict for run with argv 
sats = {"NOAA-18":      "NOAA 18",
        "NOAA-19":      "NOAA 19",
        "METEOR-M-2":   "METEOR-M 2",
        "METEOR-M2-2":  "METEOR-M2 2",
        "METOP-B":      "METOP-B",
        "METOP-C":      "METOP-C",
        "FENGYUN-3B":   "FENGYUN 3B",
        "FENGYUN-3C":   "FENGYUN 3C"}

