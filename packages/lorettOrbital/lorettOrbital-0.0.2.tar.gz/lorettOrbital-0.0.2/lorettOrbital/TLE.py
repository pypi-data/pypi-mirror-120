from requests import get, exceptions
from os.path import abspath, join, dirname
from datetime import datetime
from bs4 import BeautifulSoup as bs

from .config import *



__all__ = [
    "update",
]


# Service function that calculates count days since the biginning of the year
# In:
#   datetime date
# Out:
#   int deys
def getDays(date):
    days = date.day
    days += daysForMonth[ date.month-1 ]

    return days


# Function that updates TLE files
def update(showLog=True):

    try:
        if showLog:
            print("Connecting to celestrak.com\n")

        page = get( "http://celestrak.com/NORAD/elements/" )
        html = bs(page.content, "html.parser")
        now = datetime.utcnow()
        
        
        # Getting TLE date with server
        try:
            year = int(html.select('h3.center')[0].text.split(' ')[3])
            dayPass = int(html.select('h3.center')[0].text.replace(')', '').rsplit(' ', 1)[1])

        except:
            year = now.year
            dayPass = 0

        if showLog:    
            print("On site:")
            print(year, dayPass, end='\n\n')

        # Getting TLE date with client
        try:
            with open( join( tlePath, "tle.txt" ), "r" ) as file:
                yearInTLE, daysPassInTLE = map(int, file.readline().strip().split(' '))

        except:
            yearInTLE = now.year
            daysPassInTLE = 0

        if showLog:
            print("In TLE:")
            print(yearInTLE, daysPassInTLE, end='\n\n')


        # if TLE is outdated then update TLE
        if (yearInTLE <= year) and (daysPassInTLE < dayPass):
            if showLog:
                print("Update TLE..\n")

            with open( join( tlePath, "tle.txt" ), "wb" ) as file:
                file.write( f"{now.year} {getDays(now)}\n".encode('utf-8') )
                file.write(get("http://www.celestrak.com/NORAD/elements/weather.txt").content)
            
            if showLog:
                print("Done")

        else:
            if showLog:
                print("TLE are Relevant")

    except exceptions.ConnectionError:
        print('Error when update TLE')
        print("No internet connection\n")
    
    except Exception as e:
        print('Error when update TLE')
        print(str(e), "\n")



if __name__ == "__main__":
    update()